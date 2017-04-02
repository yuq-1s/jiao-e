#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Login jaccount and return requests.session object.

    TODO: 
        1. Add argparse to process username and password from CLI
        2. Decode captcha automatically
'''

from requests import Session
from sys import argv, exit
from pdb import set_trace
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
    prot, body = resp.request.url.split(':')
    return prot + 's' + body

def captcha_src(soup):
    for img_tag in soup.findAll('img'):
        if img_tag['src'].startswith('captcha?'):
            return img_tag['src']
    raise RuntimeError("Cannot find captcha.")


def input_captcha(sess, soup):
    r = sess.get('https://jaccount.sjtu.edu.cn/jaccount/'+captcha_src(soup),
            stream=True)
    return image_to_string(Image.open(BytesIO(r.content)))

def post_data(sess, soup, user, secret):
    form = ['sid', 'returl', 'se', 'v']

    data = dict(zip(form, [soup.find('input', {'name': s}).get('value') for s in form]))
    data['user'] = user
    data['pass'] = secret
    data['captcha'] = input_captcha(sess, soup)
    return data

def login(user, secret):
    logger = getLogger(__name__)
    try:
        with open('/tmp/cookie.pickle', 'rb') as f:
            sess = pickle.load(f)
            # TODO: Verify the sesion is not out dated.
            return sess
    except FileNotFoundError:
        for try_count in range(10):
            # Get Session object
            sess = Session()

            # Store ASP.NetSessionId in sess
            resp = sess.get('http://electsys.sjtu.edu.cn/edu/login.aspx')

            # Prepare for post
            soup = BeautifulSoup(resp.text, 'html.parser')
            post_url = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'

            # Post username and password and get authorization url
            auth_resp = sess.post(post_url, data = post_data(sess, soup, user, secret))
            soup = BeautifulSoup(auth_resp.text, 'html.parser')
            try:
                auth_url = soup.find('meta', {'http-equiv':'refresh'})['content'].split('url=')[1]

                # Get authorized
                sess.get(auth_url)

                logger.info("Login succeeded!")
                with open("/tmp/cookie.pickle", 'wb') as f:
                    pickle.dump(sess, f)
                return sess# , prepare_form(sess)
            except TypeError:
                logger.warning("The %d attempt to login failed ..." % try_count)
        logger.error("Login failed...")
        print("Are you sure about the username and password?")
        exit(1)

def prepare_cookie(sess):
    ele_cookies_list = ['ASP.NET_SessionId', 'mail_test_cookie']
    return {s: sess.cookies[s] for s in ele_cookies_list}

if __name__ == '__main__':
    print(prepare_cookie(login(argv[1], argv[2])))

# def check_session(sess):
#     check_list = ['ASP.NET_SessionId', 'JASiteCookie', 'mail_test_cookie']
#     resp_check = sess.get('http://electsys.sjtu.edu.cn/edu/student/sdtinfocheck.aspx',
#             cookies = {s: sess.cookies[s] for s in check_list})
