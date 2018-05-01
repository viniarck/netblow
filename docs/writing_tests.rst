.. _writing_tests_label:

Writing tests
=============

Either you choose to write your tests directly in Python, by instantiating NetBlow, or in yml files and run them in the CLI (command line interface).

Code Snippets
-------------

Let's say you want to perform some asynchronous interface flaps and afterwards, you want to keep tearing down the entire BGP configuration for a few seconds. In this case, I have two devices `eos1` and `junos1`:

.. note::

    The devices kwargs (keyword arguments) are exactly the same as documented in napalm RTD http://napalm.readthedocs.io/en/latest/base.html

.. code:: python

  #!/usr/bin/env python
  # -*- coding: utf-8 -*-

  from netblow.netblow import NetBlow


  def main():
      """Main func."""

      topology = {
          'devices': {
              'eos1': {
                  'driver': 'eos',
                  'hostname': 'labhost',
                  'username': 'vrnetlab',
                  'password': 'vrnetlab9',
                  'optional_args': {
                      'port': 4443
                  }
              },
              'junos1': {
                  'driver': 'junos',
                  'hostname': 'labhost',
                  'username': 'vrnetlab',
                  'password': 'vrnetlab9',
                  'optional_args': {
                      'port': 2224
                  }
              }
          }
      }

      nb = NetBlow(topo=topology)
      devices = ['eos1', 'junos1']
      interfaces = [['Ethernet 2'], ['ge-0/0/2']]

      # Interfaces flap stress async on 'eos1' and 'junos1'. Iterates 3 times.
      for dut, intfs in zip(devices, interfaces):
          nb.interfaces_flap(dut, interfaces=intfs, sync=False, iterations=3)
      nb.await()  # async await

      # Completely tear down current BGP synchronously during 30 secs.
      cmds = [['no router bgp'], ['delete protocols bgp']]
      for dut, cmds in zip(devices, cmds):
          nb.config_rollback(dut, commands=cmds, duration=30)


  if __name__ == "__main__":
      main()

.. note::

  You can find more snippets in the `integration test folder <https://github.com/viniciusarcanjo/netblow/tree/master/tests/integration>`_ on github.

If you were to run this Python code, you'd see an output similar to this:

.. code:: shell

  ~/repos/netblow/docs master*
  ❯ python examples/flap_rollback.py
  2018-05-01 12:49:58 [MainThread] [ INFO] Devices in the topology ['eos1', 'junos1']
  2018-05-01 12:49:58 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 12:49:58 [      eos1] [ INFO] Trying to connect on eos1...
  2018-05-01 12:49:58 [    junos1] [ INFO] Trying to connect on junos1...
  2018-05-01 12:50:01 [    junos1] [ INFO] Successfully connected on junos1
  2018-05-01 12:50:02 [      eos1] [ INFO] Successfully connected on eos1
  2018-05-01 12:50:02 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 12:50:02 [      eos1] [ INFO] Test interfaces_flap started on eos1
  2018-05-01 12:50:02 [    junos1] [ INFO] Test interfaces_flap started on junos1
  2018-05-01 12:50:02 [MainThread] [ INFO] Waiting for async tests to finish...
  2018-05-01 12:50:02 [      eos1] [ INFO]   Iteration #1/3 on eos1
  2018-05-01 12:50:02 [    junos1] [ INFO]   Iteration #1/3 on junos1
  2018-05-01 12:50:02 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 2'] down
  2018-05-01 12:50:02 [    junos1] [ INFO]     Shutting interfaces ['ge-0/0/2'] down
  2018-05-01 12:50:04 [    junos1] [ INFO]     Bringing interfaces ['ge-0/0/2'] up
  2018-05-01 12:50:06 [    junos1] [ INFO]   Iteration #2/3 on junos1
  2018-05-01 12:50:06 [    junos1] [ INFO]     Shutting interfaces ['ge-0/0/2'] down
  2018-05-01 12:50:08 [    junos1] [ INFO]     Bringing interfaces ['ge-0/0/2'] up
  2018-05-01 12:50:09 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 2'] up
  2018-05-01 12:50:10 [    junos1] [ INFO]   Iteration #3/3 on junos1
  2018-05-01 12:50:10 [    junos1] [ INFO]     Shutting interfaces ['ge-0/0/2'] down
  2018-05-01 12:50:12 [    junos1] [ INFO]     Bringing interfaces ['ge-0/0/2'] up
  2018-05-01 12:50:15 [      eos1] [ INFO]   Iteration #2/3 on eos1
  2018-05-01 12:50:15 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 2'] down
  2018-05-01 12:50:21 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 2'] up
  2018-05-01 12:50:27 [      eos1] [ INFO]   Iteration #3/3 on eos1
  2018-05-01 12:50:27 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 2'] down
  2018-05-01 12:50:34 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 2'] up
  2018-05-01 12:50:41 [      eos1] [ INFO] Test config_rollback started on eos1
  2018-05-01 12:50:41 [      eos1] [ INFO]   Iteration #1/31536000 on eos1
  2018-05-01 12:50:41 [      eos1] [ INFO]     Applying commands ['no router bgp'] on eos1
  2018-05-01 12:50:48 [      eos1] [ INFO]     Performing rollback
  2018-05-01 12:50:52 [      eos1] [ INFO]   Iteration #2/31536000 on eos1
  2018-05-01 12:50:52 [      eos1] [ INFO]     Applying commands ['no router bgp'] on eos1
  2018-05-01 12:50:59 [      eos1] [ INFO]     Performing rollback
  2018-05-01 12:51:03 [      eos1] [ INFO]   Iteration #3/31536000 on eos1
  2018-05-01 12:51:03 [      eos1] [ INFO]     Applying commands ['no router bgp'] on eos1
  2018-05-01 12:51:10 [      eos1] [ INFO]     Performing rollback
  2018-05-01 12:51:14 [      eos1] [ INFO]   Duration timeout exceeded. Aborting test.
  2018-05-01 12:51:14 [    junos1] [ INFO] Test config_rollback started on junos1
  2018-05-01 12:51:14 [    junos1] [ INFO]   Iteration #1/31536000 on junos1
  2018-05-01 12:51:14 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:16 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:17 [    junos1] [ INFO]   Iteration #2/31536000 on junos1
  2018-05-01 12:51:17 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:19 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:20 [    junos1] [ INFO]   Iteration #3/31536000 on junos1
  2018-05-01 12:51:20 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:22 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:23 [    junos1] [ INFO]   Iteration #4/31536000 on junos1
  2018-05-01 12:51:23 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:25 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:26 [    junos1] [ INFO]   Iteration #5/31536000 on junos1
  2018-05-01 12:51:26 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:28 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:29 [    junos1] [ INFO]   Iteration #6/31536000 on junos1
  2018-05-01 12:51:29 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:31 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:32 [    junos1] [ INFO]   Iteration #7/31536000 on junos1
  2018-05-01 12:51:32 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:34 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:35 [    junos1] [ INFO]   Iteration #8/31536000 on junos1
  2018-05-01 12:51:35 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:37 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:39 [    junos1] [ INFO]   Iteration #9/31536000 on junos1
  2018-05-01 12:51:39 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:41 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:42 [    junos1] [ INFO]   Iteration #10/31536000 on junos1
  2018-05-01 12:51:42 [    junos1] [ INFO]     Applying commands ['delete protocols bgp'] on junos1
  2018-05-01 12:51:44 [    junos1] [ INFO]     Performing rollback
  2018-05-01 12:51:45 [    junos1] [ INFO]   Duration timeout exceeded. Aborting test.
  2018-05-01 12:51:45 [MainThread] [ INFO] Closing connections to all devices


CLI
---

netblow also ships with a CLI, which you should probably use if you'd rather write tests in yml file than writing them directly in Python.

Options
^^^^^^^

In addition to the execution modes, in the CLI you also have to specify the topology yml file `-f` and the tests yml file `-t`, which describes all the arguments of your tests and how they are supposed to be executed.

.. code:: shell

  ❯ netblow -h
  usage: netblow [-h] [-d | -c | -1] [-l {info,debug}] [-v] [-f TOPOLOGY]
                 [-t TESTS]

  netblow. Vendor agnostic network testing framework to stress network failures.

  required arguments:
    -f TOPOLOGY, --topology TOPOLOGY
                          topology yml file
    -t TESTS, --tests TESTS
                          tests yml file

  optional arguments:
    -h, --help            show this help message and exit
    -d, --dryrun          show tests calls, won't connect to any devices
    -c, --concheck        check connectivity with all devices in the topology
    -1, --once            iterates only once and perfom napalm diffs
    -l {info,debug}, --level {info,debug}
                          logging verbosity level (default: info)
    -v, --version         show version

XDG-based directories
^^^^^^^^^^^^^^^^^^^^^

If you intend to also write tests in yml files, you probably want to organize these files somewhere. You could simply use the current working directory, or alternatively, XDG-based directories:

- `~/.config/netblow/topologies`: yml files in this folder represent all network devices involved in the tests, which you can target individually in the command line.
- `~/.config/netblow/scenarios_tests`: yml files in this folder are the actual tests specification and test execution.


.. _yml_files_label:

Topology yml files
^^^^^^^^^^^^^^^^^^

Let's say you have a topology with two EOS devices, you can create a yml file named, for instance, `eos_topo.yml`:

.. code::

  ---
  devices:
    eos1:
      driver: 'eos'
      hostname: 'labhost'
      username: 'vrnetlab'
      password: 'vrnetlab9'
      optional_args:
        port: 4443
    eos2:
      driver: 'eos'
      hostname: 'labhost'
      username: 'vrnetlab'
      password: 'vrnetlab9'
      optional_args:
        port: 4444


Tests yml file
^^^^^^^^^^^^^^

The yml tests file are composed of two main keys:

- `tests_specs`: specifies all tests, which are nested dictionaries that tell which function on netblow the user wants to run and which kwargs should be used.
- `tests_execution`: it's a list of dictionaries that dictates how the tests should be run, and scheduled either synchronously or asynchronously. Essentially, it's just a cross reference with the definitions in the `tests_specs`.

Let's assume I have two EOS networking devices, `eos1` and `eos2`, and I'd like to stress interface flaps. First, I have to specify how exactly I want the interface_flap kwargs for each device and then which order they are supposed to be run. In this case, I created the `scenarios_tests/eos_tests.yml`, which have two test_specs definitions, and three scheduled tests based on these definitions:

.. code::

  ---
  tests_specs:
    eos1_interfaces_flap:
      function: 'interfaces_flap'
      dut: 'eos1'
      interfaces: ['Ethernet 7', 'Ethernet 8']
    eos2_interfaces_flap:
      function: 'interfaces_flap'
      dut: 'eos2'
      interfaces: ['Ethernet 2', 'Ethernet 3']

  tests_execution:
    - tests: [eos1_interfaces_flap]
      kwargs:
        iterations: 2
    - tests: [eos1_interfaces_flap, eos2_interfaces_flap]
      kwargs:
        sync: False
    - tests: [eos1_interfaces_flap, eos2_interfaces_flap]
      kwargs:
        duration: 3
