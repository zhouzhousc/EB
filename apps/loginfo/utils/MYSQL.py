#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 15:42
# @Author  : zhuyuanbo

import time
import threading
import requests
start_time = int(time.time())

class eventNotice():
    def __init__(self,result):
        self.event_list = list()
        self.eventdata = dict()
        self.read_eventdata = list()
        self.result = result

    def connect(self):
        with open("Edgebox.txt", "a+", encoding="utf-8") as f:
            lines = f.readlines()
            f.write(str(self.result) + "\n")
            print("寫入成功")
            f.close()
        return (self.eventdata)

    def newwrite(self,name):
        global start_time
        end_time = int(time.time())
        if end_time - start_time > 10:
            with open("%s.txt"%name , "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open("%s.txt"%name, "w", encoding="utf-8") as f:
                f.write(str(lines[-1]))
                f.write(str(lines[-1]))
                print("刪除成功")
            start_time = int(time.time())

    def read(self):
        with open("Edgebox.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            lastline = lines[-1].replace("\n", "")
            secondlastline = lines[-2].replace("\n", "")
            for i in list(eval(lastline)):
                if i not in list(eval(secondlastline)):
                    # print(i)
                    self.read_eventdata.append(i)
            if self.read_eventdata == None:
                pass
                # print(self.read_eventdata)
            elif self.read_eventdata == []:
                self.read_eventdata = ["AIR"]
            elif self.read_eventdata != []:
                pass
                # print(self.read_eventdata)
            return (self.read_eventdata)

    def main(self):
            try:
                self.connect()
                neww = threading.Thread(target=self.newwrite, args=("Edgebox",))
                neww.start()
                return self.read()
            except Exception as e:
                with open("error.txt", "a", encoding="utf-8") as f:
                    f.write(str(e) + "\n")
                    f.close()


# def APINUMBER():
#     data = requests.get(url="http://10.167.198.95:9090/loginfo/Event_list/")
#     number = data.json()['count']
#     return (number)
# # A = "F1334098"
# APINUMBER(A)

def APINUMBER():
    data = requests.get(url="http://10.167.198.95:9090/loginfo/Event_list/")
    number = data.json()['count']
    return (number)
# A = "F1334098"
# APINUMBER(A)