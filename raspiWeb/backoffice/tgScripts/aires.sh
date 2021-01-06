#!/bin/bash

curl -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiZDMxNTVkOGQ5OWY0ZjIwODUzOWEzZmI0NzNjNWY0MCIsImlhdCI6MTYwOTg3OTc0MSwiZXhwIjoxOTI1MjM5NzQxfQ.Yrg9Urw7t81xc07b-O3FEBF2QgeDfeAmthnR0wOMSzo" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.acpasillo"}' \
  https://ha.sergutpal.dynu.com/api/services/switch/turn_on

sleep 2

curl -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiZDMxNTVkOGQ5OWY0ZjIwODUzOWEzZmI0NzNjNWY0MCIsImlhdCI6MTYwOTg3OTc0MSwiZXhwIjoxOTI1MjM5NzQxfQ.Yrg9Urw7t81xc07b-O3FEBF2QgeDfeAmthnR0wOMSzo" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.acsalon"}' \
  https://ha.sergutpal.dynu.com/api/services/switch/turn_on
