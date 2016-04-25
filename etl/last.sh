#!/bin/bash
#
# ETL for reading last values from Smart Emission CityGIS Raw Sensor API
#

STETL_ARGS="-c last.cfg -a options/docker.args"
WORK_DIR="`pwd`"
PG_HOST=postgis
NAME="stetl"

# Stop and remove possibly old containers
sudo docker stop ${NAME} > /dev/null 2>&1
sudo docker rm ${NAME} > /dev/null 2>&1

sudo docker run --name ${NAME} --link ${PG_HOST}:${PG_HOST} -v ${WORK_DIR}:${WORK_DIR} -w ${WORK_DIR} -t -i geonovum/stetl ${STETL_ARGS}
