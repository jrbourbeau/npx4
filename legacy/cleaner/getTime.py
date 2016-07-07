#!/usr/bin/env python

import re, datetime

def extractTime(line):

    dateFormat = re.compile('\d{2}/\d{2}')
    timeFormat = re.compile('\d{2}:\d{2}:\d{2}')
    d0 = dateFormat.findall(line)[0]
    t0 = timeFormat.findall(line)[0]

    # Extract month, day, and time
    mm, dd = int(d0[:2]), int(d0[3:])
    hrs, min, sec = int(t0[:2]), int(t0[3:5]), int(t0[6:])

    # Get the year
    now = datetime.datetime.now()
    yy = now.year

    t = datetime.datetime(yy, mm, dd, hrs, min, sec)

    return t
    
    

def getTime(file):

    fl = open(file, 'r')
    lines = fl.readlines()
    fl.close()

    startLines = [line for line in lines if 'Job executing on host:' in line]
    endLines = [line for line in lines if 'Job terminated' in line]
    if startLines == [] or endLines == []:
        return False

    startLine = startLines[0]
    endLine = endLines[-1]
    startTime = extractTime(startLine)
    endTime = extractTime(endLine)
    dt = endTime - startTime
    dt = dt.total_seconds()
    
    return dt

