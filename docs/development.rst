
Development
===========

Currently, to test the source code of netblow, the following test stages and test suites are in place:

- **linters**: flake8, pycodestyle and pydocstyle.
- **unit**: pytest. All networking I/O are mocked in the CI/CD pipeline.
- **integration**: pytest. This suite is run outside of the pipeline because it needs actual networking devices (JunOS, EOS, IOS-XR and IOS).

Since I can't run the integration test suite on travis-ci (CI/CD pipeline), I will use this section to post the results of these tests that I run locally for the record:

.. note::

  Let me know if you can host these instances publicly somewhere, just so I could have full integration with the current CI/CD and increase the test coverage.

.. note::

  I'm running virtual instances of OES, JunOS, IOS-XR and IOS-XE on qemu on Docker engine, so chances are, the performance of the output commands are probably worse that what you would have in a device running the OS natively.

Integration test results
------------------------

.. code:: shell

  ❯ pytest tests/integration -s
  ============================================================================================= test session starts ==============================================================================================
  platform linux -- Python 3.6.4, pytest-3.5.1, py-1.5.3, pluggy-0.6.0
  rootdir: /home/arcanjo/repos/netblow, inifile:
  plugins: xdist-1.22.2, forked-0.2, cov-2.5.1
  collected 17 items

  tests/integration/test_eos.py 2018-05-01 14:21:05 [MainThread] [ INFO] Devices in the topology ['eos1', 'eos2']
  2018-05-01 14:21:05 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 14:21:05 [      eos1] [ INFO] Trying to connect on eos1...
  2018-05-01 14:21:05 [      eos2] [ INFO] Trying to connect on eos2...
  2018-05-01 14:21:09 [      eos1] [ INFO] Successfully connected on eos1
  2018-05-01 14:21:09 [      eos2] [ INFO] Successfully connected on eos2
  2018-05-01 14:21:09 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 14:21:09 [      eos1] [ INFO] Test interfaces_down started on eos1
  2018-05-01 14:21:09 [      eos2] [ INFO] Test interfaces_down started on eos2
  2018-05-01 14:21:09 [MainThread] [ INFO] Waiting for async tests to finish...
  2018-05-01 14:21:09 [      eos2] [ INFO]   Iteration #1/1 on eos2
  2018-05-01 14:21:09 [      eos2] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 14:21:09 [      eos1] [ INFO]   Iteration #1/1 on eos1
  2018-05-01 14:21:09 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 14:21:17 [      eos1] [ INFO] Test interfaces_up started on eos1
  2018-05-01 14:21:17 [      eos2] [ INFO] Test interfaces_up started on eos2
  2018-05-01 14:21:17 [      eos1] [ INFO]   Iteration #1/1 on eos1
  2018-05-01 14:21:17 [MainThread] [ INFO] Waiting for async tests to finish...
  2018-05-01 14:21:17 [      eos2] [ INFO]   Iteration #1/1 on eos2
  2018-05-01 14:21:17 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  2018-05-01 14:21:17 [      eos2] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  .2018-05-01 14:21:24 [      eos1] [ INFO] Test interfaces_down started on eos1
  2018-05-01 14:21:24 [      eos1] [ INFO]   Iteration #1/1 on eos1
  2018-05-01 14:21:24 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 14:21:30 [      eos2] [ INFO] Test interfaces_down started on eos2
  2018-05-01 14:21:30 [      eos2] [ INFO]   Iteration #1/1 on eos2
  2018-05-01 14:21:30 [      eos2] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 14:21:35 [      eos1] [ INFO] Test interfaces_up started on eos1
  2018-05-01 14:21:35 [      eos1] [ INFO]   Iteration #1/1 on eos1
  2018-05-01 14:21:35 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  2018-05-01 14:21:42 [      eos2] [ INFO] Test interfaces_up started on eos2
  2018-05-01 14:21:42 [      eos2] [ INFO]   Iteration #1/1 on eos2
  2018-05-01 14:21:42 [      eos2] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  .2018-05-01 14:21:49 [MainThread] [ INFO] Devices in the topology ['eos1', 'eos2']
  2018-05-01 14:21:49 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 14:21:49 [      eos1] [ INFO] Trying to connect on eos1...
  2018-05-01 14:21:49 [      eos2] [ INFO] Trying to connect on eos2...
  2018-05-01 14:21:53 [      eos1] [ INFO] Successfully connected on eos1
  2018-05-01 14:21:53 [      eos2] [ INFO] Successfully connected on eos2
  2018-05-01 14:21:53 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 14:21:53 [      eos1] [ INFO] Test config_rollback started on eos1
  2018-05-01 14:21:53 [      eos1] [ INFO]   Iteration #1/1 on eos1
  2018-05-01 14:21:53 [      eos1] [ INFO]     Applying commands ['hostname eos1eos1'] on eos1
  2018-05-01 14:22:00 [      eos1] [ INFO]       Diff:
  @@ -3,6 +3,8 @@
   ! boot system flash:/vEOS-lab.swi
   !
   transceiver qsfp default-mode 4x10G
  +!
  +hostname eos1eos1
   !
   spanning-tree mode mstp
   !
  2018-05-01 14:22:03 [      eos1] [ INFO]     Performing rollback
  .2018-05-01 14:22:07 [      eos2] [ INFO] Test show started on eos2
  2018-05-01 14:22:07 [      eos2] [ INFO]   Iteration #1/1 on eos2
  2018-05-01 14:22:07 [      eos2] [ INFO]     Applying show commands ['show version'] on eos2
  2018-05-01 14:22:09 [      eos2] [ INFO]     show version
  Arista vEOS
  Hardware version:
  Serial number:
  System MAC address:  5254.005a.ebe5

  Software image version: 4.20.1F
  Architecture:           i386
  Internal build version: 4.20.1F-6820520.4201F
  Internal build ID:      790a11e8-5aaf-4be7-a11a-e61795d05b91

  Uptime:                 1 day, 22 hours and 25 minutes
  Total memory:           2017260 kB
  Free memory:            1038628 kB


  .2018-05-01 14:22:09 [      eos1] [ INFO] Test reboot started on eos1
  2018-05-01 14:22:09 [      eos1] [ INFO]   Iteration #1/1 on eos1
  2018-05-01 14:22:09 [      eos1] [ INFO]     Rebooting eos1
  2018-05-01 14:22:11 [      eos1] [ INFO] Trying to connect on eos1...
  2018-05-01 14:22:41 [      eos1] [ INFO] Retry #1
  2018-05-01 14:22:41 [      eos1] [ INFO] Socket error during eAPI connection: _ssl.c:761: The handshake operation timed out
  2018-05-01 14:22:41 [      eos1] [ INFO] Waiting for 30 seconds...
  2018-05-01 14:22:41 [      eos1] [ INFO] 569 seconds left before timeouting...
  2018-05-01 14:23:11 [      eos1] [ INFO] Trying to connect on eos1...
  2018-05-01 14:23:42 [      eos1] [ INFO] Retry #2
  2018-05-01 14:23:42 [      eos1] [ INFO] Socket error during eAPI connection: _ssl.c:761: The handshake operation timed out
  2018-05-01 14:23:42 [      eos1] [ INFO] Waiting for 30 seconds...
  2018-05-01 14:23:42 [      eos1] [ INFO] 509 seconds left before timeouting...
  2018-05-01 14:24:12 [      eos1] [ INFO] Trying to connect on eos1...
  2018-05-01 14:24:36 [      eos1] [ INFO] Successfully connected on eos1
  .
  tests/integration/test_ios.py 2018-05-01 14:24:36 [MainThread] [ INFO] Devices in the topology ['ios1']
  2018-05-01 14:24:36 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 14:24:36 [      ios1] [ INFO] Trying to connect on ios1...
  2018-05-01 14:24:44 [      ios1] [ INFO] Successfully connected on ios1
  2018-05-01 14:24:44 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 14:24:44 [      ios1] [ INFO] Test interfaces_down started on ios1
  2018-05-01 14:24:44 [      ios1] [ INFO]   Iteration #1/1 on ios1
  2018-05-01 14:24:44 [      ios1] [ INFO]     Shutting interfaces ['GigabitEthernet12', 'GigabitEthernet13'] down
  2018-05-01 14:26:21 [      ios1] [ INFO] Test interfaces_up started on ios1
  2018-05-01 14:26:21 [      ios1] [ INFO]   Iteration #1/1 on ios1
  2018-05-01 14:26:21 [      ios1] [ INFO]     Bringing interfaces ['GigabitEthernet12', 'GigabitEthernet13'] up
  2018-05-01 14:26:26 [      ios1] [ERROR] SCP file transfers are not enabled. Configure 'ip scp server enable' on the device.
  2018-05-01 14:26:26 [      ios1] [ INFO] Trying to connect on ios1...
  2018-05-01 14:26:33 [      ios1] [ INFO] Successfully connected on ios1
  .2018-05-01 14:26:33 [MainThread] [ INFO] Devices in the topology ['ios1']
  2018-05-01 14:26:33 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 14:26:33 [      ios1] [ INFO] Trying to connect on ios1...
  2018-05-01 14:26:40 [      ios1] [ INFO] Successfully connected on ios1
  2018-05-01 14:26:40 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 14:26:40 [      ios1] [ INFO] Test config_rollback started on ios1
  2018-05-01 14:26:40 [      ios1] [ INFO]   Iteration #1/1 on ios1
  2018-05-01 14:26:40 [      ios1] [ INFO]     Applying commands ['router bgp 65000'] on ios1
  2018-05-01 14:26:51 [      ios1] [ INFO]       Diff:
  +router bgp 65000
  2018-05-01 14:28:18 [      ios1] [ INFO]     Performing rollback
  Exception in thread ios1:
  Traceback (most recent call last):
    File "/usr/lib64/python3.6/threading.py", line 916, in _bootstrap_inner
      self.run()
    File "/usr/lib64/python3.6/threading.py", line 864, in run
      self._target(*self._args, **self._kwargs)
    File "/home/arcanjo/repos/netblow/netblow/netblow.py", line 590, in blow_thread
      **kwargs)
    File "/home/arcanjo/repos/netblow/netblow/netblow.py", line 785, in config_rollback
      dut_driver.rollback()
    File "/home/arcanjo/repos/netblow/.direnv/python-3.6.4/lib/python3.6/site-packages/napalm/ios/ios.py", line 471, in rollback
      self.device.send_command_expect("write mem")
    File "/home/arcanjo/repos/netblow/.direnv/python-3.6.4/lib/python3.6/site-packages/netmiko/base_connection.py", line 1069, in send_command_expect
      return self.send_command(*args, **kwargs)
    File "/home/arcanjo/repos/netblow/.direnv/python-3.6.4/lib/python3.6/site-packages/netmiko/base_connection.py", line 1051, in send_command
      search_pattern))
  OSError: Search pattern never detected in send_command_expect: xt\ force

  .2018-05-01 14:29:49 [      ios1] [ INFO] Test show started on ios1
  2018-05-01 14:29:49 [      ios1] [ INFO]   Iteration #1/1 on ios1
  2018-05-01 14:29:49 [      ios1] [ INFO]     Applying show commands ['show version'] on ios1
  2018-05-01 14:29:50 [      ios1] [ INFO]     show version
  Cisco IOS XE Software, Version 16.06.02
  Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.2, RELEASE SOFTWARE (fc2)
  Technical Support: http://www.cisco.com/techsupport
  Copyright (c) 1986-2017 by Cisco Systems, Inc.
  Compiled Wed 01-Nov-17 07:24 by mcpre


  Cisco IOS-XE software, Copyright (c) 2005-2017 by cisco Systems, Inc.
  All rights reserved.  Certain components of Cisco IOS-XE software are
  licensed under the GNU General Public License ("GPL") Version 2.0.  The
  software code licensed under GPL Version 2.0 is free software that comes
  with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
  GPL code under the terms of GPL Version 2.0.  For more details, see the
  documentation or "License Notice" file accompanying the IOS-XE software,
  or the applicable URL provided on the flyer accompanying the IOS-XE
  software.


  ROM: IOS-XE ROMMON

  csr1000v uptime is 1 day, 22 hours, 31 minutes
  Uptime for this control processor is 1 day, 22 hours, 32 minutes
  System returned to ROM by reload
  System image file is "bootflash:packages.conf"
  Last reload reason: Reload Command



  This product contains cryptographic features and is subject to United
  States and local country laws governing import, export, transfer and
  use. Delivery of Cisco cryptographic products does not imply
  third-party authority to import, export, distribute or use encryption.
  Importers, exporters, distributors and users are responsible for
  compliance with U.S. and local country laws. By using this product you
  agree to comply with applicable laws and regulations. If you are unable
  to comply with U.S. and local laws, return this product immediately.

  A summary of U.S. laws governing Cisco cryptographic products may be found at:
  http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

  If you require further assistance please contact us by sending email to
  export@cisco.com.

  License Level: ax
  License Type: Default. No valid license found.
  Next reload license Level: ax

  cisco CSR1000V (VXE) processor (revision VXE) with 2190795K/3075K bytes of memory.
  Processor board ID 9CT15UOLWFI
  10 Gigabit Ethernet interfaces
  32768K bytes of non-volatile configuration memory.
  3984840K bytes of physical memory.
  7774207K bytes of virtual hard disk at bootflash:.
  0K bytes of WebUI ODM Files at webui:.

  Configuration register is 0x2102
  .2018-05-01 14:29:50 [      ios1] [ INFO] Test reboot started on ios1
  2018-05-01 14:29:50 [      ios1] [ INFO]   Iteration #1/1 on ios1
  2018-05-01 14:29:50 [      ios1] [ INFO]     Rebooting ios1
  2018-05-01 14:31:21 [      ios1] [ INFO] Trying to connect on ios1...
  2018-05-01 14:31:36 [      ios1] [ INFO] Retry #1
  2018-05-01 14:31:36 [      ios1] [ INFO] Error reading SSH protocol banner
  2018-05-01 14:31:36 [      ios1] [ INFO] Waiting for 30 seconds...
  2018-05-01 14:31:36 [      ios1] [ INFO] 584 seconds left before timeouting...
  2018-05-01 14:32:06 [      ios1] [ INFO] Trying to connect on ios1...
  2018-05-01 14:32:22 [      ios1] [ INFO] Retry #2
  2018-05-01 14:32:22 [      ios1] [ INFO] Error reading SSH protocol banner
  2018-05-01 14:32:22 [      ios1] [ INFO] Waiting for 30 seconds...
  2018-05-01 14:32:22 [      ios1] [ INFO] 539 seconds left before timeouting...
  2018-05-01 14:32:52 [      ios1] [ INFO] Trying to connect on ios1...
  2018-05-01 14:32:59 [      ios1] [ INFO] Successfully connected on ios1
  .
  tests/integration/test_iosxr.py 2018-05-01 14:32:59 [MainThread] [ INFO] Devices in the topology ['iosxr1']
  2018-05-01 14:32:59 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 14:32:59 [    iosxr1] [ INFO] Trying to connect on iosxr1...
  2018-05-01 14:33:10 [    iosxr1] [ INFO] Successfully connected on iosxr1
  2018-05-01 14:33:10 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 14:33:10 [    iosxr1] [ INFO] Test interfaces_down started on iosxr1
  2018-05-01 14:33:10 [    iosxr1] [ INFO]   Iteration #1/1 on iosxr1
  2018-05-01 14:33:10 [    iosxr1] [ INFO]     Shutting interfaces ['GigabitEthernet0/0/0/1', 'GigabitEthernet0/0/0/2'] down
  2018-05-01 14:33:13 [    iosxr1] [ INFO] Test interfaces_up started on iosxr1
  2018-05-01 14:33:13 [    iosxr1] [ INFO]   Iteration #1/1 on iosxr1
  2018-05-01 14:33:13 [    iosxr1] [ INFO]     Bringing interfaces ['GigabitEthernet0/0/0/1', 'GigabitEthernet0/0/0/2'] up
  .2018-05-01 14:33:15 [MainThread] [ INFO] Devices in the topology ['iosxr1']
  2018-05-01 14:33:15 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 14:33:15 [    iosxr1] [ INFO] Trying to connect on iosxr1...
  2018-05-01 14:33:27 [    iosxr1] [ INFO] Successfully connected on iosxr1
  2018-05-01 14:33:27 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 14:33:27 [    iosxr1] [ INFO] Test config_rollback started on iosxr1
  2018-05-01 14:33:27 [    iosxr1] [ INFO]   Iteration #1/1 on iosxr1
  2018-05-01 14:33:27 [    iosxr1] [ INFO]     Applying commands ['router bgp 65001'] on iosxr1
  2018-05-01 14:33:29 [    iosxr1] [ INFO]       Diff:
  ---
  +++
  @@ -385,6 +385,8 @@
   interface GigabitEthernet0/0/0/127
    shutdown
   !
  +router bgp 65001
  +!
   xml agent tty
   !
   netconf-yang agent
  2018-05-01 14:33:31 [    iosxr1] [ INFO]     Performing rollback
  .2018-05-01 14:33:31 [    iosxr1] [ INFO] Test show started on iosxr1
  2018-05-01 14:33:31 [    iosxr1] [ INFO]   Iteration #1/1 on iosxr1
  2018-05-01 14:33:31 [    iosxr1] [ INFO]     Applying show commands ['show version'] on iosxr1
  2018-05-01 14:33:32 [    iosxr1] [ INFO]     show version
  Cisco IOS XR Software, Version 6.0.1[Default]
  Copyright (c) 2016 by Cisco Systems, Inc.

  ROM: GRUB, Version 1.99(0), DEV RELEASE

  ios uptime is 1 day, 22 hours, 36 minutes
  System image file is "bootflash:disk0/xrvr-os-mbi-6.0.1/mbixrvr-rp.vm"

  cisco IOS XRv Series (Pentium Celeron Stepping 3) processor with 3145215K bytes of memory.
  Pentium Celeron Stepping 3 processor at 2607MHz, Revision 2.174
  IOS XRv Chassis

  128 GigabitEthernet
  1 Management Ethernet
  97070k bytes of non-volatile configuration memory.
  866M bytes of hard disk.
  2321392k bytes of disk0: (Sector size 512 bytes).

  Configuration register on node 0/0/CPU0 is 0x2102
  Boot device on node 0/0/CPU0 is disk0:
  Package active on node 0/0/CPU0:
  iosxr-infra, V 6.0.1[Default], Cisco Systems, at disk0:iosxr-infra-6.0.1
      Built on Mon May  9 12:06:47 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  iosxr-fwding, V 6.0.1[Default], Cisco Systems, at disk0:iosxr-fwding-6.0.1
      Built on Mon May  9 12:06:47 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  iosxr-routing, V 6.0.1[Default], Cisco Systems, at disk0:iosxr-routing-6.0.1
      Built on Mon May  9 12:06:47 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  iosxr-ce, V 6.0.1[Default], Cisco Systems, at disk0:iosxr-ce-6.0.1
      Built on Mon May  9 12:06:48 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  xrvr-os-mbi, V 6.0.1[Default], Cisco Systems, at disk0:xrvr-os-mbi-6.0.1
      Built on Mon May  9 12:07:35 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  xrvr-base, V 6.0.1[Default], Cisco Systems, at disk0:xrvr-base-6.0.1
      Built on Mon May  9 12:06:47 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  xrvr-fwding, V 6.0.1[Default], Cisco Systems, at disk0:xrvr-fwding-6.0.1
      Built on Mon May  9 12:06:48 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  xrvr-mgbl-x, V 6.0.1[Default], Cisco Systems, at disk0:xrvr-mgbl-x-6.0.1
      Built on Mon May  9 12:06:55 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  iosxr-mpls, V 6.0.1[Default], Cisco Systems, at disk0:iosxr-mpls-6.0.1
      Built on Mon May  9 12:06:47 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  iosxr-mgbl, V 6.0.1[Default], Cisco Systems, at disk0:iosxr-mgbl-6.0.1
      Built on Mon May  9 12:06:47 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  iosxr-mcast, V 6.0.1[Default], Cisco Systems, at disk0:iosxr-mcast-6.0.1
      Built on Mon May  9 12:06:48 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  xrvr-mcast-supp, V 6.0.1[Default], Cisco Systems, at disk0:xrvr-mcast-supp-6.0.1
      Built on Mon May  9 12:06:48 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  iosxr-bng, V 6.0.1[Default], Cisco Systems, at disk0:iosxr-bng-6.0.1
      Built on Mon May  9 12:06:45 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  xrvr-bng-supp, V 6.0.1[Default], Cisco Systems, at disk0:xrvr-bng-supp-6.0.1
      Built on Mon May  9 12:06:45 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  iosxr-security, V 6.0.1[Default], Cisco Systems, at disk0:iosxr-security-6.0.1
      Built on Mon May  9 12:06:39 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie

  xrvr-fullk9-x, V 6.0.1[Default], Cisco Systems, at disk0:xrvr-fullk9-x-6.0.1
      Built on Mon May  9 12:07:39 UTC 2016
      By iox-lnx-003 in /auto/srcarchive12/production/6.0.1/xrvr/workspace for pie
  .2018-05-01 14:33:32 [    iosxr1] [ INFO] Test reboot started on iosxr1
  2018-05-01 14:33:32 [    iosxr1] [ INFO]   Iteration #1/1 on iosxr1
  2018-05-01 14:33:32 [    iosxr1] [ INFO]     Rebooting iosxr1
  2018-05-01 14:34:07 [    iosxr1] [ INFO] Trying to connect on iosxr1...
  2018-05-01 14:34:19 [    iosxr1] [ INFO] Successfully connected on iosxr1
  .
  tests/integration/test_junos.py 2018-05-01 14:34:19 [MainThread] [ INFO] Devices in the topology ['junos1']
  2018-05-01 14:34:19 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 14:34:19 [    junos1] [ INFO] Trying to connect on junos1...
  2018-05-01 14:34:21 [    junos1] [ INFO] Successfully connected on junos1
  2018-05-01 14:34:21 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 14:34:21 [    junos1] [ INFO] Test interfaces_down started on junos1
  2018-05-01 14:34:21 [    junos1] [ INFO]   Iteration #1/1 on junos1
  2018-05-01 14:34:21 [    junos1] [ INFO]     Shutting interfaces ['ge-0/0/1', 'ge-0/0/2'] down
  2018-05-01 14:34:24 [    junos1] [ INFO] Test interfaces_up started on junos1
  2018-05-01 14:34:24 [    junos1] [ INFO]   Iteration #1/1 on junos1
  2018-05-01 14:34:24 [    junos1] [ INFO]     Bringing interfaces ['ge-0/0/1', 'ge-0/0/2'] up
  2018-05-01 14:34:26 [    junos1] [ INFO] Test interfaces_flap started on junos1
  2018-05-01 14:34:26 [    junos1] [ INFO]   Iteration #1/1 on junos1
  2018-05-01 14:34:26 [    junos1] [ INFO]     Shutting interfaces ['ge-0/0/1', 'ge-0/0/2'] down
  2018-05-01 14:34:28 [    junos1] [ INFO]     Bringing interfaces ['ge-0/0/1', 'ge-0/0/2'] up
  .2018-05-01 14:34:30 [MainThread] [ INFO] Devices in the topology ['junos1']
  2018-05-01 14:34:30 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 14:34:30 [    junos1] [ INFO] Trying to connect on junos1...
  2018-05-01 14:34:33 [    junos1] [ INFO] Successfully connected on junos1
  2018-05-01 14:34:33 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 14:34:33 [    junos1] [ INFO] Test config_rollback started on junos1
  2018-05-01 14:34:33 [    junos1] [ INFO]   Iteration #1/1 on junos1
  2018-05-01 14:34:33 [    junos1] [ INFO]     Applying commands ['set system domain-name lab.com', 'set system ntp peer 10.10.10.10'] on junos1
  2018-05-01 14:34:34 [    junos1] [ INFO]       Diff:
  [edit system]
  +  domain-name lab.com;
  +  ntp {
  +      peer 10.10.10.10;
  +  }
  2018-05-01 14:34:35 [    junos1] [ INFO]     Performing rollback
  .2018-05-01 14:34:37 [    junos1] [ INFO] Test show started on junos1
  2018-05-01 14:34:37 [    junos1] [ INFO]   Iteration #1/1 on junos1
  2018-05-01 14:34:37 [    junos1] [ INFO]     Applying show commands ['show interfaces terse', 'show version'] on junos1
  2018-05-01 14:34:38 [    junos1] [ INFO]     show interfaces terse

  Interface               Admin Link Proto    Local                 Remote
  ge-0/0/0                up    up
  lc-0/0/0                up    up
  lc-0/0/0.32769          up    up   vpls
  pfe-0/0/0               up    up
  pfe-0/0/0.16383         up    up   inet
                                     inet6
  pfh-0/0/0               up    up
  pfh-0/0/0.16383         up    up   inet
  pfh-0/0/0.16384         up    up   inet
  ge-0/0/1                up    up
  ge-0/0/2                up    up
  ge-0/0/3                up    up
  ge-0/0/4                up    up
  ge-0/0/5                up    up
  ge-0/0/6                up    up
  ge-0/0/7                up    up
  ge-0/0/8                up    up
  ge-0/0/9                up    up
  ge-0/0/10               up    up
  ge-0/0/11               up    up
  ge-0/0/12               up    up
  ge-0/0/13               up    up
  ge-0/0/14               up    up
  ge-0/0/15               up    up
  ge-0/0/16               up    up
  ge-0/0/17               up    up
  ge-0/0/18               up    up
  ge-0/0/19               up    up
  ge-0/0/20               up    up
  ge-0/0/21               up    up
  ge-0/0/22               up    up
  ge-0/0/23               up    up
  ge-0/0/24               up    up
  ge-0/0/25               up    up
  ge-0/0/26               up    up
  ge-0/0/27               up    up
  ge-0/0/28               up    up
  ge-0/0/29               up    up
  ge-0/0/30               up    up
  ge-0/0/31               up    up
  ge-0/0/32               up    up
  ge-0/0/33               up    up
  ge-0/0/34               up    up
  ge-0/0/35               up    up
  ge-0/0/36               up    up
  ge-0/0/37               up    up
  ge-0/0/38               up    up
  ge-0/0/39               up    up
  ge-0/0/40               up    up
  ge-0/0/41               up    up
  ge-0/0/42               up    up
  ge-0/0/43               up    up
  ge-0/0/44               up    up
  ge-0/0/45               up    up
  ge-0/0/46               up    up
  ge-0/0/47               up    up
  ge-0/0/48               up    up
  ge-0/0/49               up    up
  ge-0/0/50               up    up
  ge-0/0/51               up    up
  ge-0/0/52               up    up
  ge-0/0/53               up    up
  ge-0/0/54               up    up
  ge-0/0/55               up    up
  ge-0/0/56               up    up
  ge-0/0/57               up    up
  ge-0/0/58               up    up
  ge-0/0/59               up    up
  ge-0/0/60               up    up
  ge-0/0/61               up    up
  ge-0/0/62               up    up
  ge-0/0/63               up    up
  ge-0/0/64               up    up
  ge-0/0/65               up    up
  ge-0/0/66               up    up
  ge-0/0/67               up    up
  ge-0/0/68               up    up
  ge-0/0/69               up    up
  ge-0/0/70               up    up
  ge-0/0/71               up    up
  ge-0/0/72               up    up
  ge-0/0/73               up    up
  ge-0/0/74               up    up
  ge-0/0/75               up    up
  ge-0/0/76               up    up
  ge-0/0/77               up    up
  ge-0/0/78               up    up
  ge-0/0/79               up    up
  ge-0/0/80               up    up
  ge-0/0/81               up    up
  ge-0/0/82               up    up
  ge-0/0/83               up    up
  ge-0/0/84               up    up
  ge-0/0/85               up    up
  ge-0/0/86               up    up
  ge-0/0/87               up    up
  ge-0/0/88               up    up
  ge-0/0/89               up    up
  ge-0/0/90               up    up
  ge-0/0/91               up    up
  ge-0/0/92               up    up
  ge-0/0/93               up    up
  ge-0/0/94               up    up
  cbp0                    up    up
  demux0                  up    up
  dsc                     up    up
  em1                     up    up
  em1.0                   up    up   inet     10.0.0.4/8
                                              128.0.0.1/2
                                              128.0.0.4/2
                                     inet6    fe80::5254:ff:fe55:5801/64
                                              fec0::a:0:0:4/64
                                     tnp      0x4
  esi                     up    up
  fxp0                    up    up
  fxp0.0                  up    up   inet     10.0.0.15/24
  gre                     up    up
  ipip                    up    up
  irb                     up    up
  jsrv                    up    up
  jsrv.1                  up    up   inet     128.0.0.127/2
  lo0                     up    up
  lo0.16384               up    up   inet     127.0.0.1           --> 0/0
  lo0.16385               up    up   inet
  lsi                     up    up
  mtun                    up    up
  pimd                    up    up
  pime                    up    up
  pip0                    up    up
  pp0                     up    up
  rbeb                    up    up
  tap                     up    up
  vtep                    up    up

  2018-05-01 14:34:38 [    junos1] [ INFO]     show version

  Model: vmx
  Junos: 17.2R1.13
  JUNOS OS Kernel 64-bit  [20170523.350481_builder_stable_10]
  JUNOS OS libs [20170523.350481_builder_stable_10]
  JUNOS OS runtime [20170523.350481_builder_stable_10]
  JUNOS OS time zone information [20170523.350481_builder_stable_10]
  JUNOS network stack and utilities [20170601.185252_builder_junos_172_r1]
  JUNOS modules [20170601.185252_builder_junos_172_r1]
  JUNOS mx modules [20170601.185252_builder_junos_172_r1]
  JUNOS libs [20170601.185252_builder_junos_172_r1]
  JUNOS OS libs compat32 [20170523.350481_builder_stable_10]
  JUNOS OS 32-bit compatibility [20170523.350481_builder_stable_10]
  JUNOS libs compat32 [20170601.185252_builder_junos_172_r1]
  JUNOS runtime [20170601.185252_builder_junos_172_r1]
  JUNOS Packet Forwarding Engine Simulation Package [20170601.185252_builder_junos_172_r1]
  JUNOS py extensions [20170601.185252_builder_junos_172_r1]
  JUNOS py base [20170601.185252_builder_junos_172_r1]
  JUNOS OS vmguest [20170523.350481_builder_stable_10]
  JUNOS OS crypto [20170523.350481_builder_stable_10]
  JUNOS mx libs compat32 [20170601.185252_builder_junos_172_r1]
  JUNOS mx runtime [20170601.185252_builder_junos_172_r1]
  JUNOS common platform support [20170601.185252_builder_junos_172_r1]
  JUNOS mx libs [20170601.185252_builder_junos_172_r1]
  JUNOS mtx Data Plane Crypto Support [20170601.185252_builder_junos_172_r1]
  JUNOS daemons [20170601.185252_builder_junos_172_r1]
  JUNOS mx daemons [20170601.185252_builder_junos_172_r1]
  JUNOS Services URL Filter package [20170601.185252_builder_junos_172_r1]
  JUNOS Services TLB Service PIC package [20170601.185252_builder_junos_172_r1]
  JUNOS Services SSL [20170601.185252_builder_junos_172_r1]
  JUNOS Services Stateful Firewall [20170601.185252_builder_junos_172_r1]
  JUNOS Services RPM [20170601.185252_builder_junos_172_r1]
  JUNOS Services PTSP Container package [20170601.185252_builder_junos_172_r1]
  JUNOS Services PCEF package [20170601.185252_builder_junos_172_r1]
  JUNOS Services NAT [20170601.185252_builder_junos_172_r1]
  JUNOS Services Mobile Subscriber Service Container package [20170601.185252_builder_junos_172_r1]
  JUNOS Services MobileNext Software package [20170601.185252_builder_junos_172_r1]
  JUNOS Services Logging Report Framework package [20170601.185252_builder_junos_172_r1]
  JUNOS Services LL-PDF Container package [20170601.185252_builder_junos_172_r1]
  JUNOS Services Jflow Container package [20170601.185252_builder_junos_172_r1]
  JUNOS Services Deep Packet Inspection package [20170601.185252_builder_junos_172_r1]
  JUNOS Services IPSec [20170601.185252_builder_junos_172_r1]
  JUNOS Services IDS [20170601.185252_builder_junos_172_r1]
  JUNOS IDP Services [20170601.185252_builder_junos_172_r1]
  JUNOS Services HTTP Content Management package [20170601.185252_builder_junos_172_r1]
  JUNOS Services Crypto [20170601.185252_builder_junos_172_r1]
  JUNOS Services Captive Portal and Content Delivery Container package [20170601.185252_builder_junos_172_r1]
  JUNOS Services COS [20170601.185252_builder_junos_172_r1]
  JUNOS AppId Services [20170601.185252_builder_junos_172_r1]
  JUNOS Services Application Level Gateways [20170601.185252_builder_junos_172_r1]
  JUNOS Services AACL Container package [20170601.185252_builder_junos_172_r1]
  JUNOS Extension Toolkit [20170601.185252_builder_junos_172_r1]
  JUNOS jfirmware [20170601.185252_builder_junos_172_r1]
  JUNOS Online Documentation [20170601.185252_builder_junos_172_r1]

  .2018-05-01 14:34:38 [    junos1] [ INFO] Test reboot started on junos1
  2018-05-01 14:34:38 [    junos1] [ INFO]   Iteration #1/1 on junos1
  2018-05-01 14:34:38 [    junos1] [ INFO]     Rebooting junos1
  2018-05-01 14:34:39 [    junos1] [ INFO] Trying to connect on junos1...
  2018-05-01 14:34:39 [    junos1] [ INFO] Retry #1
  2018-05-01 14:34:39 [    junos1] [ INFO] ConnectRefusedError(labhost)
  2018-05-01 14:34:39 [    junos1] [ INFO] Waiting for 30 seconds...
  2018-05-01 14:34:39 [    junos1] [ INFO] 599 seconds left before timeouting...
  2018-05-01 14:35:09 [    junos1] [ INFO] Trying to connect on junos1...
  2018-05-01 14:35:24 [    junos1] [ INFO] Retry #2
  2018-05-01 14:35:24 [    junos1] [ INFO] ConnectError(host: labhost, msg: Negotiation failed)
  2018-05-01 14:35:24 [    junos1] [ INFO] Waiting for 30 seconds...
  2018-05-01 14:35:24 [    junos1] [ INFO] 554 seconds left before timeouting...
  2018-05-01 14:35:54 [    junos1] [ INFO] Trying to connect on junos1...
  2018-05-01 14:36:09 [    junos1] [ INFO] Retry #3
  2018-05-01 14:36:09 [    junos1] [ INFO] ConnectError(host: labhost, msg: Negotiation failed)
  2018-05-01 14:36:09 [    junos1] [ INFO] Waiting for 30 seconds...
  2018-05-01 14:36:09 [    junos1] [ INFO] 509 seconds left before timeouting...
  2018-05-01 14:36:39 [    junos1] [ INFO] Trying to connect on junos1...
  2018-05-01 14:36:42 [    junos1] [ INFO] Successfully connected on junos1
  .

  ========================================================================================= 17 passed in 937.32 seconds =========================================================================================
  2018-05-01 14:36:42 [MainThread] [ INFO] Closing connections to all devices
  2018-05-01 14:36:42 [MainThread] [ INFO] Closing connections to all devices
  2018-05-01 14:36:42 [MainThread] [ INFO] Closing connections to all devices
  2018-05-01 14:36:42 [MainThread] [ INFO] Closing connections to all devices
  2018-05-01 14:36:42 [MainThread] [ INFO] Closing connections to all devices
  2018-05-01 14:36:42 [MainThread] [ INFO] Closing connections to all devices
  2018-05-01 14:36:46 [MainThread] [ INFO] Closing connections to all devices
  2018-05-01 14:36:46 [MainThread] [ INFO] Closing connections to all devices
