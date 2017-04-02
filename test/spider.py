#! /usr/bin/env python3

from utils.pages.summer import SummerPage
from utils import SUMMER_CHECK_URL
from pdb import set_trace
import requests as rq
import sys

if __name__ == '__main__':
    try:
        sess = rq.Session()
        sess.cookies.set(name='ASP.NET_SessionId', value=sys.argv[1])
        sess.head(SUMMER_CHECK_URL)
        for info in SummerPage(sess).run():
            print(info)
            set_trace()
    except IndexError:
        print('Usage: %s <cookie value of ASP.NET_SessionId>')
        sys.exit()
