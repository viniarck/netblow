#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from netblow.netblow import NetBlow


@pytest.fixture()
def funcs():
    """Functions that should be patched in napalm

    """
    return [
        'interfaces_down', 'interfaces_up', 'interfaces_flap', 'reboot',
        'show', 'config_rollback'
    ]


@pytest.fixture(scope='function')
def topology():
    """Dummy topology device dict fixture.
    These are all drivers that are currently supported.

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
            },
            'junos1': {
                'driver': 'junos',
                'hostname': 'labhost',
                'username': 'vrnetlab',
                'password': 'vrnetlab9',
                'optional_args': {
                    'port': 2224
                }
            },
            'iosxr1': {
                'driver': 'iosxr',
                'hostname': 'labhost',
                'username': 'vrnetlab',
                'password': 'vrnetlab9',
                'optional_args': {
                    'port': 2225
                }
            },
            'ios1': {
                'driver': 'ios',
                'hostname': 'labhost',
                'username': 'vrnetlab',
                'password': 'vrnetlab9',
                'optional_args': {
                    'port': 2226
                }
            }
        },
        'minions': ['minion1', 'minion2'],
    }


@pytest.fixture(scope='function')
def netblow(topology):
    """Dummy netblow dry run fixture

    """
    return NetBlow(dry_run=True, topo=topology)


@pytest.fixture(scope='function')
def netblow_salt(topology):
    """Dummy netblow dry run salt-enabled fixture

    """
    return NetBlow(dry_run=True, enable_salt=True, topo=topology)
