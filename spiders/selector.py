# FIXME: Get rid of dependency of scrapy.
''' 解析html的工具，暂时用scrapy的HtmlResponse，以后改用更轻便的。
'''
from scrapy.http import HtmlResponse as Selector
import requests


def add_selector(html):
    if isinstance(html, str):
        html = Selector(url='', body=html, encoding='utf-8')
    elif isinstance(html, requests.Response) and not hasattr(html, 'css'):
        html = Selector(url=html.url, body=html.text, encoding='utf-8')

    if not isinstance(html, Selector):
        raise(TypeError('Bad argument: expected str or requests.Response'
                        ' or scrapy.http.HtmlResponse, given %s' % type(html)))
    return html
