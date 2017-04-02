#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import logging


ASP_FORM_ID = ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION',
               '__EVENTTARGET', '__EVENTARGUMENT', '__LASTFOCUS']


EDU_URL = 'http://electsys.sjtu.edu.cn/edu/'
LESSON_URL = EDU_URL+'lesson/viewLessonArrange.aspx'
ELECT_URL = EDU_URL+'student/elect/'
MAIN_URL = ELECT_URL+'electcheck.aspx?xklc=%d' % 1
REMOVE_URL = ELECT_URL+'removeLessonFast.aspx'
SUBMIT_URL = ELECT_URL+'electSubmit.aspx'
RECOMMAND_URL = ELECT_URL+'RecommandTblOuter.aspx'
SUMMER_URL = ELECT_URL + 'ShortSession.aspx'
SUMMER_CHECK_URL = ELECT_URL+'ShortSessionCheck.aspx?xklc=%d' % 1


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

class SessionOutdated(Exception):
    pass
