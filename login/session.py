# -*- coding: utf-8 -*-
from .login import login

from urllib.parse import unquote
from time import sleep
from functools import wraps
from ..settings import SELECT_COURSE_URL, NORMAL_CHECK_URL_TEMPLATE, SUMMER_CHECK_URL_TEMPLATE
import logging

logger = logging.getLogger()


class Session(object):
    # Abstract base class needing CHECK_URL.
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.refresh()
        logger.debug("Session object initialization complete.")

    def _tackle_frequent_requests_error(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            response.raise_for_status()
            while True:
                try:
                    if 'outTimePage.aspx' in response.url:
                        self.refresh()
                        logger.error('Session outdated.')
                        continue
                    message = unquote(response.url.split('message=')[1])
                    if '刷新' in message:
                        sleep(self.SLEEP_DURATION)
                    else:
                        logger.debug(message)
                    response = func(self, *args, **kwargs)
                except IndexError:
                    return response
        return wrapper

    @_tackle_frequent_requests_error
    def get(self, *args, **kwargs):
        return self.raw_session.get(*args, **kwargs)

    @_tackle_frequent_requests_error
    def post(self, url, data, asp_dict, *args, **kwargs):
        if '__VIEWSTATE' not in data:
            data.update(asp_dict)
        return self.raw_session.post(url=url, data=data, *args, **kwargs)

    def head(self, *args, **kwargs):
        return self.raw_session.head(*args, **kwargs)

    def refresh(self):
        self.raw_session = login(self.username, self.password)
        self.head(self.CHECK_URL)

    def select_course(self, bsid, asp_dict):
        return self.post(url=SELECT_COURSE_URL,
                         data={'LessonTime1$btnChoose': '选定此教师',
                               'myradiogroup': bsid},
                         asp_dict=asp_dict)


# FIXME: This should be a singleton.
class SessionFactory(object):
    ''' Abstract session factory with CHECK_URL_TEMPLATE not specified.
    '''
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create(self, description):
        session = Session(self.username, self.password)
        if description['type'] == 'summer':
            session.CHECK_URL = SUMMER_CHECK_URL_TEMPLATE % description['round']
            return session
        elif description['type'] == 'normal':
            session.CHECK_URL = NORMAL_CHECK_URL_TEMPLATE % description['round']
            return session
        else:
            raise ValueError("ListPage has no type %s" % description)
