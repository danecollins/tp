#!/bin/bash -l

cd /Users/dane/src/tp/scripts/

DATE=`date +%Y-%m-%d_%H%M%S`
pg_dump --dbname=$HPG_PROD_DBNAME --host=$HPG_PROD_HOST --username=$HPG_PROD_UNAME > db.prod.$DATE

