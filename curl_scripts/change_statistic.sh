#!/usr/bin/bash
curl --request PUT \
     --url http://localhost:5000/statistics/1 \
     --header 'authorization: Bearer TOKEN' \
     --header 'content-type: application/json' \
     --data '{
	"linkedin_post_id": 1,
  "num_views": 12,
  "num_likes": 13,
  "num_comments": 14
}'
