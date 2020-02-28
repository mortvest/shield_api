#!/usr/bin/bash
curl --request GET \
     --url http://localhost:5000/user/1/posts \
     --header 'authorization: Bearer TOKEN'
