#!/usr/bin/bash
curl --request POST \
     --url http://localhost:5000/register \
     --header 'content-type: application/json' \
     --data '{"username":"user3",
 "password":"qwerty",
 "first_name": "Tom",
 "last_name": "Johns"}'
