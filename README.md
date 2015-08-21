# nebrios-authentication
NebriOS Authentication Library

This app is intended for use in a NebriOS instance. Visit https://nebrios.com to sign up for free!

This app currently supports Token, Basic Access, and App-Only OAuth2 Authentication.

Example functions can be found at the end.

<h2>General Setup</h2>
This app requires very little in terms of setup. Please ensure that all files are placed in the correct places over SFTP.
  - load_authentication_token_card.py, load_authentication_oauth_card.py, and load_authentication_basic_card.py should be copied to /scripts
  - nebrios_authentication.py should be copied to /api
  - nebrios-authentication-token.html, nebrios-authentication-oauth.html, and nebrios-authentication-basic.html should be copied to /card_html_files

<h2>Token Auth</h2>
<h4>Setup</h4>    
Once all files are in place, tokens can be created for use.
  - in debug mode set load_authentication_token_card to true and run
  
    ```
    load_authentication_token_card := True
    ```
  - this will trigger a card to load in interactive mode
  - the token input will be pre filled with a random string, but can be changed if desired
  - realm is not required, but can be filled out to enforce ACL for what users can access different api endpoints/apps
  - <strong>NOTE</strong> we recommend using a random string consisting of upper and lower case letters and numbers for tokens. This will help increase security and make it harder for attackers to gain access to your views.

<h4>Usage</h4>
Once tokens have been created for users, you will be able to restrict views. Simply add <strong>@token_required(realm=<realm>)</strong> as a decorator to any view that needs permissions. This decorator can be imported from nebrios_authentication_lib. Realm can be set to any string. An empty string is a valid argument and will only grant permission to people that do not have a realm specified.

In order to access these views, a token matching one that has been created needs to be sent with the request payload. This can be done one of 2 ways:
  - in the request body as json
  - as part of a posted form

Either method requires the keyword 'token' with a value.

<h2>Basic Auth</h2>
<h4>Setup</h4>
Once all files are in place, login pairs can be created for use.
  - in debug mode set load_authentication_basic_card to true and run
  
    ```
    load_authentication_basic_card := True
    ```
  - this will trigger a card to load in interactive mode
  - once a username/password combination has been saved, users can start accessing your views!
  - realm is not required, but can be filled out to enforce ACL for what users can access different api endpoints/apps

<h4>Usage</h4>
To restrict views so users can only access them with basic authentication, simply add <strong>@basic_auth_required(realm=<realm>)</strong> as a decorator to any view that needs permissions. This decorator can be imported from nebrios_authentication_lib. Realm can be set to any string. An empty string is a valid argument and will only grant permission to people that do not have a realm specified.

When a view is hit that requires basic authentication, our server will return a 401 response and prompt your user to enter their username/password combination. Users will only get one chance to enter their password correctly before being flagged as Unauthorized.

<h2>App-Only OAuth</h2>
<h4>Setup</h4>
Once all files are in place, consumer key/secret pairs can be generated for use.
  - in debug mode set load_authentication_oauth_card to true and run
  
  ```
  load_authentication_oauth_card := True
  ```
  - this will trigger a card to load in interactive mode
  - the consumer key and consumer secret fields will be auto filled with generated strings and should be saved for your app to use later
  - scope is not required, but can be filled out with any string to enforce ACL for what users can access different api endpoints/apps

<h4>Usage</h4>
To restrict views so users can only access them with app-only OAuth authentication, simply add <strong>@oauth_required(realm=<realm>)</strong> as a decorator to any view that needs permissions. This decorator can be imported from nebrios_authentication_lib. Realm can be set to any string. An empty string is a valid argument and will only grant permission to people that do not have a realm specified.

Before a view with oauth authentication can be hit, a token needs to be generated. This is done by sending your consumer key and consumer secret via a POST request to /api/v1/nebrios_authentication/get_oauth_token.

```
requests.POST('/api/v1/nebrios_authentication/get_oauth_token', data={'key':<consumer_key>, 'secret':<consumer_secret>})
```
- if the consumer key/secret match up with our records, you will receive a response similar to the following:

```
{'token_type':'bearer', 'access_token':<access_token>}
```
- the returned access_token is what your app should send to oauth protected views

```
requests.POST('/api/v1/<api_module>/<protected_api_endpoint>', data={'access_token':<access_token>,....})
```
- <strong>NOTE:</strong> generating an access token and submitting your access token can be done through a raw JSON BODY request or from a form submission

<strong>NOTE:</strong> Attempting to access a protected view before generating an access token will result in a 403 Forbidden response.


<h2>Examples</h2>

```
@token_required(realm='')
def protected_api_endpoint(request):
    print 'welcome to this protected endpoint!'
    
@token_required(realm='admin')
def admin_view(request):
    print 'this is an admin view'
```
In this example, we have two token protected endpoints. User token entries with a blank realm will be able to access the first endpoint, while user token entries with a realm set to 'admin' will be able to access the second endpoint. This applies to all authentication methods.
