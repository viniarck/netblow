CLI Workflow
============

This section gives an example of the recommended workflow to run the `eos_tests.yml` test file in the `eos_topo.yml` mentioned in :ref:`yml_files_label` section:

1. Dry run mode to verify the yml syntax:


.. code:: shell

  ❯ netblow -f topologies/eos_topo.yml -t scenarios_tests/eos_tests.yml -d
  2018-05-01 13:56:37 [MainThread] [ INFO] Dry run mode
  2018-05-01 13:56:37 [MainThread] [ INFO] Loading topology file /home/arcanjo/repos/netblow/topologies/eos_topo.yml
  2018-05-01 13:56:37 [MainThread] [ INFO] Devices in the topology ['eos1', 'eos2']
  2018-05-01 13:56:37 [MainThread] [ INFO] Loading test file /home/arcanjo/repos/netblow/scenarios_tests/eos_tests.yml
  2018-05-01 13:56:37 [MainThread] [ INFO] Waiting for async tests to finish...
  2018-05-01 13:56:37 [MainThread] [ INFO] Mock call trace:
  2018-05-01 13:56:37 [MainThread] [ INFO] call.interfaces_flap('eos1', interfaces=['Ethernet 7', 'Ethernet 8'], iterations=2)
  2018-05-01 13:56:37 [MainThread] [ INFO] call.interfaces_flap('eos1', interfaces=['Ethernet 7', 'Ethernet 8'], sync=False)
  2018-05-01 13:56:37 [MainThread] [ INFO] call.interfaces_flap('eos2', interfaces=['Ethernet 2', 'Ethernet 3'], sync=False)
  2018-05-01 13:56:37 [MainThread] [ INFO] call.interfaces_flap('eos1', duration=3, interfaces=['Ethernet 7', 'Ethernet 8'])
  2018-05-01 13:56:37 [MainThread] [ INFO] call.interfaces_flap('eos2', duration=3, interfaces=['Ethernet 2', 'Ethernet 3'])


2. Connectivity check mode:

.. code:: shell

  ❯ netblow -f topologies/eos_topo.yml -t scenarios_tests/eos_tests.yml -c
  2018-05-01 13:56:41 [MainThread] [ INFO] Loading topology file /home/arcanjo/repos/netblow/topologies/eos_topo.yml
  2018-05-01 13:56:41 [MainThread] [ INFO] Devices in the topology ['eos1', 'eos2']
  2018-05-01 13:56:41 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 13:56:41 [      eos1] [ INFO] Trying to connect on eos1...
  2018-05-01 13:56:41 [      eos2] [ INFO] Trying to connect on eos2...
  2018-05-01 13:56:44 [      eos2] [ INFO] Successfully connected on eos2
  2018-05-01 13:56:45 [      eos1] [ INFO] Successfully connected on eos1
  2018-05-01 13:56:45 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 13:56:45 [MainThread] [ INFO] Closing connections to all devices
  2018-05-01 13:56:45 [MainThread] [ INFO] Closing connections to all devices

3. Once mode:

In this case, I don't have a long lasting test, but it's also super useful to see napalm diffs:

.. code:: shell

  ❯ netblow -f topologies/eos_topo.yml -t scenarios_tests/eos_tests.yml -1
  2018-05-01 13:56:49 [MainThread] [ INFO] Loading topology file /home/arcanjo/repos/netblow/topologies/eos_topo.yml
  2018-05-01 13:56:49 [MainThread] [ INFO] Devices in the topology ['eos1', 'eos2']
  2018-05-01 13:56:49 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 13:56:49 [      eos1] [ INFO] Trying to connect on eos1...
  2018-05-01 13:56:49 [      eos2] [ INFO] Trying to connect on eos2...
  2018-05-01 13:56:51 [      eos1] [ INFO] Successfully connected on eos1
  2018-05-01 13:56:52 [      eos2] [ INFO] Successfully connected on eos2
  2018-05-01 13:56:52 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 13:56:52 [MainThread] [ INFO] Loading test file /home/arcanjo/repos/netblow/scenarios_tests/eos_tests.yml
  2018-05-01 13:56:52 [      eos1] [ INFO] Test interfaces_flap started on eos1
  2018-05-01 13:56:52 [      eos1] [ INFO]   Iteration #1/1 on eos1
  2018-05-01 13:56:52 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 13:56:59 [      eos1] [ INFO]       Diff:
  @@ -23,8 +23,10 @@
   interface Ethernet6
   !
   interface Ethernet7
  +   shutdown
   !
   interface Ethernet8
  +   shutdown
   !
   interface Ethernet9
   !
  2018-05-01 13:57:01 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  2018-05-01 13:57:09 [      eos1] [ INFO]       Diff:
  @@ -23,10 +23,8 @@
   interface Ethernet6
   !
   interface Ethernet7
  -   shutdown
   !
   interface Ethernet8
  -   shutdown
   !
   interface Ethernet9
   !
  2018-05-01 13:57:11 [      eos1] [ INFO] Test interfaces_flap started on eos1
  2018-05-01 13:57:11 [      eos2] [ INFO] Test interfaces_flap started on eos2
  2018-05-01 13:57:11 [MainThread] [ INFO] Waiting for async tests to finish...
  2018-05-01 13:57:11 [      eos1] [ INFO]   Iteration #1/1 on eos1
  2018-05-01 13:57:11 [      eos2] [ INFO]   Iteration #1/1 on eos2
  2018-05-01 13:57:11 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 13:57:11 [      eos2] [ INFO]     Shutting interfaces ['Ethernet 2', 'Ethernet 3'] down
  2018-05-01 13:57:17 [      eos1] [ INFO]       Diff:
  @@ -23,8 +23,10 @@
   interface Ethernet6
   !
   interface Ethernet7
  +   shutdown
   !
   interface Ethernet8
  +   shutdown
   !
   interface Ethernet9
   !
  2018-05-01 13:57:17 [      eos2] [ INFO]       Diff:
  @@ -13,8 +13,10 @@
   interface Ethernet1
   !
   interface Ethernet2
  +   shutdown
   !
   interface Ethernet3
  +   shutdown
   !
   interface Ethernet4
   !
  2018-05-01 13:57:20 [      eos2] [ INFO]     Bringing interfaces ['Ethernet 2', 'Ethernet 3'] up
  2018-05-01 13:57:21 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  2018-05-01 13:57:28 [      eos2] [ INFO]       Diff:
  @@ -13,10 +13,8 @@
   interface Ethernet1
   !
   interface Ethernet2
  -   shutdown
   !
   interface Ethernet3
  -   shutdown
   !
   interface Ethernet4
   !
  2018-05-01 13:57:29 [      eos1] [ INFO]       Diff:
  @@ -23,10 +23,8 @@
   interface Ethernet6
   !
   interface Ethernet7
  -   shutdown
   !
   interface Ethernet8
  -   shutdown
   !
   interface Ethernet9
   !
  2018-05-01 13:57:31 [      eos1] [ INFO] Test interfaces_flap started on eos1
  2018-05-01 13:57:31 [      eos1] [ INFO]   Iteration #1/31536000 on eos1
  2018-05-01 13:57:31 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 13:57:37 [      eos1] [ INFO]       Diff:
  @@ -23,8 +23,10 @@
   interface Ethernet6
   !
   interface Ethernet7
  +   shutdown
   !
   interface Ethernet8
  +   shutdown
   !
   interface Ethernet9
   !
  2018-05-01 13:57:39 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  2018-05-01 13:57:47 [      eos1] [ INFO]       Diff:
  @@ -23,10 +23,8 @@
   interface Ethernet6
   !
   interface Ethernet7
  -   shutdown
   !
   interface Ethernet8
  -   shutdown
   !
   interface Ethernet9
   !
  2018-05-01 13:57:49 [      eos1] [ INFO]   Duration timeout exceeded. Aborting test.
  2018-05-01 13:57:49 [      eos2] [ INFO] Test interfaces_flap started on eos2
  2018-05-01 13:57:49 [      eos2] [ INFO]   Iteration #1/31536000 on eos2
  2018-05-01 13:57:49 [      eos2] [ INFO]     Shutting interfaces ['Ethernet 2', 'Ethernet 3'] down
  2018-05-01 13:57:55 [      eos2] [ INFO]       Diff:
  @@ -13,8 +13,10 @@
   interface Ethernet1
   !
   interface Ethernet2
  +   shutdown
   !
   interface Ethernet3
  +   shutdown
   !
   interface Ethernet4
   !
  2018-05-01 13:57:58 [      eos2] [ INFO]     Bringing interfaces ['Ethernet 2', 'Ethernet 3'] up
  2018-05-01 13:58:04 [      eos2] [ INFO]       Diff:
  @@ -13,10 +13,8 @@
   interface Ethernet1
   !
   interface Ethernet2
  -   shutdown
   !
   interface Ethernet3
  -   shutdown
   !
   interface Ethernet4
   !
  2018-05-01 13:58:06 [      eos2] [ INFO]   Duration timeout exceeded. Aborting test.
  2018-05-01 13:58:06 [MainThread] [ INFO] Closing connections to all devices

4. Run the original specified tests without modifiers:


.. code:: shell

  ❯ netblow -f topologies/eos_topo.yml -t scenarios_tests/eos_tests.yml
  2018-05-01 13:58:18 [MainThread] [ INFO] Loading topology file /home/arcanjo/repos/netblow/topologies/eos_topo.yml
  2018-05-01 13:58:18 [MainThread] [ INFO] Devices in the topology ['eos1', 'eos2']
  2018-05-01 13:58:18 [MainThread] [ INFO] Trying to open connections to all devices...
  2018-05-01 13:58:18 [      eos1] [ INFO] Trying to connect on eos1...
  2018-05-01 13:58:18 [      eos2] [ INFO] Trying to connect on eos2...
  2018-05-01 13:58:21 [      eos2] [ INFO] Successfully connected on eos2
  2018-05-01 13:58:21 [      eos1] [ INFO] Successfully connected on eos1
  2018-05-01 13:58:21 [MainThread] [ INFO] All devices are CONNECTED
  2018-05-01 13:58:21 [MainThread] [ INFO] Loading test file /home/arcanjo/repos/netblow/scenarios_tests/eos_tests.yml
  2018-05-01 13:58:21 [      eos1] [ INFO] Test interfaces_flap started on eos1
  2018-05-01 13:58:21 [      eos1] [ INFO]   Iteration #1/2 on eos1
  2018-05-01 13:58:21 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 13:58:29 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  2018-05-01 13:58:35 [      eos1] [ INFO]   Iteration #2/2 on eos1
  2018-05-01 13:58:35 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 13:58:41 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  2018-05-01 13:58:49 [      eos1] [ INFO] Test interfaces_flap started on eos1
  2018-05-01 13:58:49 [      eos2] [ INFO] Test interfaces_flap started on eos2
  2018-05-01 13:58:49 [      eos1] [ INFO]   Iteration #1/1 on eos1
  2018-05-01 13:58:49 [MainThread] [ INFO] Waiting for async tests to finish...
  2018-05-01 13:58:49 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 13:58:49 [      eos2] [ INFO]   Iteration #1/1 on eos2
  2018-05-01 13:58:49 [      eos2] [ INFO]     Shutting interfaces ['Ethernet 2', 'Ethernet 3'] down
  2018-05-01 13:58:55 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  2018-05-01 13:58:55 [      eos2] [ INFO]     Bringing interfaces ['Ethernet 2', 'Ethernet 3'] up
  2018-05-01 13:59:03 [      eos1] [ INFO] Test interfaces_flap started on eos1
  2018-05-01 13:59:03 [      eos1] [ INFO]   Iteration #1/31536000 on eos1
  2018-05-01 13:59:03 [      eos1] [ INFO]     Shutting interfaces ['Ethernet 7', 'Ethernet 8'] down
  2018-05-01 13:59:09 [      eos1] [ INFO]     Bringing interfaces ['Ethernet 7', 'Ethernet 8'] up
  2018-05-01 13:59:17 [      eos1] [ INFO]   Duration timeout exceeded. Aborting test.
  2018-05-01 13:59:17 [      eos2] [ INFO] Test interfaces_flap started on eos2
  2018-05-01 13:59:17 [      eos2] [ INFO]   Iteration #1/31536000 on eos2
  2018-05-01 13:59:17 [      eos2] [ INFO]     Shutting interfaces ['Ethernet 2', 'Ethernet 3'] down
  2018-05-01 13:59:24 [      eos2] [ INFO]     Bringing interfaces ['Ethernet 2', 'Ethernet 3'] up
  2018-05-01 13:59:30 [      eos2] [ INFO]   Duration timeout exceeded. Aborting test.
  2018-05-01 13:59:30 [MainThread] [ INFO] Closing connections to all devices
