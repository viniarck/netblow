#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""netblow exceptions."""

from napalm.base.exceptions import NapalmException


class MaxReconnectionRetries(NapalmException):
    """Maximum number of connection retries reached."""

    def __init__(self, msg='Maximum number of retries reached'):
        """Constructor."""
        super().__init__(msg)


class RebootException(NapalmException):
    """Reboot Exception."""

    def __init__(self, msg='Reboot Exception'):
        """Concstructor."""
        super().__init__(msg)
