#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Hanyuan Liu, All rights reserved.
# Use of this source code is governed by a GNU v2 license that can be
# found in the LICENSE file.
#
# coding:utf-8

import sys
import os

import re
import subprocess
import time
import psutil
import socket

from lcd2usb import LCD, SMILE_SYMBOL
RE_UPTIME = re.compile('(.*?)\s+up\s+(.*?),\s+(\d+) users?,\s+'
                       'load averages?: (\d+\.\d+),?'
                       '\s+(\d+\.\d+),?\s+(\d+\.\d+)')


def getCPUstate(sleeptime=1):
    return (str(psutil.cpu_percent(sleeptime)) + "%")

def getMemstate():
    return (str(psutil.virtual_memory().percent) + "%")

def getIPaddr():
	return str((socket.gethostbyname(socket.gethostname())))

def load_uptime():
    info = subprocess.check_output('uptime')
    _, duration, users, avg1, avg5, avg15 = RE_UPTIME.match(info).groups()
    days = '0'
    hours = '0'
    mins = '0'
    if 'day' in duration:
        match = re.search('([0-9]+)\s+day', duration)
        days = str(int(match.group(1)))
    if ':' in duration:
        match = re.search('([0-9]+):([0-9]+)', duration)
        hours = str(int(match.group(1)))
        mins = str(int(match.group(2)))
    if 'min' in duration:
        match = re.search('([0-9]+)\s+min', duration)
        mins = str(int(match.group(1)))
    return int(days), int(hours), int(mins), int(users)


def main(lcd):
    lcd.clear()
    while True:
        #row0_WelcomInfo
        lcd.fill('-   Welcome Info   -',0)
        #row1_IPaddr
        lcd.write(getIPaddr(),4,1)
        #row2_CPU+Men_Status
        load= "CPU: " + getCPUstate() + "|Men: " + getMemstate()
        lcd.fill(load,2)
        #row3_upTime+UserNum
        days, hours, mins, users = load_uptime()
        if days:
            row3 = 'UP %d Days' % days
        elif hours:
            row3 = 'UP %d Hours' % hours
        else:
            row3 = 'UP %d Mins' % mins
        row3 += ', %d Users' % users
        lcd.fill(row3, 3)
        time.sleep(1)
        lcd.fill('|   Welcome Info   |',0)
        time.sleep(1)



if __name__ == '__main__':
    lcd = LCD.find_or_die()
    lcd.set_brightness(100)
    lcd.set_contrast(35)
    try:
        main(lcd)
    except KeyboardInterrupt:
        pass
    