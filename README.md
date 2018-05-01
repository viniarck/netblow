[![Build Status](https://travis-ci.org/viniciusarcanjo/netblow.svg?branch=master)](https://travis-ci.org/viniciusarcanjo/netblow)

# netblow

Vendor agnostic network testing framework to stress network failures.

## Why?

- You want to stress network failures to validate if the network control plane is converging as expected.
- Maybe you've just got a bleeding-edge control plane software update that hasn't been extensively tested yet :)
- You'd like to make sure that control plane changes are first validated in a CI/CD testing environment for a couple of hours or even days, before pushing to production.

## Features

- netblow exposes functions to stress the control plane and network failures, such as `interfaces_down`, `interfaces_up`, `interfaces_flap`, `reboot`, and `config_rollback`.
- These functions have a common set of arguments, which simplifies the business logic of your tests.
- You can either write your tests directly in Python or in a yml file.
- Tests can be run either asynchronously or synchronously in multiple devices.
- Devices re-connections are handled automatically.
- Data plane validation with salt minions (next release).
- Memory leak detection (next release).

## Installation

```
pip3 install netblow --user
```

## Docs

Visit [ReadTheDocs](https://netblow.readthedocs.io/en/latest/), for more information about network topologies, installation options, usage, code snippets and examples.

## Roadmap

[Upcoming features and enhancements.](https://github.com/viniciusarcanjo/netblow/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)

## Contributing

I am looking for users and contributors, [reach me out](https://twitter.com/forwardingflows) if you're interested.

### Project testing

The following test stages and suites are in place:

- **linters**: flake8, pycodestyle and pydocstyle.
- **unit**: pytest. All networking I/O are mocked in the CI/CD pipeline.
- **integration**: pytest. This suite is run outside of the CI/CD pipeline because it needs actual networking devices (JunOS, EOS, IOS-XR and IOS).

