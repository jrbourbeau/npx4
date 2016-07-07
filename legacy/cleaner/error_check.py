#!/usr/bin/env python

#######################################################
# Runs through error files, returns a list of files where the process ran
# correctly for elimination with cleaner
#######################################################

from finished import getFinished
from getTime import getTime
import os, sys, re

if __name__ == "__main__":

    prefix = sys.argv[1]
    fileList = getFinished(prefix)

    goodRuns, badRuns, tList = [],[],[]
    t = 0.

    oks = ['NOTICE','INFO','WARN']

    # Append to safeErrors any errors you want to ignore
    safeErrors = []
    # General safe errors
    safeErrors.append('Error in <TSystem::ExpandFileName>: input: $HOME/.root.mimes, output: $HOME/.root.mimes')
    # IceTop time-scrambling errors
    safeErrors.append('Error in <TTree::SetBranchStatus>: unknown branch -> ShowerLLH_proton.energy')
    safeErrors.append('Error in <TTree::SetBranchStatus>: unknown branch -> ShowerLLH_iron.energy')
    safeErrors.append('Error in <TTree::SetBranchStatus>: unknown branch -> maxLLH_proton.value')
    safeErrors.append('Error in <TTree::SetBranchStatus>: unknown branch -> maxLLH_iron.value')
    safeErrors.append('Error in <TTree::SetBranchStatus>: unknown branch -> LaputopStandardParams.s125')
    safeErrors.append('Error in <TTree::SetBranchStatus>: unknown branch -> LaputopSmallShowerParams.s125')

    for file in fileList:

        # Find the jobID
        jobID = re.split('/|\.', file)[-2]
        # Ensure that it has an error file
        if not os.path.isfile('%s/npx4-error/%s.error' % (prefix, jobID)):
            os.system('rm -rf %s/npx4-*/%s.*' % (prefix, jobID))
            continue

        # Check the error file for any lines that aren't harmless
        isGood = True
        errFile = '%s/npx4-error/%s.error' % (prefix, jobID)
        with open(errFile, 'r') as f:
            err = f.readlines()
        err = [line.strip() for line in err]
        # Remove non-error-related I3Tray output
        err = [l for l in err if l.split(' ')[0] not in oks]
        if any([line not in safeErrors for line in err]):
            isGood = False

       # Check to make sure timing calculation works
        t0 = getTime('%s/npx4-logs/%s.log' % (prefix, jobID))

        # Append run number to good or bad run list
        if isGood and t0:
            goodRuns.append(jobID)
            t += t0
            tList += [t0]
        else:
            badRuns.append(jobID)

    if len(goodRuns) != 0:
        print 'Average time per job for good runs:', t/len(goodRuns), 'seconds'
        tList.sort()
        print 'Min time:', tList[0]
        print 'Max time:', tList[-1]

    # Write good and bad run lists to a text file
    f = open(prefix + '/cleaner/goodRuns.txt', 'w')
    f.write('')
    for run in goodRuns:
        f.write(run + '\n')
    f.close()

    f = open(prefix + '/cleaner/badRuns.txt', 'w')
    f.write('')
    for run in badRuns:
        f.write(run + '\n')
    f.close()
