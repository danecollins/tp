#!/bin/bash -l

heroku pg:reset database --app tpstage
heroku pg:push tpdata database --app tpstage
