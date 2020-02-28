#!/usr/bin/bash
curl --request PUT \
     --url http://localhost:5000/posts/3 \
     --header 'authorization: Bearer TOKEN' \
     --header 'content-type: application/json' \
     --data '{"content": "Changed content"}'
