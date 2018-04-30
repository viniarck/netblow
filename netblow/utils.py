#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""utils module."""

import logging
import os

DEBUG = 'debug'
FORMAT = "%(asctime)s [%(threadName)10s] [%(levelname)5s] %(message)s"
FORMAT_DEBUG = "%(asctime)s [%(name)18s] [%(threadName)10s] [%(levelname)5s] %(message)s"  # noqa
FIELD_STYLES = {
    'programname': {
        'color': 'cyan'
    },
    'name': {
        'color': 'blue'
    },
    'levelname': {
        'color': 'white'
    },
    'asctime': {
        'color': 'magenta'
    },
    'threadName': {
        'color': 'cyan'
    }
}

LEVEL_STYLES = {
    'info': {},
    'critical': {
        'color': 'red',
    },
    'error': {
        'color': 'red',
        'bold': True
    },
    'debug': {
        'color': 'green'
    },
    'warning': {
        'color': 'yellow'
    }
}

TOPO_DIR = 'topologies'
TESTS_DIR = 'scenarios_tests'


def _str_to_level(string):
    """Convert string level to actual logging.level.

    Anything that's not debug will be converted to info level.

    :string: either 'debug' or 'info'.

    """
    if string.lower() == DEBUG:
        return logging.DEBUG
    return logging.INFO


def _create_dir(directory):
    """Create directory."""
    if not os.path.isdir(directory):
        os.mkdir(directory)


def find_file(file_name, sub_dir=None):
    """Find file under cwd, cwd/sub_dir or xdg_dir/sub_dir in this order.

    :file_name: yml file name
    :sub_dir:sub directory
    :returns: file path

    """
    cwd = os.getcwd()
    for dir_name in [
            cwd,
            os.path.join(cwd, sub_dir),
            os.path.join(_get_xdg_dir(), sub_dir)
    ]:
        try:
            f_name = os.path.join(dir_name, file_name)
            with open(f_name):
                pass
            return f_name
        except OSError:
            pass
    raise OSError("File {} couldn't be found".format(file_name))


def _get_xdg_dir():
    """Get and Initialize xdg configuration directory.

    :return: xdg_dir

    """
    xdg_dir = os.path.join(os.path.expanduser('~'), '.config', 'netblow')
    return xdg_dir


def _bootstrap_xdg_dirs():
    """Bootstrap xdg dirs."""
    xdg_dir = _get_xdg_dir()
    _create_dir(xdg_dir)
    dirs = [os.path.join(xdg_dir, TOPO_DIR), os.path.join(xdg_dir, TESTS_DIR)]
    for dir_name in dirs:
        _create_dir(dir_name)
