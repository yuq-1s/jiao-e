# FIXME Replace HtmlResponse with lxml or something for performance.
from .. import SUMMER_URL, SUBMIT_URL
from ..login.session import SessionFactory
from .parsers import ParserFactory, LessonParser

from abc import ABCMeta, abstractmethod
import logging
import requests

logger = logging.getLogger(__name__)


class Spider(object):
    # Misssing: url, SUBMIT_URL, session_config, parser_config
    __metaclass__ = ABCMeta

    def __init__(self, username, password):
        self.session = SessionFactory(username,
                                      password).create(self.session_config)
        self.__refresh_parser()

    def _get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    def _post(self, url, data, *args, **kwargs):
        while True:
            try:
                return self.session.post(url=url,
                                         data=data,
                                         asp_dict=self.asp_dict,
                                         *args,
                                         **kwargs)
            except requests.exceptions.HTTPError:
                logger.error("asp arguments expired.")
                self.__refresh_parser()

    def __refresh_parser(self):
        self.parser = ParserFactory(self.session).create(self.parser_config)
        self.asp_dict = self.parser.get_asp_args()

    def get_current_number_by_course_id(self, course_id):
        for info in self.crawl_by_course_id(course_id):
            yield {info['bsid']: info['now_number']}

    def grab_course_by_bsid(self, bsid):
        while True:
            response = self.session.select_course(bsid)
            if response.url == self.url:
                self._submit()
                return True

    def _submit(self):
        self.session.head(self.SUBMIT_URL)

    @abstractmethod
    def crawl_one_course_by_course_id(self, course_id):
        ''' 根据课程代码爬课的信息
            @params course_id: 课程代码，比如AD001
            @return 一个课程信息生成器，信息格式见lesson_page.py
        '''
        pass

    @abstractmethod
    def crawl(self):
        ''' 爬所有课程信息，
            @params course_id: 课程代码，比如AD001
            @return 一个课程信息生成器，信息格式见lesson_page.py
        '''
        pass


# TODO: Add a local cache for pages.
class SummerSpider(Spider):
    url = SUMMER_URL
    SUBMIT_URL = SUBMIT_URL
    description = {}

    def crawl_one_course_by_course_id(self, course_id):
        inner_parser = LessonParser(self._post({'myradiogroup': course_id,
                                                'lessonArrange': '课程安排'}))
        outer_info = self.__search_outer_info_by_course_id(course_id)
        for inner_info in inner_parser.parse():
            inner_info.update(outer_info)
            yield inner_info

    # FIXME: 这个代码重复修一下.
    def crawl(self):
        for outer_info in self.parser.parse():
            inner_parser = LessonParser(self._post({'myradiogroup':
                                                    outer_info['cid'],
                                                    'lessonArrange':
                                                    '课程安排'}))
            for inner_info in inner_parser.parse():
                inner_info.update(outer_info)
                yield inner_info

    def __search_outer_info_by_course_id(self, course_id):
        for outer_info in self.parser.parse():
            if outer_info['cid'] == course_id:
                return outer_info
        raise ValueError("Course Id %s not found" % course_id)

# class SpiderFactory(PageFactory):
#     def create(self, description):
#         if description == 'summer':
#             return SummerSpider(self.session)
#         else:
#             raise TypeError("ListPage has no type %s" % description)
