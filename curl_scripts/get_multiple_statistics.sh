#!/usr/bin/bash
curl --request GET \
     --url http://localhost:5000/statistics \
     --header 'authorization: Bearer TOKEN'
