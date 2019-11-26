#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/6 16:46
# @Author  : userzhang
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



