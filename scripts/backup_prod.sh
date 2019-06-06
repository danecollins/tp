#!/bin/bash -l

source /Users/dane/env/tp/bin/activate
source /Users/dane/dropbox/osx/env_vars/tp_vars

DATE=`date +%Y-%m-%d`
backup_file=/Users/dane/dropbox/dacxl/TrackPlaces/backups/heroku_tpdata.$DATE

echo "backing up $HPG_PROD_DBNAME"
export PGPASSWORD=$HPG_PROD_PASS

pg_dump --dbname=$HPG_PROD_DBNAME --host=$HPG_PROD_HOST --username=$HPG_PROD_UNAME -F c -f $backup_file
curl -L http://w4e.herokuapp.com/checkin/9YZNCBAR/

