#!/usr/bin/env python
"""
fast reading of gzip files

timings on decent sized machine:
(Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz; 4 cores)

## Python 3:
- 'pigz'        took: 3.8783 sec
- 'zcat'        took: 7.2531 sec
- 'buffered'    took: 8.4927 sec
- 'mmap'        took: 9.8283 sec
- 'gzip_rt'     took: 10.9042 sec

Comparison is slightly skewed, because "gzip_rt" produces unicode
    whereas other solutions may produce byte strings
"""
import io
import mmap
from subprocess import Popen, PIPE
from contextlib import contextmanager
import gzip
import logging
import atexit


@contextmanager
def gzip_mmap(fname):
    logging.warn('gzip_mmap is only included for reference')
    with open(fname, 'r+b') as infile:
        with mmap.mmap(infile.fileno(),
                       length=0,
                       access=mmap.ACCESS_READ) as m_file:
            with gzip.open(m_file) as gz_file:
                with io.BufferedReader(gz_file) as f:
                    yield f


@contextmanager
def pigz(fname, universal_newlines=False, *args, **kwargs):
    """ requires `pigz` to be installed.

    :param universal_newlines: should really be called text_mode
        (https://docs.python.org/3/glossary.html#term-universal-newlines)
    """
    process = Popen(['pigz', '--decompress', '--stdout', fname],
                    universal_newlines=universal_newlines,
                    stdout=PIPE, stderr=PIPE, *args, **kwargs)
    atexit.register(process.terminate)
    yield process.stdout
    exitcode = process.wait()
    if exitcode:
        raise Exception('asdf %s', process.stderr.read())


@contextmanager
def zcat(fname, *args, **kwargs):
    process = Popen(['zcat', fname],
                    stdout=PIPE, stderr=PIPE, *args, **kwargs)
    atexit.register(process.terminate)
    yield process.stdout
    exitcode = process.wait()
    if exitcode:
        raise Exception('asdf %s', process.stderr.read())


@contextmanager
def gzip_buffered(fname, *args, **kwargs):
    with gzip.open(fname, 'rb', *args, **kwargs) as gz_file:
        with io.BufferedReader(gz_file) as f:
            yield f
