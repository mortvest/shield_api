#!/usr/bin/bash
curl --request GET \
     --url http://localhost:5000/statistics/1 \
     --header 'authorization: Bearer TOKEN'
