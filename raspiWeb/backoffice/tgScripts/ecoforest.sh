#!/bin/bash

for ((i=0; i<10; i++)) do

  if [[ $((i % 2)) -eq 0 ]];
  then
    ENTITY="switch.ecoforestsalon"
  else
    ENTITY="switch.ecoforestsalon2"
  fi
  JSON='{"entity_id": '$ENTITY'}'
  JSON="'$JSON'"
  echo $JSON

  TOKEN="Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiZDMxNTVkOGQ5OWY0ZjIwODUzOWEzZmI0NzNjNWY0MCIsImlhdCI6MTYwOTg3OTc0MSwiZXhwIjoxOTI1MjM5NzQxfQ.Yrg9Urw7t81xc07b-O3FEBF2QgeDfeAmthnR0wOMSzo"
  TOKEN="'$TOKEN'"
  CTYPE="Content-Type: application/json"
  CTYPE="'$CTYPE'"
  URL="https://ha.sergutpal.dynu.com/api/services/switch/turn_on"
  CMD="curl -X POST -H $TOKEN -H $CTYPE -d $JSON $URL"
  echo $CMD
  eval "$CMD";
  sleep 1.5
done


