#!/usr/bin/env python

import glob

if __name__ == "__main__":

    badFiles = 'cleaner/badRuns.txt'
    with open(badFiles, 'r') as f:
        badJobs = f.readlines()
    badJobs = [badJob.strip() for badJob in badJobs]
    
    for badJob in badJobs:
        badFile = 'npx4-execs/%s.sh' % badJob
        with open(badFile, 'r') as f:
            lines = f.readlines()

        print badFile
        errfile = badFile.replace('execs','error')
        errfile = errfile.replace('.sh','.error')
        with open(errfile, 'r') as f:
            lines = f.readlines()
        for l in lines:
            if l == '\n':
                continue
            if l.split()[0] not in ['INFO','NOTICE','WARN']:
                print l
