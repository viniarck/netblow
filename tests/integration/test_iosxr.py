#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from netblow.netblow import NetBlow


@pytest.fixture(scope='module')
def iosxr_topo():
    """topology fixture

    """
    return {
        'devices': {
            'iosxr1': {
                'driver': 'iosxr',
                'hostname': 'labhost',
                'username': 'vrnetlab',
                'password': 'vrnetlab9',
                'optional_args': {
                    'port': 2225
                }
            }
        }
    }


@pytest.fixture(scope='module')
def get_netblow(iosxr_topo):
    """netblow fixture

    """
    return NetBlow(topo=iosxr_topo)


def test_interfaces(get_netblow):

    interfaces = ['GigabitEthernet0/0/0/1', 'GigabitEthernet0/0/0/2']
    dut = 'iosxr1'
    netblow = get_netblow

    netblow.interfaces_down(dut, interfaces=interfaces)
    netblow.interfaces_up(dut, interfaces=interfaces)


def test_config_merge(iosxr_topo):

    netblow = NetBlow(topo=iosxr_topo, iter_once=True)
    dut = 'iosxr1'
    commands = ['router bgp 65001']
    netblow.config_rollback(dut, commands=commands)


def test_show(get_netblow):

    netblow = get_netblow
    dut = 'iosxr1'
    show_commands = ['show version']
    netblow.show(dut, commands=show_commands)


@pytest.mark.slow
def test_reboot(get_netblow):

    dut = 'iosxr1'
    netblow = get_netblow

    netblow.reboot(dut)
