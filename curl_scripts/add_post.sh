#!/usr/bin/bash
curl --request POST \
     --url http://localhost:5000/posts \
     --header 'authorization: Bearer TOKEN' \
     --header 'content-type: application/json' \
     --data '{"user_id": 1, "content": "Content 3"}'
