#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from netblow.netblow import NetBlow


@pytest.fixture(scope='module')
def junos_topo():
    """topology fixture

    """
    return {
        'devices': {
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


@pytest.fixture(scope='module')
def get_netblow(junos_topo):
    """netblow fixture

    """
    return NetBlow(topo=junos_topo)


def test_interfaces(get_netblow):

    interfaces = ['ge-0/0/1', 'ge-0/0/2']
    dut = 'junos1'
    netblow = get_netblow

    netblow.interfaces_down(dut, interfaces=interfaces)
    netblow.interfaces_up(dut, interfaces=interfaces)
    netblow.interfaces_flap(dut, interfaces=interfaces)


def test_config_merge(junos_topo):

    netblow = NetBlow(topo=junos_topo, iter_once=True)
    dut = 'junos1'
    commands = [
        'set system domain-name lab.com', 'set system ntp peer 10.10.10.10'
    ]
    netblow.config_rollback(dut, commands=commands)


def test_show(get_netblow):

    netblow = get_netblow
    dut = 'junos1'
    show_commands = ['show interfaces terse', 'show version']
    netblow.show(dut, commands=show_commands)


@pytest.mark.slow
def test_reboot(get_netblow):

    netblow = get_netblow
    dut = 'junos1'
    netblow.reboot(dut)
