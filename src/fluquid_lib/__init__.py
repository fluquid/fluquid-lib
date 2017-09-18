# -*- coding: utf-8 -*-

__author__ = 'Johannes Ahlmann'
__email__ = 'johannes@fluquid.com'
__version__ = '0.1.0'

from itertools import islice, chain

'''
utility functions for python development.

* html
    * body to text
* requests.get
* gzip handling
* csv handling
* chunkify
* bing/google/yandex search
* string
    * detect language
    * "normalize"
    * ngrams
    * tfidf
    * tokenize, sentences, etc.
    * fast string find (pyaho)
* logging
    * set default level
    * log to file
* itertools
    * groupby
* date
    * date to epoch
    * epoch to date
    * date to iso
* tldextract
    * registered_domain
    * added domains (.uk.com)
* package
    * load package-local data file
* json
    * pretty print
* flask
    * auth?
* machine learning
    * text classification
    * LDA
* html-to-text
* lxml.etree
    * common ancestor
'''


# source: https://stackoverflow.com/a/1915307
def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))


# source: https://stackoverflow.com/a/24527424
def chunks(iterable, size=10):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))
