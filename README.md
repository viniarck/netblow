[![pipeline status](https://gitlab.com/viniarck/netblow/badges/master/pipeline.svg)](https://gitlab.com/viniarck/netblow/commits/master) [![Documentation Status](https://readthedocs.org/projects/netblow/badge/?version=latest)](http://netblow.readthedocs.io/en/latest/?badge=latest) [![PyPI](https://img.shields.io/pypi/v/netblow.svg)](https://pypi.python.org/pypi/netblow) [![PyPI Versions](https://img.shields.io/pypi/pyversions/netblow.svg)](https://pypi.python.org/pypi/netblow)

# netblow

Vendor agnostic network testing framework to stress network failures.

![netblow arch](docs/images/arch_topo.png?raw=true "netblow architecture")

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

## Installation

```
pip3 install netblow --user
```

## Docs

Visit [ReadTheDocs](https://netblow.readthedocs.io/en/latest/), knock yourself out.

## Roadmap

[Upcoming features and enhancements.](https://github.com/viniarck/netblow/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)

- Data plane validation with salt minions.
- Memory leak detection.

## Contributing

I am looking for users and contributors, [reach me out](https://twitter.com/viniarck) if you're interested.
