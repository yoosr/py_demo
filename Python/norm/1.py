#!/usr/bin/python
# -*- coding:UTF-8 -*-
#Author liusonglin
#20090807
import sys
import os
import time
import datetime
import string
from ftplib import FTP

def getLstMonth():
    d=datetime.datetime.now()
    
    year=d.year
    month=d.month

    if month==1:
	month=12
	year-=1
    else:
	month-=1
    return datetime.datetime(year,month,1).strftime('%Y-%m')

dd = getLstMonth()
ftp=FTP()
ftp.set_debuglevel(2)
ftp.connect('21.40.3.198',)
ftp.login()
#ftp.dir()
ftp.cwd('01.PYID0030')
#ftp.dir()
nlist=ftp.nlst()
for subdir in nlist:
    if string.find(subdir,dd)==0:
	print subdir
#print getLstMonth()
