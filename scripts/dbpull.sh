#!/bin/bash -l

heroku pg:pull HEROKU_POSTGRESQL_MAUVE tpdata --app trackplaces
