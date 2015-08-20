from nebriosmodels import NebriOSModel, NebriOSField, NebriOSReference
from passlib.hash import pbkdf2_sha512

class Token(NebriOSModel):
    token = NebriOSField(required=True)
    description = NebriOSField(required=True)

class BasicAuth(NebriOSModel):
    username = NebriOSField(required=True)
    password = NebriOSField(required=True)

    def set_password(self, password):
        self.password = pbkdf2_sha512.encrypt(password)

    def validate_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)