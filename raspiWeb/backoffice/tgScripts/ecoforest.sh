#!/bin/bash

for ((i=0; i<15; i++)) do

  if [[ $((i % 2)) -eq 0 ]];
  then
    curl -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiZDMxNTVkOGQ5OWY0ZjIwODUzOWEzZmI0NzNjNWY0MCIsImlhdCI6MTYwOTg3OTc0MSwiZXhwIjoxOTI1MjM5NzQxfQ.Yrg9Urw7t81xc07b-O3FEBF2QgeDfeAmthnR0wOMSzo" \
      -H "Content-Type: application/json" -d '{"entity_id": "switch.ecoforestsalon"}' https://ha.sergutpal.dynu.com/api/services/switch/turn_on
  else
    curl -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiZDMxNTVkOGQ5OWY0ZjIwODUzOWEzZmI0NzNjNWY0MCIsImlhdCI6MTYwOTg3OTc0MSwiZXhwIjoxOTI1MjM5NzQxfQ.Yrg9Urw7t81xc07b-O3FEBF2QgeDfeAmthnR0wOMSzo" \
      -H "Content-Type: application/json" -d '{"entity_id": "switch.ecoforestsalon2"}' https://ha.sergutpal.dynu.com/api/services/switch/turn_on
  fi
  sleep 1.1
done


