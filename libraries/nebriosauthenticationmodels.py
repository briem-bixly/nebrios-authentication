from nebriosmodels import NebriOSModel, NebriOSField, NebriOSReference
from passlib.hash import pbkdf2_sha512


class Token(NebriOSModel):
    token = NebriOSField(required=True)
    description = NebriOSField(required=True)
    realm = NebriOSField()


class BasicAuth(NebriOSModel):
    username = NebriOSField(required=True)
    password = NebriOSField(required=True)
    realm = NebriOSField()

    def set_password(self, password):
        self.password = pbkdf2_sha512.encrypt(password)

    def validate_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)


class OAuth(NebriOSModel):
    username = NebriOSField(required=True)
    consumer_key = NebriOSField(required=True)
    consumer_secret = NebriOSField(required=True)
    token = NebriOSField()
    scope = NebriOSField()