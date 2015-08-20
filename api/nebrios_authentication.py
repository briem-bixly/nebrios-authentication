from nebriosauthenticationmodels import Token, BasicAuth
from nebrios_authentication_lib import token_required, basic_auth_required
import logging

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
            t = Token(token=request.FORM.token, description=request.FORM.description)
            created = True

    if not created and t is not None:
        t.token = request.FORM.token
        t.description = request.FORM.description
    t.save()


def update_basic(request):
    b = None
    created = False
    try:
        b = BasicAuth.get(username=request.FORM.username)
    except Process.DoesNotExist:
        b = BasicAuth(username=request.FORM.username)
        b.set_password(request.FORM.pw)
        request.FORM.pw = ''
        created = True

    if not created and b is not None:
        b.username = request.FORM.username
        b.set_password(request.FORM.pw)
    b.save()


@token_required
def test_endpoint(request):
    logging.debug(request.POST)
    logging.debug('lol test')


@basic_auth_required
def other_test(request):
    logging.debug(request.POST)
