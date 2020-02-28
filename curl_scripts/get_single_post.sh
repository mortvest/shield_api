#!/usr/bin/bash
curl --request GET \
     --url http://localhost:5000/posts/1 \
     --header 'authorization: Bearer TOKEN'
