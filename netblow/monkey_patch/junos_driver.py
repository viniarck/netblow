#!/usr/bin/env python
# -*- coding: utf-8 -*-

import napalm
import ncclient
import time
from jnpr.junos.exception import ConnectClosedError
from netblow.exceptions import RebootException


class JunOSDriver(object):
    """Monkey patch JunOSDriver."""

    def __init__(self, driver):
        """Constructor.

        :driver: napalm.junos.junos.JunOSDriver instance

        """
        self.driver = driver

        self.driver.interfaces_down = self.interfaces_down.__get__(
            self.driver, napalm.junos.junos.JunOSDriver)
        self.driver.interfaces_up = self.interfaces_up.__get__(
            self.driver, napalm.junos.junos.JunOSDriver)
        self.driver.reboot = self.reboot.__get__(
            self.driver, napalm.junos.junos.JunOSDriver)

    def interfaces_down(self, interfaces):
        """Shut interfaces down.

        :interfaces: list of interfaces

        """
        commands_str = ''
        for interface in interfaces:
            commands_str += "set interfaces {} disable\n".format(interface)
        self.driver.load_merge_candidate(config=commands_str)

    def interfaces_up(self, interfaces):
        """Bring interfaces up.

        :interfaces: list of interfaces

        """
        commands_str = ''
        for interface in interfaces:
            commands_str += "delete interfaces {} disable\n".format(interface)
        self.driver.load_merge_candidate(config=commands_str)

    def reboot(self, optional_args=None):
        """Reboot.

        Raises exceptions.RebootException when it succeeds.

        """
        commands = []
        commands.append('request system reboot')
        try:
            self.driver.cli(commands)
            self.driver.commit_config()
        except ConnectClosedError:
            raise RebootException()
