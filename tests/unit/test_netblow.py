#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pytest
from unittest.mock import MagicMock
from threading import Thread
from unit_fixtures import funcs
from unit_fixtures import topology
from unit_fixtures import netblow
from unit_fixtures import netblow_salt
from netblow.netblow import NetBlow


def test_dry_run(topology, netblow, funcs):
    """Test dry run mode.

    """
    for f in funcs:
        assert isinstance(netblow.__dict__.get(f), MagicMock)
    assert set(netblow.devices) == set(topology['devices'])


def test_patched_drivers_attrs(netblow):
    """Test all attributes that should be patched in napalm drivers

    """
    for device_name, driver in netblow.drivers.items():
        assert driver.intentional_reboot == False
        assert driver.state == netblow.INIT
        assert driver.func_running == netblow.CONNECTING


def test_patched_funcs(netblow, funcs):
    """Test all functions that should be patched in napalm all napalm drivers
    The topology fixture has all current supported drivers

    """
    for f in funcs:
        for device_name, driver in netblow.drivers.items():
            assert getattr(netblow, f)


def test_load_minions(netblow_salt, topology):
    """Test load minions.

    """
    minions = topology['minions']
    nb_minions = list(netblow_salt.minions.keys())
    assert set(nb_minions) == set(minions)


def test_load_topo_file(topology):
    """Test load topology (devices and minions) from yml file

    """
    nb = NetBlow(dry_run=True, enable_salt=True, topo_file='topology.yml')
    assert set(nb.devices.keys()) == set(topology['devices'].keys())
    assert set(nb.minions.keys()) == set(topology['minions'])


def test_exit_func(netblow):
    """Test netblow exit and tear_down

    """
    with pytest.raises(SystemExit):
        netblow._exit(0)


def test_neither_topo_nor_file():
    """Test if it quits if neither the topo dict nor the topo.yml file were specified

    """
    with pytest.raises(SystemExit):
        NetBlow(topo=None, test_file='')


def test_wait_state(netblow):
    """Test wait state function

    """

    def short_delay(device_name):
        """Changes device_name driver state to TESTING after 10ms

        """
        time.sleep(0.01)
        netblow.drivers[device_name].state = netblow.TESTING

    eos_name = 'eos1'
    eos_driver = netblow.drivers[eos_name]
    assert eos_driver.state == netblow.INIT
    # to bypass sync blocking call
    Thread(target=short_delay, args=(eos_name, )).start()
    netblow._wait_state(eos_name, state=netblow.TESTING, delay=0.02)
    assert eos_driver.state == netblow.TESTING
