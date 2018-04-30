#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from netblow.netblow import NetBlow


@pytest.fixture(scope='module')
def ios_topo():
    """topology fixture

    """
    return {
        'devices': {
            'ios1': {
                'driver': 'ios',
                'hostname': 'labhost',
                'username': 'vrnetlab',
                'password': 'vrnetlab9',
                'optional_args': {
                    'port': 2226
                }
            }
        }
    }


@pytest.fixture(scope='module')
def get_netblow(ios_topo):
    """netblow fixture

    """
    return NetBlow(topo=ios_topo)


def test_interfaces(get_netblow):

    interfaces = ['GigabitEthernet12', 'GigabitEthernet13']
    dut = 'ios1'
    netblow = get_netblow

    netblow.interfaces_down(dut, interfaces=interfaces)
    netblow.interfaces_up(dut, interfaces=interfaces)


def test_config_merge(ios_topo):

    netblow = NetBlow(topo=ios_topo, iter_once=True)
    dut = 'ios1'
    commands = ['router bgp 65000']
    netblow.config_rollback(dut, commands=commands)


def test_show(get_netblow):

    netblow = get_netblow
    dut = 'ios1'
    show_commands = ['show version']
    netblow.show(dut, commands=show_commands)


@pytest.mark.slow
def test_reboot(get_netblow):

    dut = 'ios1'
    netblow = get_netblow

    netblow.reboot(dut)
