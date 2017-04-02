from . import Page


class LessonPage(Page):
    SLEEP_DURATION = 2

    def __init__(self, sess, html='', url=''):
        if url:
            self.URL = url
        elif html:
            self.URL = html.url
        super().__init__(sess, html)

    def parse(self):
        for tr in self.selector.css('tr.tdcolour1, tr.tdcolour2'):
            info = [s.strip() for s in tr.xpath('.//text()').extract() if s.strip()]
            info.insert(0, tr.xpath('.//input/@value').extract_first())
            yield info

    def select_course(self, bsid):
        return self.post({'LessonTime1$btnChoose': '选定此教师',
                   'myradiogroup': bsid})
