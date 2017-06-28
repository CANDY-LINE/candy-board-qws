# candy-board-qws

[![GitHub release](https://img.shields.io/github/release/CANDY-LINE/candy-board-qws.svg)](https://github.com/CANDY-LINE/candy-board-qws/releases/latest)
[![Build Status](https://travis-ci.org/CANDY-LINE/candy-board-qws.svg?branch=master)](https://travis-ci.org/CANDY-LINE/candy-board-qws)
[![License MIT](https://img.shields.io/github/license/CANDY-LINE/candy-board-qws.svg)](http://opensource.org/licenses/MIT)

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
$ pip install pypandoc
```

### Local Installation test

```
$ ./setup.py install --record files.txt
```

### Local Uninstallation test

```
$ cat files.txt | xargs rm -rf
```

### Create local package

```
$ tar czvf candy-board-qws.tgz --exclude .git --exclude .eggs --exclude build --exclude dist --exclude .cache .
```

## Test

```
$ ./setup.py test
```

# Revision history

* 1.0.0
    - Initial public release
