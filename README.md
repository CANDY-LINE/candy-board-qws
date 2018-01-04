# candy-board-qws

[![GitHub release](https://img.shields.io/github/release/CANDY-LINE/candy-board-qws.svg)](https://github.com/CANDY-LINE/candy-board-qws/releases/latest)
[![Build Status](https://travis-ci.org/CANDY-LINE/candy-board-qws.svg?branch=master)](https://travis-ci.org/CANDY-LINE/candy-board-qws)
[![License ASL 2.0](https://img.shields.io/github/license/CANDY-LINE/candy-board-qws.svg)](https://opensource.org/licenses/Apache-2.0)

Base CANDY LINE boards service for Quectel Wireless Solutions Modules

## pip Installation

```
$ pip install candy-board-qws
```

## pip Uninstallation

```
$ pip candy-board-qws
```

## Development

### Prerequisites

 * [pandoc](http://pandoc.org)
 * [pypandoc](https://pypi.python.org/pypi/pypandoc/1.2.0)

On Mac OS:

```
$ brew install pandoc
$ pip install pypandoc twine
```

### Local Installation test

```
$ ./setup.py install --record files.txt
```

 * `sudo` is required in some cases

### Local Uninstallation test

```
$ cat files.txt | xargs rm -rf
```

### Create local package

```
$ tar czvf candy-board-qws.tgz --exclude "./.*" --exclude build --exclude dist *
```

## Test

```
$ ./setup.py test
```

## Publish

```
$ ./setup.py publish
```

# Revision history
* 1.2.2
    - Set operator property value to 'N/A' when there's no available operator
* 1.2.1
    - Set network property value to 'N/A' as the value isn't available on QWS modules
* 1.2.0
    - Return precise error on `modem init` command error
    - Fix ValueError
* 1.1.0
    - Add a new option to reset only packet counter
    - Filter USB serial ports for ppp
* 1.0.0
    - Initial public release
