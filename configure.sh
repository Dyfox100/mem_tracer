#!/bin/bash
#set -x
yaml() {
    python3 -c "import yaml;print(yaml.safe_load(open('$1'))['$2'][0])"
}

export OUTPUT_VOL=$(yaml configuration.yaml output_volume)
export PROGRAM_VOL=$(yaml configuration.yaml programs_volume)
envsubst < ./templates/compose.tmpl > ./docker-compose.yaml
docker volume create --name=output
export SECTIONS_TO_TRACE=$(yaml configuration.yaml sections_to_trace)
TO_REPLACE='$SECTIONS_TO_TRACE'
envsubst "$TO_REPLACE" < ./templates/run_traces.tmpl > ./run_traces.sh
