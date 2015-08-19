from nebriosmodels import NebriOSModel, NebriOSField, NebriOSReference

class Token(NebriOSModel):
    token = NebriOSField(required=True)
    description = NebriOSField(required=True)