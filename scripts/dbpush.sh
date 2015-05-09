#!/bin/bash -l

heroku pg:push tpdata HEROKU_POSTGRESQL_MAUVE --app trackplaces
