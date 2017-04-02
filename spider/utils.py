#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import re


# FIXME: Multiple call not checked, is that ok?
def get_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARN)
    ch.setFormatter(formatter)

    LOG_PATHNAME = os.path.dirname(os.path.abspath(__file__))+'/log'
    try:
        os.mkdir(LOG_PATHNAME)
    except FileExistsError:
        pass
    try:
        LOG_FILENAME = sys.argv[1]+'-qiangke'
    except IndexError:
        LOG_FILENAME = 'qiangke'

    fh = logging.FileHandler('{}/{}.log'.format(LOG_PATHNAME, LOG_FILENAME))
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


logger = get_logger(__name__)


def asp_args(resp):
    ''' Parse "__xx" arguments (such as __VIEWSTATE) from HtmlResponse
    '''
    ret = {}
    for tag in resp.css('input'):
        name = tag.xpath('./@name').extract_first()
        value = tag.xpath('./@value').extract_first()
        if name and name.startswith('__'):
            ret.update({name: value})
    return ret


def parse_time(s):
    ''' Parse duration of a course from the remark field.
    '''
    def helper(parity, rmk):
        for match in re.finditer(r'星期(?P<day>\w)\s*第(?P<cbegin>\d+)节--'
                                 r'第(?P<cend>\d+)节\s*(?P<place>.*)'
                                 r'\((?P<wbegin>\d+)-(?P<wend>\d+)周\)\.',
                                 parity):
            result = match.groupdict()
            result.update({'parity': rmk})
            yield result

    try:
        odd, even = re.search(r'单周((?:\s(?:.*))+)双周((?:\s(?:.*))+)',
                              s).groups()
        for duration in helper(odd, 'odd'):
            yield duration
        for duration in helper(even, 'even'):
            yield duration
    except AttributeError:
        for duration in helper(s, 'both'):
            yield duration
