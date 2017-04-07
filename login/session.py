from ..login.login import login

from urllib.parse import unquote
from time import sleep
from .. import SessionOutdated
from functools import wraps
import logging

logger = logging.getLogger()


class Session(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.raw_session = login(username, password)

    def _tackle_frequent_requests_error(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
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


class RobustSession(Session):
    # Abstract base class needing CHECK_URL.
    def post(self, *args, **kwargs):
        try:
            super().post(*args, **kwargs)
        except SessionOutdated:
            self.refresh()

    def refresh(self):
        self.raw_session = login(self.username, self.password)
        self.head(self.CHECK_URL)
