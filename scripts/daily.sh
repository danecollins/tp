#!/bin/bash -l

cd ~/src/tp
echo -n "*** " >> ~/daily.log
date >> ~/daily.log
source ~/env/dj/bin/activate
dropdb tpdata.heroku >> ~/daily.log 2>&1
if [ $? -ne 0 ]; then
 0   echo "ERROR: could not drop database" 
    echo "ERROR: could not drop database" >> ~/daily.log
    exit 1
fi

heroku pg:pull HEROKU_POSTGRESQL_MAUVE tpdata.heroku --app trackplaces >> ~/daily.log 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: heroku pull failed"
    echo "ERROR: heroku pull failed" >> ~/daily.log
    exit 1
fi

echo "INFO: heroku pull completed" >> ~/daily.log
export DATABASE_URL=postgres:///tpdata.heroku
scripts/dbsummary.py >> ~/daily.log 2>&1
#curl http://trackplaces.heroku.com/watch/checkin/JHUNHHH5

echo "INFO: next backup ladera database" >> ~/daily.log
cd ~/src/scripts
./backup_ladera_prod.sh >> ~/daily.log 2>&1

