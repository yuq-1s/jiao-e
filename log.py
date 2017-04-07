#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import logging


# FIXME: Multiple call not checked, is that ok?
def setup_logger(module_name):
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
