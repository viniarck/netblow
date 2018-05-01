#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IOSDriver module."""

import napalm
from netblow.exceptions import RebootException


class IOSDriver(object):
    """Monkey patch IOSDriver."""

    def __init__(self, driver):
        """Constructor.

        :driver: napalm driver

        """
        self.driver = driver

        self.driver.interfaces_down = self.interfaces_down.__get__(
            self.driver, napalm.ios.ios.IOSDriver)
        self.driver.interfaces_up = self.interfaces_up.__get__(
            self.driver, napalm.ios.ios.IOSDriver)
        self.driver.reboot = self.reboot.__get__(self.driver,
                                                 napalm.ios.ios.IOSDriver)

    def interfaces_down(self, interfaces):
        """Shut interfaces down.

        :interfaces: list of interfaces

        """
        commands_str = ''
        for interface in interfaces:
            commands_str += "interface {}\n".format(interface)
            commands_str += "shutdown \n"
        self.driver.load_merge_candidate(config=commands_str)

    def interfaces_up(self, interfaces):
        """Bring interfaces up.

        :interfaces: list of interfaces

        """
        commands_str = ''
        for interface in interfaces:
            commands_str += "interface {}\n".format(interface)
            commands_str += "no shutdown \n"
        self.driver.load_merge_candidate(config=commands_str)

    def reboot(self, optional_args=None):
        """Reboot.

        Raises exceptions.RebootException when it succeeds.

        """
        command = 'reload\n'
        self.driver.device.send_command(command, expect_string=r'[confirm]')
        try:
            # after this command, OSError is expected
            self.driver.device.send_command('\n')
            msg = 'failed to reboot'
            self.log.error(msg)
            raise RuntimeError(msg)
        except OSError:
            raise RebootException()
