from jaccount import login
from urllib.parse import unquote
from time import sleep
from utils import SessionOutdated
from functools import wraps
from scrapy.http import HtmlResponse as hr
import requests
import logging

logger = logging.getLogger()


def asp_args(resp=None, text=''):
    ''' Parse "__xx" arguments (such as __VIEWSTATE) from HtmlResponse
    '''
    if isinstance(resp, str):
        resp = hr(url='', body=resp, encoding='utf-8')
    elif isinstance(resp, requests.Response) and not hasattr(resp, 'css'):
        resp = hr(url=resp.url, body=resp.text, encoding='utf-8')

    if not isinstance(resp, hr):
        raise(TypeError('Bad argument: expected str or requests.Response'
                        ' or scrapy.http.HtmlResponse, given %s' % type(resp)))

    ret = {}
    for tag in resp.css('input'):
        name = tag.xpath('./@name').extract_first()
        value = tag.xpath('./@value').extract_first()
        if name and name.startswith('__'):
            ret.update({name: value})
    return ret


class Page(object):
    SLEEP_DURATION = 0
    ASP_ARGS = {}
    URL = ''

    def __init__(self, sess, text=''):
        assert self.URL, 'Bad Page class: Empty URL'
        assert self.SLEEP_DURATION, 'Bad Page class: Empty SLEEP_DURATION'
        self.sess = sess
        self.ASP_ARGS = asp_args(text if text else self.get(self.URL))

    @classmethod
    def _ensure(cls, func):
        @wraps(func)
        def wrapper(*args, **kw):
            resp = func(*args, **kw)
            resp.raise_for_status()
            while True:
                try:
                    if 'outTimePage.aspx' in resp.url:
                        raise SessionOutdated
                    message = unquote(resp.url.split('message=')[1])
                    if '刷新' in message:
                        sleep(cls.SLEEP_DURATION)
                    else:
                        logger.debug(message)
                    resp = func(*args, **kw)
                except IndexError:
                    return resp
        return wrapper

    @_ensure
    def get(self, *args, **kw):
        return self.sess.get(*args, **kw)

    @_ensure
    def post(self, data, *args, **kw):
        if '__VIEWSTATE' not in data:
            data.update(self.ASP_ARGS)
        return self.sess.post(self.URL, data, *args, **kw)


class RobustPage(Page):
    CHECK_URL = ''

    def __init__(self, sess, text, user, passwd):
        assert self.CHECK_URL, 'Bad Page class: Empty CHECK_URL'
        super().__init__()
        self.user = user
        self.passwd = passwd

        if not self.sess:
            self.sess = login(self.user, self.passwd)

    def post(self, *args, **kw):
        try:
            super().post(*args, **kw)
        except SessionOutdated:
            self.refresh()
        except requests.exceptions.HTTPError:
            self.ASP_ARGS = asp_args(self.get())

    def refresh(self):
        self.sess = login(self.user, self.passwd)
        self.head(self.CHECK_URL)
