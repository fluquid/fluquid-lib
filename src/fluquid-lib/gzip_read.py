#!/usr/bin/env python
"""
fast reading of gzip files
"""
import os
import io
import mmap
from subprocess import Popen, PIPE
from contextlib import contextmanager
import gzip
import timeit


@contextmanager
def gzip_mmap(fname):
    with open(fname, 'r+b') as infile:
        with mmap.mmap(infile.fileno(),
                       length=0,
                       access=mmap.ACCESS_READ) as m_file:
            with gzip.open(m_file) as gz_file:
                with io.BufferedReader(gz_file) as f:
                    yield f


@contextmanager
def pigz(fname):
    """ requires `pigz` to be installed. """
    # throws OSError
    process = Popen(['pigz', '--decompress', '--stdout', fname],
                    stdout=PIPE, stderr=PIPE)
    yield process.stdout
    exitcode = process.wait()
    if exitcode:
        raise Exception('asdf %s', process.stderr.read())


@contextmanager
def zcat(fname):
    # throws OSError
    process = Popen(['zcat', fname], stdout=PIPE, stderr=PIPE)
    yield process.stdout
    exitcode = process.wait()
    if exitcode:
        raise Exception('asdf %s', process.stderr.read())


@contextmanager
def gzip_buffered(fname, *args, **kwargs):
    with gzip.open(fname, *args, **kwargs) as gz_file:
        with io.BufferedReader(gz_file) as f:
            yield f
