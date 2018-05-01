#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from netblow.netblow import NetBlow
from unit_fixtures import topology


def test_load_topology_yml_file():
    """Test load topology from yml file.

    """
    nb = NetBlow(topo_file='eos_topo.yml', dry_run=True)
    assert set(['eos1', 'eos2']) == set(nb.devices.keys())


def test_load_eos_test_yml_file(topology):
    """Test loading eos tests from yml file.

    """
    nb = NetBlow(test_file='eos_tests.yml', topo=topology, dry_run=True)
    assert len(nb.mock.mock_calls) == 5
