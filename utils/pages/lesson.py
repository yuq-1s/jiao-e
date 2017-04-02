from . import Page

class LessonPage(Page):
    def parse(self):
        for tr in self.selector.css('tr.tdcolour1, tr.tdcolour2'):
            info = [s.strip() for s in tr.xpath('.//text()').extract() if s.strip()]
            info.insert(0, tr.xpath('.//input/@value').extract_first())
            yield info

