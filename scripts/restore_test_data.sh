#!/bin/bash -l

file=test_data.db

echo 'Restoring tpdata_test from file $file'
pg_restore --dbname=tpdata_test --clean $file
