from . import Page
from pdb import set_trace
from .items import Course
from scrapy.loader import ItemLoader

class LessonPage(Page):
    SLEEP_DURATION = 2

    def __init__(self, session, html='', url=''):
        if url:
            self.URL = url
        elif html:
            self.URL = html.url
        super().__init__(session, html)

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
            yield ld.load_item()

    def select_course(self, bsid):
        return self.post({'LessonTime1$btnChoose': '选定此教师',
                   'myradiogroup': bsid})
