from nebriosauthenticationmodels import Token, BasicAuth, OAuth
from nebrios_authentication_lib import token_required, basic_auth_required, oauth_required
import logging
import json
import string
import random

logging.basicConfig(filename='token_errors.log', level=logging.DEBUG)


def update_token(request):
    t = None
    created = False
    try:
        t = Token.get(token=request.FORM.token)
    except Process.DoesNotExist:
        try:
            t = Token.get(description=request.FORM.description)
        except Process.DoesNotExist:
            t = Token(
                token=request.FORM.token,
                description=request.FORM.description,
                realm=request.FORM.realm
            )
            created = True

    if not created and t is not None:
        t.token = request.FORM.token
        t.description = request.FORM.description
        t.realm = request.FORM.realm
    t.save()


def update_basic(request):
    b = None
    created = False
    try:
        b = BasicAuth.get(username=request.FORM.username)
    except Process.DoesNotExist:
        b = BasicAuth(
            username=request.FORM.username,
            realm=request.FORM.realm
        )
        b.set_password(request.FORM.pw)
        request.FORM.pw = ''
        created = True
    if not created and b is not None:
        b.username = request.FORM.username
        b.realm = request.FORM.realm
        b.set_password(request.FORM.pw)
    b.save()


def update_oauth(request):
    o = None
    created = False
    try:
        o = OAuth.get(username=request.user)
    except Process.DoesNotExist:
        o = OAuth(
            username=request.user,
            consumer_key=request.FORM.consumer_key,
            consumer_secret=request.FORM.consumer_secret,
            scope=request.FORM.scope
        )
        created = True

    if not created and o is not None:
        o.consumer_key = request.FORM.consumer_key
        o.consumer_secret = request.FORM.consumer_secret
        o.realm = request.FORM.realm
    o.save()


def get_oauth_token(request):
    try:
        oauth_info = OAuth.get(consumer_key=request.POST['key'])
    except Process.DoesNotExist:
        try:
            oauth_info = OAuth.get(consumer_key = request.BODY['key'])
        except:
            return HttpResponseForbidden
    if oauth_info.consumer_secret == request.POST['secret']:
        pass
    elif oauth_info.consumer_secret == request.BODY['secret']:
        pass
    else:
        return HttpResponseForbidden
    oauth_info.token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(45))
    oauth_info.save()
    return HttpResponse(json.dumps({'token_type': 'bearer', 'access_token': oauth_info.token}), content_type="application/json")


@token_required(realm='')
def test_endpoint(request):
    logging.debug(request.POST)
    logging.debug('lol test')


@token_required(realm='test')
def test_token(request):
    logging.debug('wooo')


@basic_auth_required(realm='')
def other_test(request):
    logging.debug(request.POST)


@basic_auth_required(realm="basic")
def test_basic(request):
    logging.debug('yay!')


@oauth_required(realm='')
def another_test(request):
    logging.debug(request.POST)


@oauth_required(realm='oauth')
def test_oauth(request):
    logging.debug('excellent')