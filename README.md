Track Places Project
====================

## Goals
* Store places, such as restaurants, organized by locale and city
* Allow you to store metadata such as ratings and dog friendlyness
* Allow you to share a place with a friend (with or without your metadata)

## Status
* First beta release deployed on heroku

## Todo
TODO: User registration form
TODO: Add cancel button to edit form
TODO: Get rid of <hr> in login page
TODO: Need a way to share a place, can do by url but no UI
TODO: Create a read-only demo account

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
