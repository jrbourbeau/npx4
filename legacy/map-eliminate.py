#!/usr/bin/env python

import os, glob
import myGlobals as my

if __name__ == "__main__":

    my.setupGlobals(verbose=False)

    eliminateList = []
    badFile = '%s/cleaner/badRuns.txt' % my.npx4
    with open(badFile, 'r') as f:
        jobIDs = f.readlines()
    jobIDs = [jobID.strip() for jobID in jobIDs]

    badFiles = []
    for jobID in jobIDs:
        badFiles += glob.glob('%s/npx4-*/%s.*' % (my.npx4, jobID))

    for errFile in badFiles:

        with open(errFile, 'r') as f:
            lines = f.readlines()

        # Isolate lines with a given prefix
        prefix = '/data/user/fmcnally/anisotropy/maps'
        suffix = '.fits'
        lines = [l.strip() for l in lines if prefix in l]
        if lines == []:
            continue

        badOutput = [i for l in lines for i in l.split() if prefix in i]
        badOutput = [i for i in badOutput if suffix in i]
        #badOutput = lines[0]
        for f in badOutput:
            print f
            if os.path.isfile(f):
                print 'Found', f
                eliminateList += [f]

    eliminateList = list(set(eliminateList))
    if len(eliminateList) != 0:

        print 'The following files will be deleted:'
        for f in eliminateList:
            print '  %s' % f
        yn = raw_input('Continue [y|n]?:  ')
        if yn == 'y':
            for f in eliminateList:
                os.remove(f)
        
