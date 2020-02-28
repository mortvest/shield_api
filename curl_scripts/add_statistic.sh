#!/usr/bin/bash
curl --request POST \
     --url http://localhost:5000/statistics \
     --header 'authorization: Bearer TOKEN' \
     --header 'content-type: application/json' \
     --data '{
	"linkedin_post_id": 2,
  "num_views": 12,
  "num_likes": 13,
  "num_comments": 14
}'
