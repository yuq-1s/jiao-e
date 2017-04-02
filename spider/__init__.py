#! /usr/bin/env python3
# -*- coding: utf-8 -*-

ASP_FORM_ID = ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION',
               '__EVENTTARGET', '__EVENTARGUMENT', '__LASTFOCUS']


EDU_URL = 'http://electsys.sjtu.edu.cn/edu/'
LESSON_URL = EDU_URL+'lesson/viewLessonArrange.aspx'
ELECT_URL = EDU_URL+'student/elect/'
MAIN_URL = ELECT_URL+'electcheck.aspx?xklc=%d' % 1
REMOVE_URL = ELECT_URL+'removeLessonFast.aspx'
SUBMIT_URL = ELECT_URL+'electSubmit.aspx'
RECOMMAND_URL = ELECT_URL+'RecommandTblOuter.aspx'
SUMMER_URL = ELECT_URL + 'ShortSession.aspx'
SUMMER_CHECK_URL = ELECT_URL+'ShortSessionCheck.aspx?xklc=%d' % 1


class SessionOutdated(Exception):
    pass
