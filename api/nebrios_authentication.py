from nebriosauthenticationmodels import Token
from nebrios_authentication_lib import token_required
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
    test_endpoint(request.FORM)
    t.save()


@token_required
def test_endpoint(request):
    logging.debug(request.POST)
    logging.debug('lol test')


def other_test(request):
    logging.debug(request.POST)
