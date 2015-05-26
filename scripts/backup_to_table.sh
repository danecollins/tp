#!/bin/bash -l

if [ "$1" == "" ]; then
	echo
	echo "Usage: backup_to_table filename table"
	exit 1
fi

file=$1
table=$2

echo "Restoring $file into local table $table"
createdb -T template0 $table
psql -d $table -c < $file
