#!/bin/bash -l

cd ~/src/tp
date >> daily.log
source ~/env/dj/bin/activate
dropdb tpdata >> daily.log 2>&1
heroku pg:pull HEROKU_POSTGRESQL_MAUVE tpdata --app trackplaces >> daily.log 2>&1
scripts/dbsummary.py >> daily.log 2>&1
