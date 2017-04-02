# FIXME Replace HtmlResponse with lxml or something for performance.
from .. import SUMMER_URL, SUMMER_CHECK_URL
from . import asp_args, Page
from scrapy.http import HtmlResponse as hr
import requests as rq
import sys
from time import sleep

# 1 hai xuan; 2 qiang xuan; 3 di san lun
# Provide new cookies.
try:
    MY_COOKIES = {'ASP.NET_SessionId': sys.argv[1]}
except IndexError:
    print('Usage: %s <cookie value of ASP.NET_SessionId>')
    sys.exit()

class SummerPage(Page):
    URL = SUMMER_URL



class RadioForm(object):
    def __init__(self, asp):
        self.form = {'myradiogroup': '', 'lessonArrange': '课程安排'}
        self.form.update(asp)

    def post(self, radio_value):
        self.form['myradiogroup'] = radio_value
        resp = rq.post(url=SUMMER_URL, data=self.form, cookies=MY_COOKIES)
        return hr(url=resp.url, body=resp.text, encoding='utf-8')


class Spider(object):
    def __init__(self):
        print('Init...')

        # Get authorized. # 1 hai xuan; 2 qiang xuan; 3 di san lun
        resp = rq.get(SUMMER_CHECK_URL, cookies=MY_COOKIES)
        self.courses = hr(url=resp.url, body=resp.text, encoding='utf-8')
        self.form = RadioForm(asp_args(self.courses))

        print('Init complete!')

    def __parse_course(self, resp):
        for tr in resp.css('tr.tdcolour1, tr.tdcolour2'):
            info = [s.strip() for s in tr.xpath('.//text()').extract() if s.strip()]
            info.insert(0, tr.xpath('.//input/@value').extract_first())
            yield info

    def run(self):
        for cid in self.courses.css('input[type=radio]').xpath('./@value').extract():
            yield self.parse_by_cid(cid)

    def parse_by_cid(self, cid):
        resp = self.form.post(cid)
        sleep(2)
        while 'messagePage' in resp.url:
            print(cid + 'failed')
            resp = self.form.post(cid)
            sleep(2)
        print(resp.url)
        ret = {'courses': list(self.__parse_course(resp))}
        ret.update(asp_args(resp))
        return ret


