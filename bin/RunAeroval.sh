#!/bin/bash

#script to create data that is readable by pyaerocom

IFS=$(echo -en "\n\b")

usage() { echo "Usage: $0 <command to run in the container>"
        echo "examples: ${0} pya listcache"
        echo "          ${0} python <path to aeroval config file>"
        exit 0
}

if [[ $# -eq 0 ]]
   then usage
fi

abspath=$(realpath ${0})
curr_dir=$(dirname ${abspath})
. "${curr_dir}/default.env"
set -x

mamba run -n singularity singularity exec \
--bind ${PYAEROCOM_MYPYAEROCOM_PATH}:/nird/home/${USER}/MyPyaerocom \
--bind ${PYAEROCOM_DATA_PATH}:/lustre/storeB/project/aerocom/aerocom1 \
--bind ${PYAEROCOM_AEROVAL_DATA_PATH}:/nird/home/${USER}/container.data/aeroval_data \
--bind ${PYAEROCOM_AEROVAL_CONFIG_PATH}:/nird/home/${USER}/container.data/aeroval_configs \
--bind ${PYAEROCOM_CONTAINER_LOG_PATH}:/nird/home/${USER}/container.data/aeroval_logs \
--env "PYAEROCOM_LOG_FILE=${PYAEROCOM_CONTAINER_LOG_FILE}" \
"${PYAEROCOM_SIF_PATH}" \
${@}
