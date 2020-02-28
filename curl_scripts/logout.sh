curl --request POST \
     --url http://localhost:5000/logout \
     --header 'authorization: Bearer TOKEN' \
     --header 'content-type: application/json' \
     --data '{"username":"admin","password":"qwerty"}'
