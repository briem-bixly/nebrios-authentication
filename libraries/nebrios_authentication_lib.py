from nebriosauthenticationmodels import Token, BasicAuth
import logging
import base64

logging.basicConfig(filename='token_errors.log', level=logging.DEBUG)


def token_required(func):
    def new_func(*args, **kwargs):
        try:
            token = args[0].BODY['token']
        except:
            try:
                token = args[0].POST['token']
            except:
                # This will need to be looked into... uwsgi/nginx are getting in the way
                # try:
                #     token = args[0].META['token']
                # except:
                return HttpResponseForbidden
        try:
            t = Token.get(token=token)
        except:
            return HttpResponseForbidden
        func(*args, **kwargs)
    return new_func


def basic_auth_required(func):
    def new_func(*args, **kwargs):
        if args[0].META.get('HTTP_AUTHORIZATION') is None:
            response = HttpResponse('Unauthorized', status=401)
            response['WWW-Authenticate'] = "Basic realm='NebriOS Instance'"
            return response
        else:
            creds = base64.b64decode(args[0].META['HTTP_AUTHORIZATION'].split(' ')[-1]).split(':')
            user = None
            try:
                user = BasicAuth.get(username=creds[0])
            except:
                return HttpResponseForbidden
            if not user.validate_password(creds[1]):
                return HttpResponseForbidden
        func(*args, **kwargs)
    return new_func
