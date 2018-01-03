#!/bin/bash
#
# Update feature geometry from refined table stations last location
# An Enormous Hack: but there is no way to achieve this via the SOS Protocol!
#
# See issue https://github.com/Geonovum/smartemission/issues/72

SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}
. common.sh

psql -h ${PGHOST} ${PGDB} -f sos-update-feature-geom.sql

popd