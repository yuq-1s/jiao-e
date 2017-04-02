#! /usr/bin/evn python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from jaccount import login
from utils import asp_params, EmptyCourse
from abc import ABCMeta, abstractmethod

import re
import logging

logger = logging.getLogger()

ELECT_URL = 'http://electsys.sjtu.edu.cn/edu/student/elect/'
LESSON_URL = 'http://electsys.sjtu.edu.cn/edu/lesson/'


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

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from pdb import set_trace
from bs4 import BeautifulSoup
import requests
from logging import getLogger, StreamHandler, Formatter, DEBUG
from itertools import count
from functools import wraps
from sys import stdout
from urllib.parse import urlencode, urlparse, unquote
from lxml import etree
from time import sleep
from threading import Thread
from pages import InitPage, MainPage, GrabPage, LessonPage
from utils import MessageError, SessionOutdated, EmptyCourse
from jaccount import login

import itertools
import re
# TODO:
#   1. Try to grab courses directly.(not step by step from main page)

# When in main page (aka path /)
ELECT_URL = 'http://electsys.sjtu.edu.cn/edu/student/elect/'
LESSON_URL = 'http://electsys.sjtu.edu.cn/edu/lesson/'
# MAIN_PAGE_URL = ELECT_URL+'sltFromRcommandTbl.aspx'


logger = getLogger(__name__)

# ch = StreamHandler(stdout)
# ch.setLevel(DEBUG)
# formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)



class Runner(Thread):
    def __init__(self, grabpage, lessonpage, cracker):
        super().__init__()
        self.grabpage = grabpage
        self.lessonpage = lessonpage
        self.cracker = cracker

    def run(self):
        for cnt in itertools.count():
            try:
                if 'message=' not in self.lessonpage.proceed().url:
                    # if '/secondRoundFP.aspx' in resp.url:
                    resp = self.grabpage.submit()
                    if not 'successful.aspx' in resp.url:
                        logger.error(resp.url)
                        respi = self.cracker.initpage.proceed()
                        respm = self.cracker.mainpage.proceed()
                        respa = self.cracker.grabpage.proceed()
                        logger.error('Why cannot submit?')
                        # raise ResetException
                    else:
                        logger.error('Successfully got %s lesson.'%
                                self.lessonpage.url)
                        return
            except ConnectionError as e:
                sleep(5)
                logger.error(e)





class BasePage(metaclass=ABCMeta):
    def __init__(self, craker, text):
        self.text = text
        self.param.update(asp_params(self.text))
        self.craker = craker

    def proceed(self):
        return self.craker.post(self.url, data=self.param)

    def resp_by_param(self, param):
        while True:
            try:
                param.update(asp_params(self.text))
                return self.craker.post(self.url, data=param)
            except requests.exceptions.HTTPError:
                logger.error('500 error when posting %s'%param)
                self.recover()

    @abstractmethod
    def recover(self):
        # recover by cracker
        pass

class CoursesPage(object):
    def __init__(self, cracker, text):
        self.text = text
        self.asp = asp_params(self.text)

        soup = BeautifulSoup(self.text, 'html.parser')

        button = soup.find_all('input', {'class':'button', 'value':'课程安排'})
        assert len(button) == 1
        self.les_arr_param = {button[0]['name']: '课程安排'}

        trs = soup.find_all('tr', {'class': re.compile('tdcolour\d')})
        self.courses = [CoursePageCourse(tr) for tr in trs]

        logger.debug(button)
        logger.debug(self.courses)

    def _param_by_cid(self, cid):
        ret = {'myradiogroup': cid}
        ret.update(self.asp)
        ret.update(self.les_arr_param)
        logger.debug(ret)
        return ret

    def post_param(self, param, *arg, **kw):
        param.update(self.asp)
        return self.cracker.post(data=param, *arg, **kw)

    def lesson_by_name(self, name):
        result = [c for c in courses if c.name == name]
        if not result or len(result) > 1:
            raise NotImplementedError('Course named %s is not unique'%name)
        course = result[0]
        # Eliminate 参数错误
        self.cracker.post(self.url, data={})
        return self.cracker.post(self.url, data=self._param_by_cid(course.cid))



class InitPage(BasePage):
    url = ELECT_URL+'electwarning.aspx?xklc=2'
    def __init__(self, craker):
        self.param = {'CheckBox1': 'on', 'btnContinue': '继续'}
        super().__init__(craker, self.cracker.sess.get(InitPage.url).text)
        # self.url = ELECT_URL+'electwarning.aspx?xklc=1'


class BixiuPage(CoursesPage):
    def __init__(self, craker, text):
        self.url = ELECT_URL+'speltyRequiredCourse.aspx'
        # self.param = {'SpeltyRequiredCourse1$btnQxsy': '抢选首页'}
        super().__init__(craker, text)

    def to_tongshi(self):
        tongshi_param = {'SpeltyRequiredCourse1$btnTxk': '通识课'}
        return TongshiPage(self.craker, self.resp_by_param(tongshi_param).text)
    # param.update(asp_params(self.sess.post(url, data=init_param).text))

class GrabPage(BasePage):
    def __init__(self, craker, text, param):
        self.url=ELECT_URL+'secondRoundFP.aspx?yxdm=&nj=2015&kcmk=-1&txkmk=-1&tskmk='
        self.param = param
        super().__init__(craker, text)

    def submit(self):
        submit_param = {'btnSubmit': '选课提交'}
        submit_param.update(asp_params(self.text))
        return self.craker.post(self.url, data=submit_param)
    # param = {'__EVENTTARGET': param}

    def to_bixiu(self):
        bixiu_param = {'btnBxk': '必修课'}
        bixiu_param.update(asp_params(self.text))
        return BixiuPage(self.craker,
                self.craker.post(self.url, data=bixiu_param).text)

class LessonPage(BasePage):
    def __init__(self, craker, text, url, course):
        self.url = url
        self.text = text
        self.param = {'myradiogroup': self.get_bsid(course),
                'LessonTime1$btnChoose': '选定此教师'}
        # if not self.param['myradiogroup']:
        super().__init__(craker, text)

    def get_bsid(self, course):
        soup = BeautifulSoup(self.text, 'html.parser')
        trs = soup.find_all('tr', {'class': re.compile('tdcolour\d')})
        courses = [LessonPageCourse(tr) for tr in trs]
        bsids = [c.bsid for c in courses if c.teacher == course.teacher and \
                c.remark == course.remark and course.time in c.time]
        if not bsids:
            raise EmptyCourse(self.url)
        # FIXME: Ask for user input if bsid is not determined.
        assert len(bsids) == 1
        return bsids[0]
        # if len(bsid) == 1:
        # for inp in soup.find_all('input', {'type': 'radio'}):
        #     if inp['value'] in course:
        #         return inp['value']

class LessonPageCourse(object):
    def __init__(self, tr):
        self.teacher = tr.find_all('td')[1].text.strip()
        self.time = tr.find_all('td')[9].text.strip()
        self.remark = tr.find_all('td')[10].text.strip()
        self.bsid = tr.input['value']


class CoursePageCourse(object):
    def __init__(self, tr):
        tds = tr.find_all('td')
        self.name = tds[1].text.strip()
        self.cid = tds[2].text.strip()
        self.property = tds[3].text.strip()
        self.credits = tds[4].text.strip()
        self.hours = tds[5].text.strip()
        self.selected = True if tds[6].text.strip() == '√' else False
        # self.params = {'myradiogroup': self.cid}
# SpeltyRequiredCourse1$lessonArrange:课程安排


class QiangxuanPages(object):
    def __init__(self, craker):
        self.cracker = cracker
        self.initpage = InitPage(cracker)
        qxresp = self.initpage.proceed()
        self.qxpage = GrabPage(cracker, qxresp.text)
        self.bxpage = BixiuPage(cracker,
                self.qxresp.post_param({'btnBxk': '必修课'}).text)
        self.tspage = TongshiPage(cracker,
                self.qxresp.post_param({'btnTxk': '通识课'}).text)
        self.rxpage = RenxuanPage(cracker, 
                self.qxresp.post_param({'btnXuanXk':'任选课'}).text)
        self.xxpage = XianxuanPage(cracker, 
                self.qxresp.post_param({'btnXxk':'限选课'}).text)

    def refresh(self):
