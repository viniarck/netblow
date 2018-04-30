#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""netblow module."""

import atexit
import coloredlogs
import logging
import logging.config
import napalm
import napalm.eos.eos
import napalm.junos.junos
import napalm.iosxr.iosxr
import napalm.ios.ios
import netblow.monkey_patch.eos_driver
import netblow.monkey_patch.junos_driver
import netblow.monkey_patch.iosxr_driver
import netblow.monkey_patch.ios_driver
import signal
import time
import traceback
import sys
import yaml

from . import utils
from . import exceptions
from functools import wraps
from threading import Thread
from unittest.mock import MagicMock


class NetBlow(object):
    """Abstraction that performs network failures stress tests.

    Check the @blow decorator to see all functions and kwargs available.

    """

    # FSM States
    INIT = 'INIT'
    WAITING_MINIONS = 'WAITING_MINIONS'
    CONNECTED = 'CONNECTED'
    CONNECTING = 'CONNECTING'
    TESTING = 'TESTING'

    def __init__(self,
                 topo_file='',
                 test_file='',
                 auto_open=True,
                 auto_test=True,
                 enable_salt=False,
                 dry_run=False,
                 iter_once=False,
                 con_check=False,
                 level='info',
                 topo=None):
        """Constructor.

        :topo_file: name of the topology yml file in current dir, ./topologies, or ~/.config/netblow/topologies # noqa
        :test_file: name of the test yml file in current dir, ./scenarios_tests, or ~/.config/netblow/scenarios_tests # noqa
        :auto_open: automatically open connection for each device
        :auto_test: automatically start the tests
        :enable_salt: enable salt-pepper for data plane tests
        :dry_run: show scenarios tests calls, won't connect to any devices
        :iter_once: iterates only once in all tests with diff configs enabled
        :con_check: napalm connectivity check
        :level: logging verbosity level, either 'info' or 'debug'
        :topo: dictionary to load the topology instead of the topo_file. check the docs for the arguments.

        """
        super().__init__()
        # args
        self.topo_file = topo_file
        self.test_file = test_file
        self.auto_open = auto_open
        self.auto_test = auto_test
        self.enable_salt = enable_salt
        self.dry_run = dry_run
        self.iter_once = iter_once
        self.con_check = con_check
        self.level = level
        self.topo = topo

        self.mock = MagicMock()
        self.devices = dict()
        self.drivers = dict()
        self.global_args = dict()
        self.salt = None
        self.minions = dict()
        self.async_threads = []
        self.res = {}

        # init util functions
        self._init_logging()
        utils._bootstrap_xdg_dirs()
        signal.signal(signal.SIGINT, self._interrupt_handler)
        signal.signal(signal.SIGTERM, self._interrupt_handler)

        if self.dry_run:
            self.log.info('Dry run mode')
            self._setup_mock()

        self._load_topo()

        if self.enable_salt:
            self._start_salt()

        # open connections to all devices
        if self.auto_open or self.con_check:
            self.open_all()

        if self.auto_test:
            self._load_tests()
        if self.test_file:
            self._exec_tests()

        if self.dry_run:
            self._log_mock_call_trace()

    def _init_logging(self):
        """Initialize logging."""
        self.log = logging.getLogger(__name__)
        self.log.setLevel(utils._str_to_level(self.level))
        fmt = utils.FORMAT
        if self.level == utils.DEBUG:
            fmt = utils.FORMAT_DEBUG
        coloredlogs.install(
            logger=self.log,
            fmt=fmt,
            field_styles=utils.FIELD_STYLES,
            level_styles=utils.LEVEL_STYLES)

    def debug(self, msg):
        """Log debug message according to stack frame indentation level.

        :msg: log message

        """
        # subtracts 4 because of base frames, and adds 2 spaces per depth
        depth = (len(traceback.extract_stack()) - 4) * 2
        self.log.debug("{}{}".format(' ' * depth, msg))

    def info(self, msg):
        """Log info message according to stack frame indentation level.

        :msg: log message

        """
        # subtracts 4 because of base frames, and adds 2 spaces per depth
        depth = (len(traceback.extract_stack()) - 4) * 2
        self.log.info("{}{}".format(' ' * depth, msg))

    def _monkey_patch(self, driver):
        """Monkey patch napalm drivers for network failure functions."""
        if isinstance(driver, napalm.eos.eos.EOSDriver):
            netblow.monkey_patch.eos_driver.EOSDriver(driver)
        if isinstance(driver, napalm.junos.junos.JunOSDriver):
            netblow.monkey_patch.junos_driver.JunOSDriver(driver)
        if isinstance(driver, napalm.ios.ios.IOSDriver):
            netblow.monkey_patch.ios_driver.IOSDriver(driver)
        if isinstance(driver, napalm.iosxr.iosxr.IOSXRDriver):
            netblow.monkey_patch.iosxr_driver.IOSXRDriver(driver)
        # attribute to register when a reboot was intentional
        setattr(driver, 'intentional_reboot', False)
        # finite state machine state simplified
        setattr(driver, 'state', NetBlow.INIT)
        # current function running on thread
        setattr(driver, 'func_running', NetBlow.CONNECTING)

    def _load_minions(self, minions):
        """Load minions states.

        :minions: list of minions
        """
        self.log.info('Minions in the topology {}'.format(minions))
        self.minions = {}
        for minion in minions:
            self.minions[minion] = {'id': minion, 'connected': False}

    def _start_salt(self):
        """Start salt-master."""
        if not self.dry_run:
            self.log.error(
                'salt-pepper will be implemented in the next release')
            return

    def _consume_event(self, tag, data):
        """Consume SaltEvent reactor callback.

        :tag: tag
        :data: data

        """
        if 'salt/minion' in tag:
            minion_id = data.get('id')
            if self.minions.get(minion_id):
                self.log.info('Minion {} is connected'.format(minion_id))
                self.minions[data.get('id')]['connected'] = True
            else:
                self.log.error('Minion {} is not authorized'.format(minion_id))

    def _wait_minions_connect(self):
        """Wait for minions to get connected."""
        self.log.info('Checking if minions are connected...')
        all_connected = False
        while not all_connected:
            for name, minion in self.minions.items():
                all_connected = True
                if not minion.get('connected'):
                    all_connected = False
                    break
            if all_connected:
                break
            time.sleep(1)
        self.load_tests()

    def _interrupt_handler(self, signal, frame):
        """Catch SIGINT and SIGTERM to exit gracefully."""
        self.log.info('Caught interruption signal. Exiting...')
        self._exit(1)

    def _setup_mock(self):
        """Set up mock calls trace."""
        self.interfaces_flap = MagicMock()
        self.mock.interfaces_flap = self.interfaces_flap

        self.interfaces_down = MagicMock()
        self.mock.interfaces_down = self.interfaces_down

        self.interfaces_up = MagicMock()
        self.mock.interfaces_up = self.interfaces_up

        self.reboot = MagicMock()
        self.mock.reboot = self.reboot

        self.config_rollback = MagicMock()
        self.mock.config_rollback = self.config_rollback

        self.show = MagicMock()
        self.mock.show = self.mock.show

    def _log_mock_call_trace(self):
        """Log mock call trace stack."""
        self.log.info('Mock call trace: ')
        for call in self.mock.mock_calls:
            self.log.info(call)

    def _load_yml(self, yaml_file):
        """Load an yaml file.

        :yaml: yaml file path
        :returns: dictionary

        """
        try:
            with open(yaml_file) as f:
                return yaml.load(f)
        except IOError as e:
            raise e
        except yaml.YAMLError as e:
            raise e

    def _load_topo(self):
        """Load topology file."""
        # if a dict was passed in init, prefer the dict over self.topo_file
        if self.topo:
            topo = self.topo
        else:
            if self.topo_file:
                try:
                    topo_file = utils.find_file(self.topo_file, utils.TOPO_DIR)
                    self.log.info('Loading topology file {}'.format(topo_file))
                    topo = self._load_yml(topo_file)
                except OSError as e:
                    self.log.error(str(e))
                    self._exit(1)
            else:
                self.log.error(
                    'Neither topology file nor topology dict were specified.')
                self._exit(1)
        try:
            devices = topo['devices']
        except KeyError:
            err = "Topology doesn't have 'devices'"
            self.log.error(err)
            raise ValueError(err)
        self.log.info('Devices in the topology {}'.format((list(
            devices.keys()))))
        for k, v in devices.items():
            self.devices[k] = v
            try:
                driver = napalm.get_network_driver(v['driver'])
                if not v.get('timeout'):
                    v['timeout'] = 30
                self.drivers[k] = driver(
                    hostname=v['hostname'],
                    username=v['username'],
                    password=v['password'],
                    timeout=v['timeout'],
                    optional_args=v.get('optional_args'))
                self._monkey_patch(self.drivers[k])
            except KeyError:
                self.log.error(
                    "Missing 'driver' in the devices. Check napalm docs.")

        if self.enable_salt:
            try:
                self._load_minions(topo['minions'])
            except KeyError:
                self.log.error("Missing 'minions' in the topology")
                self._exit(1)

    def _load_tests(self):
        """Load test file."""
        if self.test_file:

            def check_nested_dict(obj):
                """Check if obj is a dict."""
                if not isinstance(obj, dict):
                    msg = "This key '{}' was supposed to be a dictionary"
                    self.log.error(msg.format(obj))
                    self._exit(1)

            test_file = utils.find_file(
                self.test_file, sub_dir=utils.TESTS_DIR)
            self.log.info('Loading test file {}'.format(test_file))

            test_data = self._load_yml(test_file)
            self.tests_specs = test_data.get('tests_specs')
            if not self.tests_specs:
                self.log.error(
                    "Missing 'test_specs' in the test file {}".format(
                        self.test_file))
                self._exit(1)

            for test_name, nested_dict in self.tests_specs.items():
                check_nested_dict(nested_dict)

            self.tests_execution = test_data.get('tests_execution')
            if not self.tests_execution:
                self.log.error(
                    "Missing 'test_execution' in the test file {}".format(
                        self.test_file))
                self._exit(1)
                for test_specs in self.tests_execution:
                    if not self.tests_specs.get(test_specs):
                        self.log.error(
                            "This test {} is not in 'tests_specs'".format(
                                test_specs))
                        self._exit(1)

    def _exec_tests(self):
        """Execute tests parsed from yml file."""
        for tests in self.tests_execution:
            inner_tests = tests['tests']
            kwargs = tests.get('kwargs', {})
            sync = kwargs.get('sync', True)
            for test in inner_tests:
                try:
                    test_args = self.tests_specs[test]
                    blow_func = getattr(self, test_args['function'])
                    dut = test_args['dut']

                    # update kwargs from test_specs
                    for k, value in test_args.items():
                        if k not in ['function', 'dut']:
                            kwargs[k] = value
                    blow_func(dut, **kwargs)
                except AttributeError:
                    self.log.error("Function '{}' doesn't exist".format(test))
            if not sync:
                self.await()

    def _val_dut_key(self, dut):
        """Validate if dut key is present. If it is, return the driver.
        Otherwise, log error message and call self._exit(1).

        :dut: string name of the device under test

        """
        driver = self.drivers.get(dut)
        if not driver:
            self.log.error('Device {} is not in the topology'.format(dut))
            return self._exit(1)
        return driver

    def open(self, dut, timeout=600, retry_interval=30):
        """Connect to a device in the topology.

        :dut: string name of the device under test
        :timeout: maximum number of seconds to potentially wait for
        :retry_interval: retry interval per iteration in seconds

        Raises exceptions.MaxReconnectionRetries

        """
        start_time = time.time()
        retry = 0
        while True:
            if time.time() >= start_time + timeout:
                self.log.error(
                    'Maximum connection retries reached on {}'.format(dut))
                raise exceptions.MaxReconnectionRetries()
            driver = self.drivers[dut]
            try:
                self.log.info('Trying to connect on {}...'.format(dut))
                driver.open()
                driver.cli(['show version'])
                driver.state = NetBlow.CONNECTED
                self.log.info('Successfully connected on {}'.format(dut))
                return
            except Exception as e:  # instead of dozens of different exceptions
                time_diff = timeout - (time.time() - start_time)
                retry += 1
                retry_msg = 'Waiting for {} seconds...'
                retry_msg_left = '{} seconds left before timeouting...'
                self.log.info('Retry #{}'.format(retry))
                # if wasn't intentional log as error
                if not driver.intentional_reboot:
                    if not str(e) == 'None':
                        self.log.error(e)
                else:
                    if not str(e) == 'None':
                        self.log.info(e)
                self.log.debug('Device {} params: {}'.format(
                    driver.hostname, driver.__dict__))
                self.log.info(retry_msg.format(retry_interval))
                self.log.info(retry_msg_left.format(int(time_diff)))
                time.sleep(retry_interval)

    def open_all(self):
        """Connect to all devices in the topology."""
        if not self.dry_run:
            # tear down cleanup callback
            atexit.register(self._tear_down)

            threads = []
            self.log.info('Trying to open connections to all devices...')
            for device_name, driver in self.drivers.items():
                # only starts a new thread if it hasn't been connected before
                if driver.state == NetBlow.INIT:
                    t = Thread(
                        target=self.open,
                        args=(device_name, ),
                        name=device_name,
                        daemon=True)
                    t.start()
                    threads.append(t)
            try:
                for t in threads:
                    t.join()
                self.log.info('All devices are CONNECTED')
            except exceptions.MaxReconnectionRetries:
                self._exit(1)

            if self.con_check:
                self._exit()

    def _tear_down(self):
        """Tear down everything."""
        if not self.dry_run:
            if self.drivers:
                self.log.info('Closing connections to all devices')
            for device_name, driver in self.drivers.items():
                if driver.state == NetBlow.TESTING:
                    # TODO handle discard_config()
                    pass
                driver.close()

            if self.salt:
                # TODO: handle salt-pepper tear down.
                pass

        if self.async_threads:
            self.log.warn('You started async tests but never called await()')

    def _exit(self, exit_code=0):
        """Exit and tear down netblow with a specific exit code.

        :exit_code: exit code int

        """
        self._tear_down()
        sys.exit(exit_code)

    def _wait_state(self, dut, state, iterations_to_log=5, delay=1):
        """Blocking call to wait until fsm is in a particular state.

        :dut: string name of the device under test
        :state: NetBlow state
        :iterations_to_log: number of iterations to send a log message

        """
        it = 0
        while not self.drivers[dut].state == state:
            it += 1
            time.sleep(delay)
            if it % iterations_to_log == 0 or it == 1:
                self.log.info(
                    'Waiting for state {}. Currently running {}...'.format(
                        state, self.drivers[dut].func_running))

    def await(self):
        """Await all async threads."""
        self.log.info('Waiting for async tests to finish...')
        for t in self.async_threads:
            t.join()
        # clear them all
        self.async_threads = []

    def _blow_callback(self, dut, **kwargs):
        """Update done state for a specific dut/device.

        :dut: string name of the device under test

        """
        self.res[dut] = kwargs

    def results(self, dut):
        """Get dut results.

        TODO: update with data plane results when salt is ready.

        :dut: string name of the device under test
        :returns: dict

        """
        if self.res.get(dut):
            return self.res[dut]
        return {}

    def blow(func):
        """Blow test decorator.

        :func: a function to be decorated
        :dut: string name of the device under test
        :sync: true to run synchronously or false to run asynchronously
        :iterations: number of iterations
        :duration: maximum test duration in seconds (default: one year)
        :iter_delay: delay at the end of each iteration
        :iter_check: True to check icmp per iteration (salt)
        :final_check: True to check icmp when the test is done (salt)

        """
        MAX_VALUE = 31536000  # one year in secs.

        @wraps(func)
        def wrapper(self,
                    dut,
                    sync=True,
                    iterations=1,
                    duration=MAX_VALUE,
                    iter_delay=0,
                    iter_check=False,
                    final_check=False,
                    **kwargs):
            # to support async, each test runs in a thread
            def blow_thread(dut, sync, iterations, duration, iter_delay,
                            iter_check, final_check, callback, **kwargs):

                self.log.info("Test {0} started on {1}".format(
                    func.__name__, dut))
                start_time = time.time()

                # by design, these are meant to iterate only once
                if func.__name__ in [
                        'interfaces_down', 'interfaces_up', 'show'
                ] or self.iter_once:
                    iterations = 1

                # if the user set the duration, increase iterations to MAX
                if not duration == MAX_VALUE:
                    iterations = MAX_VALUE

                driver = self.drivers[dut]
                for iteration in range(iterations):
                    if time.time() >= start_time + duration:
                        self.info('Duration timeout exceeded. Aborting test.')
                        break
                    try:
                        self.info('Iteration #{}/{} on {}'.format(
                            iteration + 1, iterations, dut))
                        func(
                            self,
                            dut,
                            iterations=iterations,
                            duration=duration,
                            iter_delay=iter_delay,
                            iter_check=iter_check,
                            final_check=final_check,
                            **kwargs)
                        if iter_delay:
                            self.info(
                                "Delaying for 'iter_delay' {} secs".format(
                                    iter_delay))
                            time.sleep(iter_delay)
                        if self.enable_salt:
                            if iter_check:
                                # TODO: implement iter_check (depends on salt)
                                self.log.info('iter_check')
                    except napalm.base.exceptions.SessionLockedException as e:
                        self.log.error(e)
                        self.log.info(
                            'Trying to release the configuration lock')
                        driver.discard_config()
                        continue
                    except napalm.base.exceptions.MergeConfigException as e:
                        msg = "Couldn't commit config. Check your parameters"
                        self.log.error(msg)
                        self.log.error(e)
                        self._exit(1)
                    except (napalm.base.exceptions.ConnectionClosedException,
                            napalm.base.exceptions.CommandTimeoutException,
                            napalm.base.exceptions.CommandErrorException) as e:
                        if not str(e) == 'None' and not getattr(
                                driver, 'intentional_reboot', False):
                            self.log.error(e)
                        driver.state = NetBlow.CONNECTING
                        self.open(dut)

                if self.enable_salt:
                    if final_check:
                        # TODO implement final_check (depends on salt)
                        self.log.info('final_check')
                # when the test is done return to the connected state
                driver.state = NetBlow.CONNECTED
                # results callback
                res = dict(kwargs)
                res.update({
                    'iterations': iterations,
                    'iter_delay': iter_delay,
                    'iter_check': iter_check,
                    'final_check': final_check
                })
                callback(dut, **res)

            driver = self._val_dut_key(dut)

            # each device runs only once blow test at a time (config lock)
            if driver.state == NetBlow.TESTING:
                self.log.warn(
                    'Device {} is still running {}. Aborting this {} call'.
                    format(dut, driver.func_running, func.__name__))
                return

            self._wait_state(dut, NetBlow.CONNECTED)
            driver.state = NetBlow.TESTING
            driver.func_running = func.__name__

            # TODO implement the actual callback though
            # callback to await the results later
            callback = self._blow_callback
            t = Thread(
                target=blow_thread,
                args=(dut, sync, iterations, duration, iter_delay, iter_check,
                      final_check, callback),
                name=dut,
                daemon=True,
                kwargs=kwargs)
            t.start()
            if sync:
                t.join()
            else:
                self.async_threads.append(t)

        return wrapper

    def _commit(self, dut):
        """Perform commit and if iter_once is enabled, perform diff as well.

        :dut: string name of the device under test

        """
        if self.iter_once:
            diff = self.drivers[dut].compare_config()
            self.info('Diff: \n{}'.format(diff))
        self.drivers[dut].commit_config()

    @blow
    def interfaces_flap(self, dut, interfaces, down_delay=0, **kwargs):
        """Perform interface flap.
        Check out @blow for default supported kwargs.

        :dut: string name of the device under test
        :interfaces: list of strings, interface names
        :down_delay: delay after shutting down the interface

        """
        dut_driver = self.drivers[dut]
        self.info('Shutting interfaces {} down'.format(interfaces))
        dut_driver.interfaces_down(interfaces=interfaces)
        self._commit(dut)

        if down_delay:
            self.info("Delaying for 'down_delay' {} secs".format(down_delay))
            time.sleep(down_delay)
        self.info('Bringing interfaces {} up'.format(interfaces))
        dut_driver.interfaces_up(interfaces=interfaces)
        self._commit(dut)

    @blow
    def interfaces_up(self, dut, interfaces, **kwargs):
        """Bring interfaces up. Iterates only once.
        Check out @blow for default supported kwargs.

        :dut: string name of the device under test
        :interfaces: list of strings, interface names

        """
        dut_driver = self.drivers[dut]
        self.info('Bringing interfaces {} up'.format(interfaces))
        dut_driver.interfaces_up(interfaces=interfaces)
        self._commit(dut)

    @blow
    def interfaces_down(self, dut, interfaces, **kwargs):
        """Shut interfaces down. Iterates only once.
        Check out @blow for default supported kwargs.

        :dut: string name of the device under test
        :interfaces: list of strings, interface names

        """
        dut_driver = self.drivers[dut]
        self.info('Shutting interfaces {} down'.format(interfaces))
        dut_driver.interfaces_down(interfaces=interfaces)
        self._commit(dut)

    @blow
    def reboot(self, dut, **kwargs):
        """Perform reboot. Check out @blow for default supported kwargs.

        :dut: string name of the device under test
        :force: True, to force. It is false by default

        """
        dut_driver = self.drivers[dut]
        try:
            self.info('Rebooting {}'.format(dut))
            dut_driver.reboot(optional_args=kwargs.get('optional_args'))
        except exceptions.RebootException:
            setattr(dut_driver, 'intentional_reboot', True)
            self.open(dut)

    @blow
    def show(self, dut, commands, **kwargs):
        """Execute show commands. Iterates only once.

        It's intended for being used at the beginning and end of the tests.

        :dut: string name of the device under test
        :commands: show commands, list of strings

        """
        dut_driver = self.drivers[dut]
        self.info('Applying show commands {} on {}'.format(commands, dut))
        outputs = dut_driver.cli(commands=commands)
        for command in commands:
            self.info('{}\n{}'.format(command, outputs[command]))
        return outputs

    @blow
    def config_rollback(self, dut, commands, commands_delay=0, **kwargs):
        """Apply configurations commands followed by a rollback.

        Check out @blow for default supported kwargs

        :dut: string name of the device under test
        :commands: list of the commands to be applied
        :commands_delay: delay after applying the first commands

        """
        dut_driver = self.drivers[dut]
        self.info('Applying commands {} on {}'.format(commands, dut))
        cmds = ''
        for cmd in commands:
            cmds += cmd + '\n'
        dut_driver.load_merge_candidate(config=cmds)
        self._commit(dut)

        if commands_delay:
            self.info(
                "Delaying for 'commands_delay' {} secs".format(commands_delay))
            time.sleep(commands_delay)
        self.info('Performing rollback')
        dut_driver.rollback()

    @blow
    def _blow(self, dut, **kwargs):
        """Blow dummy function to test blow decorator.

        :dut: string name of the device under test

        """
        pass
