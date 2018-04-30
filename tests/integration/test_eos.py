#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from netblow.netblow import NetBlow


@pytest.fixture(scope='module')
def eos_topo():
    """topology fixture

    """
    return {
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
            'eos2': {
                'driver': 'eos',
                'hostname': 'labhost',
                'username': 'vrnetlab',
                'password': 'vrnetlab9',
                'optional_args': {
                    'port': 4444
                }
            }
        }
    }


@pytest.fixture(scope='module')
def get_netblow(eos_topo):
    """netblow fixture

    """
    return NetBlow(topo=eos_topo)


def test_interfaces_async(get_netblow):

    netblow = get_netblow
    interfaces = ['Ethernet 7', 'Ethernet 8']
    sync = False

    for dut in ['eos1', 'eos2']:
        netblow.interfaces_down(dut, sync=sync, interfaces=interfaces)
    netblow.await()

    for dut in ['eos1', 'eos2']:
        netblow.interfaces_up(dut, sync=sync, interfaces=interfaces)
    netblow.await()


def test_interfaces_sync(get_netblow):

    netblow = get_netblow
    interfaces = ['Ethernet 7', 'Ethernet 8']

    for dut in ['eos1', 'eos2']:
        netblow.interfaces_down(dut, interfaces=interfaces)

    for dut in ['eos1', 'eos2']:
        netblow.interfaces_up(dut, interfaces=interfaces)


def test_config_merge(eos_topo):

    netblow = NetBlow(topo=eos_topo, iter_once=True)
    dut = 'eos1'
    commands = ['hostname {}'.format(dut * 2)]
    netblow.config_rollback(dut, commands=commands)


def test_show(get_netblow):

    netblow = get_netblow
    dut = 'eos2'
    show_commands = ['show version']
    netblow.show(dut, commands=show_commands)


@pytest.mark.slow
def test_reboot(get_netblow):

    netblow = get_netblow
    dut = 'eos1'

    netblow.reboot(dut)
