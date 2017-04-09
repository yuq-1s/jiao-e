#! /usr/bin/env python3
# -*- coding: utf-8 -*-

ASP_FORM_ID = ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION',
               '__EVENTTARGET', '__EVENTARGUMENT', '__LASTFOCUS']


EDU_URL = 'http://electsys.sjtu.edu.cn/edu'
ELE_LOGIN_URL = EDU_URL + '/login.aspx'
LESSON_URL = EDU_URL+'/lesson/viewLessonArrange.aspx'
ELECT_URL = EDU_URL+'/student/elect'
NORMAL_CHECK_URL_TEMPLATE = ELECT_URL+'/electcheck.aspx?xklc=%d'
REMOVE_URL = ELECT_URL+'/removeLessonFast.aspx'
NORMAL_SUBMIT_URL = ELECT_URL+'/electSubmit.aspx'
RECOMMAND_URL = ELECT_URL+'/RecommandTblOuter.aspx'
SUMMER_URL = ELECT_URL + '/ShortSession.aspx'
SUMMER_CHECK_URL_TEMPLATE = ELECT_URL+'/ShortSessionCheck.aspx?xklc=%d'
SELECT_COURSE_URL = LESSON_URL+'?&xklx=&redirectForm=outSpeltyEp.aspx&kcmk=-1'
SUMMER_SUBMIT_URL = ELECT_URL+'/什么来着我忘了.aspx'
JACCOUNT_URL = 'https://jaccount.sjtu.edu.cn/jaccount/'
