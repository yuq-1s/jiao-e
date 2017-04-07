from ..selector import add_selector, Selector
import requests
import logging

logger = logging.getLogger()


class Page(object):
    ''' Abstract base class for Page objects.
        Needing url
    '''

    def __init__(self, session, html=''):
        self.session = session
        self.selector = add_selector(html if html else self.get(self.url))
        self.asp_dict = self.get_asp_args(self.selector)

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

    def _get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    def _post(self, url, data, *args, **kwargs):
        try:
            return self.session.post(url=url, data=data, asp_dict=self.asp_dict,
                                     *args, **kwargs)
        except requests.exceptions.HTTPError:
            self.asp_dict = self.get_asp_args(self.get(self.url))
            return self.session.post(data=data, asp_dict=self.asp_dict,
                                     *args, **kwargs)
