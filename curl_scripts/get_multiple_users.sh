#!/usr/bin/bash
curl --request GET \
     --url http://localhost:5000/user \
     --header 'authorization: Bearer TOKEN'
