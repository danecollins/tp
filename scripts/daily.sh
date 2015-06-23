#!/bin/bash -l

cd ~/src/tp
echo -n "*** " >> ~/daily.log
date >> ~/daily.log
source ~/env/tp/bin/activate

scripts/backup_prod.sh

dropdb tpdata.heroku >> ~/daily.log 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: could not drop database" 
    echo "ERROR: could not drop database" >> ~/daily.log
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
curl http://trackplaces.herokuapp.com/watch/checkin/YQTI5DDE

echo "INFO: next backup ladera database" >> ~/daily.log
cd ~/src/scripts
./backup_ladera_prod.sh >> ~/daily.log 2>&1
curl http://trackplaces.herokuapp.com/watch/checkin/12UKLQC1

