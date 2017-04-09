from ..settings import (SELECT_COURSE_URL, NORMAL_CHECK_URL_TEMPLATE,
                       ELE_LOGIN_URL, SUMMER_CHECK_URL_TEMPLATE, JACCOUNT_URL)

from urllib.parse import unquote
from time import sleep
from functools import wraps
from PIL import Image
from io import BytesIO
from pytesseract import image_to_string
import requests
import logging
import re
import pickle

logger = logging.getLogger()


class Session(object):
    MAX_LOGIN_TRAIL = 10
    ''' 包装requests.session，进行登录后的验证和处理教务网的message和session过期
    '''
    # Abstract base class needing CHECK_URL.
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.refresh()
        logger.debug("Session object initialization complete.")

    def _login(self):
        def __parse_jaccount_page(html):
            search_pattern = r'\<input type=\"hidden\" name=\"(\w+)\" value=\"([a-zA-Z0-9_+/=]+)\"\>'
            for match in re.finditer(search_pattern, html):
                yield match.groups()

        try:
            with open('/tmp/session.pickle', 'rb') as f:
                # TODO: Verify the sesion is not out dated.
                self.raw_session = pickle.load(f)
        except FileNotFoundError:
            for try_count in range(self.MAX_LOGIN_TRAIL):
                self.raw_session = requests.Session()
                jaccount_response = self.raw_session.get(ELE_LOGIN_URL)
                form = dict(__parse_jaccount_page(jaccount_response.text))
                captcha_url = JACCOUNT_URL + re.search(
                    r'\<img src=\"(captcha\?\d+)\"',
                    jaccount_response.text).group(1)
                captcha = image_to_string(Image.open(BytesIO(
                    self.raw_session.get(captcha_url, stream=True).content)))
                form.update({'v': '',
                             'user': self.username,
                             'pass': self.password,
                             'captcha': captcha})

                post_response = self.raw_session.post(
                    JACCOUNT_URL+'ulogin', data=form)
                if '教学信息服务网' in post_response.text:
                    logger.info("Login succeeded!")
                    with open("/tmp/session.pickle", 'wb') as f:
                        pickle.dump(self.raw_session, f)
                    return
                else:
                    logger.warning("The %d attempt to login failed ..." % try_count)
            logger.error("Login failed...")
            print("Are you sure about the username and password?")
            exit(1)

    def _tackle_frequent_requests_error(func):
        ''' 处理页面过期和频繁刷新页面的提示
        '''
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
        self.raw_session = self._login()
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
