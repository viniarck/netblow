#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http
import napalm
from netblow.exceptions import RebootException
import pyeapi



class EOSDriver(object):
    """Monkey patch EOSDriver."""

    def __init__(self, driver):
        """Constructor.

        :driver: napalm driver

        """
        self.driver = driver

        self.driver.interfaces_down = self.interfaces_down.__get__(
            self.driver, napalm.eos.eos.EOSDriver)
        self.driver.interfaces_up = self.interfaces_up.__get__(
            self.driver, napalm.eos.eos.EOSDriver)
        self.driver.reboot = self.reboot.__get__(self.driver,
                                                 napalm.eos.eos.EOSDriver)

    def interfaces_down(self, interfaces):
        """Shut interfaces down.

        :interfaces: list of interfaces

        """
        commands = []
        for interface in interfaces:
            commands.append('interface {}'.format(interface))
            commands.append('shutdown')
        self.driver.load_merge_candidate(config=commands)

    def interfaces_up(self, interfaces):
        """Bring interfaces up.

        :interfaces: list of interfaces

        """
        commands = []
        for interface in interfaces:
            commands.append('interface {}'.format(interface))
            commands.append('no shutdown')
        self.driver.load_merge_candidate(config=commands)

    def reboot(self, optional_args=None):
        """Reboot.

        :optional_args:
        {
            'force': True, # to force rebooting.
        }

        Raises exceptions.RebootException when it succeeds.

        """
        commands = []
        if not optional_args:
            commands.append('reload now')
        else:
            if optional_args.get('force'):
                commands.append('reload now force')
        try:
            self.driver.cli(commands)
        except (http.client.HTTPException, http.client.IncompleteRead,
                pyeapi.eapilib.ConnectionError,
                napalm.base.exceptions.CommandErrorException):
            raise RebootException()
