#!/bin/bash
# Usage: request.sh [message]
ENDPOINT=${ENDPOINT:=localhost:8888/exampleHandler}

MESSAGE=${1:-message}
result=$(curl -X POST -H 'Content-Type: application/json' \
       -d "{ \"json_test\": \"${MESSAGE}\" }" \
       "${ENDPOINT}")
echo ${result} | jq