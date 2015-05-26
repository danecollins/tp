Track Places Project
====================

## Goals
* Store places, such as restaurants, organized by locale and city
* Allow you to store metadata such as ratings and dog friendlyness
* Allow you to share a place with a friend (with or without your metadata)

## Status
* First beta release deployed on heroku

## Utility Scripts
* daily.sh
  * drops the local database tpdata and then imports it from heroku's tpdata
  * then runs dbsummary to post dbstats to slack

* backup\_local.sh
  * dumps the local tpdata to a text file

* backup\_prod.sh
  * dumps the heroku database

* backup\_to\_table.sh
  * loads a file into a table

* dbpull.sh
  * copies the heroku database into the local tpdata database

* dbpush.sh
  * copies the local tpdata database into the tpstage database

## Environment Notes

* There are 2 requirements files.
  * requirements.txt are the requirements to deploy the site
  * requirements.dev contains the development/test requirements
* There are 2 config.settings files
  * settings.py contains the deployment settings
  * settings\_test.py contains the development settings
    * set DJANGO\_SETTINGS\_MODULE=config.settings\_test to use
    * requires that you set DB to the name of the database you want to use
      * currently can only be tpdata or tpdata_test
