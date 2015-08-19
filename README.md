# nebrios-authentication
NebriOS Authentication Library

This app is intended for use in a NebriOS instance. Visit https://nebrios.com to sign up for free!

<h4>Setup</h4>
This app requires very little in terms of setup. Please ensure that all files are placed in the correct places over SFTP.
  - load_authentication_token_card.py should be copied to /scripts
  - nebrios_authentication.py should be copied to /api
  - nebrios-authentication-token.html should be copied to /card_html_files
    
Once all files are in place, tokens should be created for use.
  - in debug mode set load_authentication_token_card to true and run
  
    ```
    load_authentication_token_card := True
    ```
  - this will trigger a card to load in interactive mode
  - the token input will be pre filled with a random string, but can be changed if desired
  - <strong>NOTE</strong> we recommend using a random string consisting of upper and lower case letters and numbers for tokens. This will help increase security and make it harder for attackers to gain access to your views.

<h4>Usage</h4>
Once tokens have been created for users, you will be able to restrict views. Simply add <strong>@token_required</strong> as a decorator to any view that needs permissions.

In order to access these views, a token matching one that has been created needs to be sent with the request payload. This can be done one of 2 ways:
  - in the request body as json
  - as part of a posted form

Either method requires the keyword 'token' with a value.


