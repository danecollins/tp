#!/bin/bash -l

cd ~/src/tp
echo -n "*** " >> daily.log
date >> daily.log
source ~/env/dj/bin/activate
dropdb tpdata >> daily.log 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: could not drop database" 
    echo "ERROR: could not drop database" >> daily.log
    exit 1
fi

heroku pg:pull HEROKU_POSTGRESQL_MAUVE tpdata --app trackplaces >> daily.log 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: heroku pull failed"
    echo "ERROR: heroku pull failed" >> daily.log
    exit 1
fi

echo "INFO: heroku pull completed" >> daily.log
scripts/dbsummary.py >> daily.log 2>&1
