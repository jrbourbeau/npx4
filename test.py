#!/usr/bin/env python

import glob, os

if __name__ == "__main__":

    badFile = 'cleaner/badRuns.txt'
    with open(badFile, 'r') as f:
        badRuns = f.readlines()
        badRuns.sort()

    for jobID in badRuns:
 
        jobID = jobID.strip()
        badexec = 'npx4-execs/%s.sh' % jobID

        with open(badexec,'r') as f:
            lines = f.readlines()
        exeLine = lines[-2].strip().split(' ')
        idx = exeLine.index('-f')
        inFile = exeLine[idx+1]
        #if os.path.isfile(inFile):
        print 'File with trouble: %s' % inFile
        #os.remove(inFile)

