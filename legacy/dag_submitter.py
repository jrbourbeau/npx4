#!/usr/bin/env python

##============================================================================##
## Writes submission script for cluster
##============================================================================##

import os
import time
import glob

def py_submit(executable, arglist, npx4dir, jobID=None, 
              maxjobs=1000, sublines=None, test=False):

    if test:
        print '(...running as test off the cluster...)'
        for a in arglist[:2]:
            os.system('{} {}'.format(executable, a.strip()))
        raise SystemExit('Completed testing run...')

    # Moderate number of submitted jobs
    njobs = len(arglist)
    if njobs > maxjobs:
        yn = raw_input(
            'About to submit {} jobs at {} maxjobs.\
                    Are you sure? [y|n]: '.format(njobs, maxjobs))
        if yn != 'y':
            raise SystemExit('Aborting...')

    # Add date information
    if jobID is not None:
        jobID += time.strftime('_%Y%m%d')
        othersubmits = glob.glob('{}/logs/{}_??.log'.format(npx4dir, jobID))
        jobID += '_{:02d}'.format(len(othersubmits)+1)
      
    # Condor submission script
    lines = [
        "universe = vanilla\n",
        "getenv = true\n",
        "executable = {}\n".format(executable),
        "arguments = $(ARGS)\n",
        "log = {}/logs/{}.log\n".format(npx4dir, jobID),
        "output = {}/outs/{}.out\n".format(npx4dir, jobID),
        "error = {}/errors/{}.error\n".format(npx4dir, jobID),
        "notification = Never\n",
        "queue \n"
    ]
    # Option for additional lines to submission script
    if sublines != None:
        for l in sublines:
            lines.insert(-1, '{}\n'.format(l))

    condor_script = '{}/submit-desc.sub'.format(npx4dir)
    with open(condor_script, 'w') as f:
        f.writelines(lines)

    # Create dag file
    dag_file = '{}/dags/{}_dag.submit'.format(npx4dir, jobID)
    with open(dag_file, 'w') as dag:
        for i, arg in enumerate(arglist):
            dag.write("JOB " + str(i) + " " + condor_script + "\n")
            dag.write("VARS " + str(i) + " ARGS=\"" + arg + "\"\n")

    os.system('condor_submit_dag -maxjobs {} {}'.format(maxjobs, dag_file))
