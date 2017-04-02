# FIXME Replace HtmlResponse with lxml or something for performance.
from .. import SUMMER_URL, SUBMIT_URL
from . import Page
from .lesson import LessonPage


class SummerPage(Page):
    URL = SUMMER_URL
    SLEEP_DURATION = 2

    def parse(self):
        return self.selector.css('input[type=radio]').xpath('./@value').extract()

    def run(self):
        for course_id in self.parse():
            lesson_page = self.view_course(course_id)
            yield {'asp': lesson_page.asp, 'course': list(lesson_page.parse())}

    def view_course(self, course_id):
        return LessonPage(self.sess,
                          self.post({'myradiogroup': course_id,
                                     'lessonArrange': '课程安排'}))

    def submit(self):
        return self.sess.head(SUBMIT_URL)

