#!/usr/bin/bash
curl --request DELETE \
     --url http://localhost:5000/statistics/2 \
     --header 'authorization: Bearer TOKEN'
