# -*- coding: utf-8 -*-
from ..login.login import login

from urllib.parse import unquote
from time import sleep
from functools import wraps
from ..settings import NORMAL_CHECK_URL_TEMPLATE, SUMMER_CHECK_URL_TEMPLATE
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


# FIXME: This should be a singleton.
class SessionFactory(object):
    ''' Abstract session factory with CHECK_URL_TEMPLATE not specified.
    '''
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_first_round(self):
        return self.__create_by_round(1)

    def create_second_round(self):
        return self.__create_by_round(2)

    def create_third_round(self):
        return self.__create_by_round(3)

    def __create_by_round(self, r0und):
        session = Session(self.username, self.password)
        session.CHECK_URL = self.CHECK_URL_TEMPLATE % r0und
        return session


class SummerSessionFactory(SessionFactory):
    CHECK_URL_TEMPLATE = SUMMER_CHECK_URL_TEMPLATE


class NormalSessionFactory(SessionFactory):
    CHECK_URL_TEMPLATE = NORMAL_CHECK_URL_TEMPLATE
