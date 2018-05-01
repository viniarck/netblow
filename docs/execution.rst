Execution modifiers
===================

netblow has the following execution mode modifiers, which are mutually exclusive:

Dry run
-------

Dry run is used for validating all network stress tests calls without actually connecting in the device or committing them. You certainly want to experiment with dry run first, before starting to run the actual tests. Plus, dry run is also used to validate if all kwargs are specified correctly.

Connectivity check
------------------

It's just used for validating that napalm can in fact connect with all devices in the topology. If any parameters are wrong, or authentication is not allowed you'll see errors. You probably want to perform some connectivity check when you are first building your topology.

Once
----

Once is really useful when you just want to limit the execution of all specified tests to a single iteration. Plus, when the once mode is on, it will show napalm diffs. So, once is great for the first validating that all specified tests are indeed running as expected and quickly. As soon as you have validated your tests with the once mode, you are good to go for the tests that are supposed to last long.


.. warning::

    Be warned that netblow actually commits the configuration in the network device if you are running in any mode other than dry run or connectivity check. Don't run in production, unless you know what you're doing.


.. note::

    napalm diffs are disabled in the normal testing mode by design. netblow assumes you have validated your tests with the once mode first. Also, as a result, the execution is faster, which is important if you are trying to have little delay as possible between iterations.

