from nebriosauthenticationmodels import Token, BasicAuth, OAuth
import logging
import base64
import json

logging.basicConfig(filename='token_errors.log', level=logging.DEBUG)


def token_required(realm):
    logging.debug('realm: %s' % realm)
    def wrap(f):
        def wrapped_f(*args):
            try:
                token = json.loads(args[0].BODY)['token']
            except:
                try:
                    token = args[0].POST['token']
                except:
                    # This will need to be looked into... uwsgi/nginx are getting in the way
                    # try:
                    #     token = args[0].META['token']
                    # except:
                    return HttpResponseForbidden
            logging.debug(token)
            try:
                t = Token.get(token=token)
                logging.debug('t realm: %s' % t.realm)
            except Exception, e:
                logging.debug(e)
                return HttpResponseForbidden
            if t.realm != realm:
                logging.debug(t.realm)
                return HttpResponseForbidden
            f(*args)
        return wrapped_f
    return wrap


def basic_auth_required(realm):
    def wrap(f):
        def wrapped_f(*args):
            if args[0].META.get('HTTP_AUTHORIZATION') is None:
                response = HttpResponse('Unauthorized', status=401)
                response['WWW-Authenticate'] = "Basic realm='%s'" % realm
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
                if user.realm != realm:
                    return HttpResponseForbidden
            f(*args)
        return wrapped_f
    return wrap


def oauth_required(realm):
    def wrap(f):
        def wrapped_f(*args):
            access_token = None
            try:
                access_token = json.loads(args[0].BODY)['access_token']
            except:
                try:
                    access_token = args[0].POST['access_token']
                except:
                    return HttpResponseForbidden
            try:
                o = OAuth.get(token=access_token)
            except:
                return HttpResponseForbidden
            if o.scope != realm:
                return HttpResponseForbidden
            f(*args)
        return wrapped_f
    return wrap
