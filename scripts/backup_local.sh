#!/bin/bash -l

DATE=`date +%Y-%m-%d`
pg_dump tpdata > backup_tpdata_$DATE
