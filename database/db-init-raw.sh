#!/bin/bash
#
# Init, database schema for raw harvested values. USE WITH CARE! IT DELETES ALL HISTORY!
#

. common.sh

psql -h ${PGHOST} ${PGDB} -f schema/db-schema-raw.sql
