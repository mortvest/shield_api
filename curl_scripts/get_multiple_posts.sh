#!/usr/bin/bash
curl --request GET \
     --url http://localhost:5000/posts \
     --header 'authorization: Bearer TOKEN'
