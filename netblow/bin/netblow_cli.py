#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""netblow_cli module."""
import argparse
from netblow.netblow import NetBlow
from netblow.version import __version__


def main():
    """Entry function."""
    parser = argparse.ArgumentParser(
        description="netblow. Vendor agnostic network testing framework to stress network failures."  # noqa
    )
    # to add required args.
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')

    m_group = optional.add_mutually_exclusive_group()
    m_group.add_argument(
        '-d',
        '--dryrun',
        default=False,
        action='store_true',
        help="show tests calls, won't connect to any devices")
    m_group.add_argument(
        '-c',
        '--concheck',
        default=False,
        action='store_true',
        help='check connectivity with all devices in the topology')
    m_group.add_argument(
        '-1',
        '--once',
        default=False,
        action='store_true',
        help="iterates only once and perfom napalm diffs")
    parser.add_argument(
        '-l',
        '--level',
        choices=['info', 'debug'],
        default='info',
        help='logging verbosity level (default: info)')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='{}'.format(__version__),
        help='show version')
    required.add_argument(
        '-f', '--topology', help='topology yml file')
    required.add_argument(
        '-t', '--tests', help='tests yml file')
    parser._action_groups.append(optional)
    args = parser.parse_args()

    if not args.topology:
        parser.error('You have to specify the topology yml file with -f')
    if not args.tests:
        if args.once or not args.dryrun and not args.concheck:
            parser.error('You have to specify the tests yml file with -t')
    NetBlow(
        topo_file=args.topology,
        test_file=args.tests,
        dry_run=args.dryrun,
        enable_salt=False,
        iter_once=args.once,
        auto_open=True,
        auto_test=True,
        con_check=args.concheck,
        level=args.level)


if __name__ == "__main__":
    main()
