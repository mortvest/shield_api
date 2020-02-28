#!/usr/bin/bash
curl --request POST \
       --url http://localhost:5000/login \
       --header 'content-type: application/json' \
       --data '{"username":"user1","password":"qwerty"}'
