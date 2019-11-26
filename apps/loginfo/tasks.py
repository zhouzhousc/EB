#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 17:46
# @Author  : userzhang
import binascii
import json
# from apps.loginfo.models import NoticeManager,Event_list
from .models import NoticeManager, Event_list, Log_list
from celery.task import Task
import django

from django_redis import get_redis_connection
from http.client import HTTPConnection
django.setup()
import time
from .utils.MYSQL import eventNotice,APINUMBER


start_time = int(time.time())

NoticeManagerdata = NoticeManager.objects.values()

class EmailManage:
    '''发送激活链接类'''
    @staticmethod
    def sendMail(toMail, sub, content, cc="", html="False"):
        toMail = type(toMail) != list and toMail or ",".join(toMail)
        data = {"system_name": "Edge Connect", "toMail": toMail, "content": content, "mail_title": sub,
                "cc": cc, "html_status": html, "errors_type": "email"}
        try:
            body = json.dumps(data)
            headers = {"Content-Type": "text/html; charset=utf-8"}
            conn = HTTPConnection("10.129.4.95:9090")
            conn.request(method="POST", url="/data_manage/", body=body, headers=headers)
            res = conn.getresponse().read().decode(encoding="utf-8")  #bug1: 老是卡顿在这里
            res=json.loads(res)
            if res["status"] == "True":
                print("邮件发送成功")
            else:
                print("邮件发送失败")
        except Exception as e:
            print("邮件发送失败-", repr(e))

class Send_enent_email_tasks(Task):
    name = "Send_enent_email_tasks"

    def event_message(self):
        emailname = dict()
        status = dict()
        Eventdict = dict()
        Eventdata_list = list()
        Eventdata = Event_list.objects.values()
        Noticedata = NoticeManager.objects.values()
        # for Notice in Noticedata:
        #     # emailname[Notice["notice_leader"]] = Notice["notice_email"]
        #     status[Notice["notice_leader"]] = Notice["notice_status"]
        # print(status)
        # print(list(emailname.keys()))
        for Eet in Eventdata:
            # if Eet['event_leader'] in emailname.keys():
            # Eet['notice_email'] = emailname[Eet['event_leader']]
            # Eet['status'] = status[Eet['event_leader']]
            Eventdict['id'] = Eet['id']
            Eventdict['event_leader'] = Eet['event_leader']
            # Eventdict['notice_email'] = Eet['notice_email']
            Eventdict['event_info'] = Eet['event_info']
            # Eventdict['status'] = Eet['status']
            Eventdict['send_status'] = Eet['event_no']
            Eventmain = Eventdict.copy()
            Eventdata_list.append(Eventmain)
        return (Eventdata_list)

    def run(self):
        global NoticeManagerdata
        while True:
            event_data = eventNotice(result=Send_enent_email_tasks.event_message(self)).main()
            time.sleep(1)
            print(event_data)
            if event_data != ["AIR"]:
                print(event_data)
                if event_data != None:
                    for event in event_data:
                        # print(event['status'])
                        # if event['status'] == "1":

                        for Notice in NoticeManagerdata:
                            print(Notice)
                            if Notice['notice_status'] == "1":
                                # print(Notice['notice_status'])
                                # print(Notice)
                            # if Notice['notice_email'] == event['notice_email']:
                                Notice['notice_message_num'] = APINUMBER()

                                print(Notice['notice_message_num'])
                                # print(Notice['notice_email'])
                                NoticeManager.objects.filter(notice_status=1).update(notice_message_num=Notice["notice_message_num"])
                            if int(event['send_status']) == 0:
                                EmailManage.sendMail(content=event['event_info'], toMail=Notice['notice_email'],
                                                     sub="EdgeBox loginfo")
                                event['send_status'] = 1
                                print(event['send_status'])
                                Event_list.objects.filter(event_info=event['event_info']).update(
                                    event_no=event['send_status'])





