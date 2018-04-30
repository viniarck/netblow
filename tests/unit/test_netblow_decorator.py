#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from unit_fixtures import netblow_salt as netblow_obj
from unit_fixtures import topology


@pytest.fixture()
def netblow(netblow_obj):
    """Netblow object with patched drivers in the connected state (faking napalm connected)
    to test decorator parameters

    """
    for device_name, driver in netblow_obj.drivers.items():
        driver.state = netblow_obj.CONNECTED
    return netblow_obj


def test_inexistent_dut(netblow):
    """Test inexistent dut

    """
    with pytest.raises(SystemExit):
        netblow._blow('inexistent_dut')


def test_iterations(netblow, caplog):
    """Test iterations

    """
    iters = 3
    netblow._blow('eos1', iterations=iters)
    # matches if the iteration number is in the log messages
    assert "{0}/{0}".format(iters) in caplog.text


def test_duration(netblow, caplog):
    """Test duration

    """
    dur = 0.05
    iters = 1000
    netblow._blow('eos1', iterations=iters, duration=dur, iter_delay=0.1)
    assert "Duration timeout" in caplog.text
    # take the chance to also test iter_delay to save time
    assert "Delaying for 'iter_delay'" in caplog.text


def test_iter_once(netblow, caplog):
    """Test iter once global

    """
    iters = 10
    netblow._blow('eos1', iterations=iters)
    assert "{0}/{0}".format(1) in caplog.text


@pytest.mark.skip(msg='test for the next release')
def test_iter_check(netblow, caplog):
    """Test iter_check

    """
    netblow._blow('eos1')
    assert "iter_check" in caplog.text


@pytest.mark.skip(msg='test for the next release')
def test_final_check(netblow, caplog):
    """Test iter_check

    """
    netblow._blow('eos1')
    assert "final_check" in caplog.text


def test_device_alredy_running(netblow, caplog):
    """Test that multiple async tests can't be run in the same device

    """
    for _ in range(2):
        netblow._blow('eos1', sync=False, iter_delay=0.01)
    assert "is still running _blow" in caplog.text


def test_async(netblow, caplog):
    """Test that async tests can run in different devices.

    """
    for device_name in ['eos1', 'eos2']:
        netblow._blow(device_name, sync=False, iter_delay=0.01)
        assert netblow.drivers[device_name].state == netblow.TESTING


def test_sync(netblow, caplog):
    """Test sync tests in different devices.

    """
    for device_name in ['eos1', 'eos2']:
        netblow._blow(device_name)
        # It should be in the CONNECTED state when the sync call is done
        assert netblow.drivers[device_name].state == netblow.CONNECTED
