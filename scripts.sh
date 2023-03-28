#!/bin/sh
cd /var/www/os3-381-23528.vs.sakura.ne.jp
export GIT_SSH=~/.ssh/git-ssh.sh
python3 new_data.py > output_newdata.txt

