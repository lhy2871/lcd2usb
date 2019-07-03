#
# Copyright (c) 2019, Hanyuan Liu, All rights reserved.
# Use of this source code is governed by a GNU v2 license that can be
# found in the LICENSE file.
#
#Modified from Lambo Wang <lambo.wang@icloud.com>
# -*- coding: utf-8 -*-
# coding:utf-8

import sys
import os

import time
import psutil
import socket

def getCPUstate(interval=1):
    return (str(psutil.cpu_percent(interval)) + "%")

def getMemorystate():
    return (str(psutil.virtual_memory().percent) + "%")

def getIPaddr():
	local = socket.getfqdn(socket.gethostname())
	return (socket.gethostbyname(local))

def poll(interval):
    time.sleep(interval)
    cpu_state = getCPUstate(interval)
    memory_state = getMemorystate()
    ipaddr = getIPaddr()
    return (cpu_state, memory_state, ipaddr)

def refresh_window(cpu_state, memory_state, ipaddr):
    os.system("clear")
    print (ipaddr)
    print (cpu_state + "|" + memory_state)

try:
    interval = 0
    while 1:
        args = poll(interval)
        refresh_window(*args)
        interval = 1
except (KeyboardInterrupt, SystemExit):
    pass