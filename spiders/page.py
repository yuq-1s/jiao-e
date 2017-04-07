from ..login.login import login
from .selector import add_selector, Selector

from urllib.parse import unquote
from time import sleep
from utils import SessionOutdated
from functools import wraps
import requests
import logging

logger = logging.getLogger()


class Page(object):
    ''' Abstract base class for Page objects.
    '''
    URL = ''
    SLEEP_DURATION = 0

    def __init__(self, session, html=''):
        assert self.URL, 'Bad Page class: Empty URL'
        assert self.SLEEP_DURATION, 'Bad Page class: Empty SLEEP_DURATION'
        self.session = session
        self.selector = add_selector(html if html else self.get(self.URL))
        self.asp = self.get_asp_args(self.selector)

    def get_asp_args(self, response):
        ''' Parse "__xx" arguments (such as __VIEWSTATE) from selector
        '''
        if not isinstance(response, Selector):
            selector = add_selector(response)
        ret = {}
        for tag in selector.css('input'):
            name = tag.xpath('./@name').extract_first()
            value = tag.xpath('./@value').extract_first()
            if name and name.startswith('__'):
                ret.update({name: value})
        return ret

    def _ensure(func):
        @wraps(func)
        def wrapper(self, *args, **kw):
            response = func(self, *args, **kw)
            response.raise_for_status()
            while True:
                try:
                    if 'outTimePage.aspx' in response.url:
                        raise SessionOutdated
                    message = unquote(response.url.split('message=')[1])
                    if '刷新' in message:
                        sleep(self.SLEEP_DURATION)
                    else:
                        logger.debug(message)
                    response = func(self, *args, **kw)
                except IndexError:
                    return response
        return wrapper

    @_ensure
    def get(self, *args, **kw):
        return self.session.get(*args, **kw)

    @_ensure
    def post(self, data, *args, **kw):
        if '__VIEWSTATE' not in data:
            data.update(self.asp)
        return self.session.post(self.URL, data, *args, **kw)


class RobustPage(Page):
    CHECK_URL = ''

    def __init__(self, session, html, user, passwd):
        assert self.CHECK_URL, 'Bad Page class: Empty CHECK_URL'
        super().__init__(session, html)
        self.user = user
        self.passwd = passwd

        if not self.session:
            self.session = login(self.user, self.passwd)

    def post(self, *args, **kw):
        try:
            super().post(*args, **kw)
        except SessionOutdated:
            self.refresh()
        except requests.exceptions.HTTPError:
            self.asp = self.get_asp_args(self.get())

    def refresh(self):
        self.session = login(self.user, self.passwd)
        self.head(self.CHECK_URL)
