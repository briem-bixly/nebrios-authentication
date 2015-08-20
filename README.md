# nebrios-authentication
NebriOS Authentication Library

This app is intended for use in a NebriOS instance. Visit https://nebrios.com to sign up for free!

This app currently supports Token and Basic Access Authentication.

<h2>General Setup</h2>
This app requires very little in terms of setup. Please ensure that all files are placed in the correct places over SFTP.
  - load_authentication_token_card.py and load_authentication_basic_card.py should be copied to /scripts
  - nebrios_authentication.py should be copied to /api
  - nebrios-authentication-token.html and nebrios-authentication-basic.html should be copied to /card_html_files

<h2>Token Auth</h2>
<h4>Setup</h4>    
Once all files are in place, tokens can be created for use.
  - in debug mode set load_authentication_token_card to true and run
  
    ```
    load_authentication_token_card := True
    ```
  - this will trigger a card to load in interactive mode
  - the token input will be pre filled with a random string, but can be changed if desired
  - <strong>NOTE</strong> we recommend using a random string consisting of upper and lower case letters and numbers for tokens. This will help increase security and make it harder for attackers to gain access to your views.

<h4>Usage</h4>
Once tokens have been created for users, you will be able to restrict views. Simply add <strong>@token_required</strong> as a decorator to any view that needs permissions. This decorator can be imported from nebrios_authentication_lib.

In order to access these views, a token matching one that has been created needs to be sent with the request payload. This can be done one of 2 ways:
  - in the request body as json
  - as part of a posted form

Either method requires the keyword 'token' with a value.

<h2>Basic Auth</h2>
<h4>Setup</h4>
Once all files are in place, login pairs can be created for use.
  - in debug mode set load_authentication_basic_card to true and run
  
    ```
    load_authentication_token_card := True
    ```
  - this will trigger a card to load in interactive mode
  - once a username/password combination has been saved, users can start accessing your views!

<h4>Usage</h4>
To restrict views so users can only access them with basic authentication, simply add <strong>@basic_auth_required</strong> as a decorator to any view that needs permissions. This decorator can be imported from nebrios_authentication_lib.

When a view is hit that requires basic authentication, our server will return a 401 response and prompt your user to enter their username/password combination. Users will only get one chance to enter their password correctly before being flagged as Unauthorized.
