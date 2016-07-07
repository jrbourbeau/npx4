#!/usr/bin/env python

import glob, os

if __name__ == "__main__":

    prefix = os.getcwd()
    badList = prefix + '/cleaner/badRuns.txt'
    with open(badList, 'r') as f:
        badRuns = f.readlines()
        badRuns.sort()

    for jobID in badRuns:

        # Extract jobID number and recreate full file path
        jobID = jobID.strip()
        badexec = prefix + '/npx4-execs/'+jobID+'.sh'

        # Condor submission script
        lines = [
            "Universe = vanilla\n",
            "Executable = npx4-execs/%s.sh\n" % jobID,
            "Log = npx4-logs/%s.log\n" % jobID,
            "Output = npx4-out/%s.out\n" % jobID,
            "Error = npx4-error/%s.error\n" % jobID,
            "Notification = NEVER\n",
            "Queue\n"
        ]

        with open('2sub.sub', 'w') as f:
            f.writelines(lines)

        os.system('condor_submit %s' % '2sub.sub')



    
