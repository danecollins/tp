#!/bin/bash -l

#COPY [ BINARY ] table_name [ WITH OIDS ]
#TO { 'filename' | STDOUT }
#[ [USING] DELIMITERS 'delimiter' ]
#[ WITH NULL AS 'null string' ]

echo "id,date,male,experiment" > votes.txt
psql -d tpdata -c "COPY vote_vote TO STDOUT DELIMITERS ','" >> votes.txt



