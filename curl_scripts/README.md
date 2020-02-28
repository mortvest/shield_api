# curl scripts for testing
The scripts in this directory can be used to test the running system. These can
also be imported to Insomnia or similar software to make the testing easier.


# Access
### register
Registers a new user with user privileges. 
### admin_login
Logs in as a user with admin privileges. Return a JSON in requested format, with 
the access token in the "token" field.
### user_login
The same, but for the user privileges.
### logout
Logs the user out by revoking the token. Replace the TOKEN value with
a valid access token.


## User methods
The following tokens require a valid access token with user privileges,
similarly to logout.
### add_post
### add_statistic
### get_single_post
### get_multiple_posts
### get_single_statistic
### get_multiple_statistics


## Admin methods
The following tokens require a valid access token with admin privileges.
### delete_statistic
### delete_post
### change_post
### change_statistic
### get_single_user
### get_multiple_users


