#!/usr/bin/env python

import subprocess, os, getpass, glob
import myGlobals as my

def getFinished(prefix):

    user = getpass.getuser()
    bashCommand = 'condor_q %s -wide' % user
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    output = [i.strip() for i in output.split('\n')]

    # Make sure call to condor went correctly
    for phrase in ['jobs','completed','removed','idle','running','held']:
        if phrase not in output[-2]:
            print 'Fetch from condor failed'
            return []
    #0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended

    # Get a list of files running
    running = []
    for line in output:
        jobID = line.strip().split(' ')[-1]
        if jobID[-3:] != '.sh':
            continue
        running.append(jobID)

    # Get a list of files submitted
    submittedFiles = glob.glob('%s/npx4-execs/*.sh' % prefix)
    submittedFiles = [os.path.basename(f) for f in submittedFiles]

    # Find out which submitted files have finished
    finished = []
    for jobID in submittedFiles:
        if jobID not in running and jobID != '':
            finished.append(jobID)

    return finished


if __name__ == "__main__":

    my.setupGlobals(verbose=False)
    finished = getFinished(my.npx4)
    print len(finished), 'finished files:'
    print finished
