#!/usr/bin/env python
import gzip

from timeit import timeit
from gzip_read import zcat, pigz, gzip_buffered, gzip_mmap

FNAME = '/home/johannes/workspace/datasets/allora/allora_domains.gz'


@timeit
def r_mmap(iters=10):
    for _ in range(iters):
        with gzip_mmap(FNAME) as fhandle:
            for _ in fhandle:
                pass


@timeit
def r_pigz(iters=10):
    for _ in range(iters):
        with pigz(FNAME) as fhandle:
            for _ in fhandle:
                pass


@timeit
def r_zcat(iters=10):
    for _ in range(iters):
        with zcat(FNAME) as fhandle:
            for _ in fhandle:
                pass


@timeit
def buffered(iters=10):
    for _ in range(iters):
        with gzip_buffered(FNAME) as fhandle:
            for _ in fhandle:
                pass


@timeit
def gzip_rt(iters=10):
    for _ in range(iters):
        with gzip.open(FNAME, 'rt') as fhandle:
            for _ in fhandle:
                pass


if __name__ == "__main__":
    r_mmap(iters=1)
    r_pigz(iters=1)
    r_zcat(iters=1)
    buffered(iters=1)
    gzip_rt(iters=1)

