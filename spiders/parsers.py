# -*- coding: utf-8 -*-

from parsel import Selector
from .items import Course

from abc import ABCMeta, abstractmethod
from .loader import ItemLoader
import json
import logging

logger = logging.getLogger()


class Parser(object, metaclass=ABCMeta):
    ''' 解析抓到的页面的类
    '''

    def __init__(self, html):
        html.encoding = 'utf-8'
        self.selector = Selector(html.text)

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
            yield vars(ld.load_item())['_values']


# TODO: Add a local cache for pages.
class SpiderParser(Parser):
    def parse(self):
        for tr in self.selector.css('tr.tdcolour1, tr.tdcolour2'):
            yield {'cid': tr.xpath('./td[3]/text()').extract_first().strip(),
                   'name': tr.xpath('./td[2]/text()').extract_first().strip(),
                   'type': tr.xpath('./td[5]/text()').extract_first().strip(),
                   'credit': tr.xpath('./td[6]/text()').extract_first().strip(),
                   'hours': tr.xpath('./td[7]/text()').extract_first().strip(),
                   }


class SummerParser(SpiderParser):
    pass


# TODO
class ParserFactory(object):
    def create(self, description):
        pass
