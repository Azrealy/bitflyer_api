#!/bin/bash 
#Usage: getbitflyer,sh [urlname]

URLNAME=${1:-urlname}
result=$(curl -X GET "https://api.bitflyer.jp/v1/${URLNAME}")

echo ${result} | jq
