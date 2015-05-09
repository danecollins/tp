#!/bin/bash -l

DATE=`date +%Y-%m-%d_%H%M%S`
pg_dump tpdata > db.backup.$DATE
