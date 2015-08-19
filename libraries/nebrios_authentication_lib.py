from nebriosauthenticationmodels import Token
import logging

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
