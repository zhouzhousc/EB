#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 17:46
# @Author  : userzhang

import datetime

import time
from celery.task import Task
import django
django.setup()


from http.client import HTTPConnection
import json

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


class Send_register_email_tasks(Task):
    name = "Send_register_email_tasks"

    def run(self, receiver, subject, html_message):
        '''定义任务函数 注册用户时发送Email'''
        EmailManage.sendMail(receiver, subject, html_message)
        return True


