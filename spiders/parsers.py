from .selector import add_selector, Selector
from .items import Course

from abc import ABCMeta, abstractmethod
from scrapy.loader import ItemLoader
import json
import logging

logger = logging.getLogger()


class Parser(object):
    ''' Abstract base class for Page objects.
        Needing url
    '''
    __metaclass__ = ABCMeta

    def __init__(self, html=''):
        self.selector = add_selector(html if html else self.get(self.url))

    def get_asp_args(self):
        ''' Parse "__xx" arguments (such as __VIEWSTATE) from selector
        '''
        ret = {}
        for tag in self.selector.css('input'):
            name = tag.xpath('./@name').extract_first()
            value = tag.xpath('./@value').extract_first()
            if name and name.startswith('__'):
                ret.update({name: value})
        return ret

    @abstractmethod
    def parse(self):
        pass


class LessonParser(Parser):
    def parse(self):
        for tr in self.selector.css('tr.tdcolour1, tr.tdcolour2'):
            ld = ItemLoader(item=Course(), selector=tr)
            ld.add_xpath('bsid', './/input/@value')
            ld.add_xpath('teacher', './td[2]')
            ld.add_xpath('teacher_job', './td[3]')
            ld.add_xpath('cid', './td[4]')
            ld.add_xpath('hours', './td[5]')
            ld.add_xpath('max_member', './td[6]')
            ld.add_xpath('min_member', './td[7]')
            ld.add_xpath('now_member', './td[8]')
            ld.add_xpath('time', './td[10]')
            ld.add_xpath('remark', './td[11]')
            ld.add_value('asp', json.dumps(self.get_asp_args()))
            yield ld.load_item()


# TODO
class SpiderParser(Parser):
    def parser(self):
        for cid in self.selector.css('input[type=radio]') \
                .xpath('./@value').extract():
            yield cid

# TODO
class ParserFactory(object):
    def create(self, description):
        pass
