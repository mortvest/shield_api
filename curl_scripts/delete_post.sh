#!/usr/bin/bash
curl --request DELETE \
     --url http://localhost:5000/posts/1 \
     --header 'authorization: Bearer TOKEN'
