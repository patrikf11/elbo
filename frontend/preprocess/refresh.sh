#!/bin/bash

# SSH_AUTH_SOCK not exported when invoked by cron make sure its set
# how to find it /usr/sbin/lsof | grep Listeners | grep ssh-agent | awk '{print $8}'
# but that freaking slow so resort to a simple ls and hope that paths wont change
 
export SSH_AUTH_SOCK=$(ls /private/tmp/*launchd*/Listeners)

cd /Users/pfm/Documents/gitrepo/elbo/frontend/preprocess
/usr/local/bin/python3 addstats.py >> refresh.log 2>&1




