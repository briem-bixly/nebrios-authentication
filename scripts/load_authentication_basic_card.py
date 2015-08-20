import string
import random

class load_authentication_basic_card(NebriOS):
    listens_to = ['load_authentication_basic_card']

    def check(self):
        return self.load_authentication_basic_card is True

    def action(self):
        load_card('nebrios-authentication-basic')