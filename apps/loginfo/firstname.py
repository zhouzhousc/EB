#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 16:20 
# @Author  : zhuyuanbo






import requests

from wangguang.tasks import Agent_sys_init_tasks

Agent_sys_init_tasks.delay()  #觸發