#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Login jaccount and return requests.session object.

    TODO: 
        1. Add argparse to process username and password from CLI
        2. head CHECK_URL immediately after login.
'''

from requests import Session
from sys import argv, exit
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from pytesseract import image_to_string
from logging import getLogger
import pickle

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def tohttps(oriurl):
    prot, body = response.request.url.split(':')
    return prot + 's' + body

def captcha_src(soup):
    for img_tag in soup.findAll('img'):
        if img_tag['src'].startswith('captcha?'):
            return img_tag['src']
    raise RuntimeError("Cannot find captcha.")


def input_captcha(session, soup):
    r = session.get('https://jaccount.sjtu.edu.cn/jaccount/'+captcha_src(soup),
            stream=True)
    return image_to_string(Image.open(BytesIO(r.content)))

def post_data(session, soup, user, secret):
    form = ['sid', 'returl', 'se', 'v']

    data = dict(zip(form, [soup.find('input', {'name': s}).get('value') for s in form]))
    data['user'] = user
    data['pass'] = secret
    data['captcha'] = input_captcha(session, soup)
    return data

def login(user, secret):
    logger = getLogger(__name__)
    try:
        with open('/tmp/cookie.pickle', 'rb') as f:
            session = pickle.load(f)
            # TODO: Verify the sesion is not out dated.
            return session
    except FileNotFoundError:
        for try_count in range(10):
            # Get Session object
            session = Session()

            # Store ASP.NetSessionId in session
            response = session.get('http://electsys.sjtu.edu.cn/edu/login.aspx')

            # Prepare for post
            soup = BeautifulSoup(response.text, 'html.parser')
            post_url = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'

            # Post username and password and get authorization url
            auth_response = session.post(post_url, data = post_data(session, soup, user, secret))
            soup = BeautifulSoup(auth_response.text, 'html.parser')
            if '教学信息服务网' in auth_response.text:
                logger.info("Login succeeded!")
                with open("/tmp/cookie.pickle", 'wb') as f:
                    pickle.dump(session, f)
                return session# , prepare_form(session)
            else:
                logger.warning("The %d attempt to login failed ..." % try_count)
        logger.error("Login failed...")
        print("Are you sure about the username and password?")
        exit(1)

def prepare_cookie(session):
    ele_cookies_list = ['ASP.NET_SessionId', 'mail_test_cookie']
    return {s: session.cookies[s] for s in ele_cookies_list}

if __name__ == '__main__':
    print(prepare_cookie(login(argv[1], argv[2])))

# def check_session(session):
#     check_list = ['ASP.NET_SessionId', 'JASiteCookie', 'mail_test_cookie']
#     resp_check = session.get('http://electsys.sjtu.edu.cn/edu/student/sdtinfocheck.aspx',
#             cookies = {s: session.cookies[s] for s in check_list})
