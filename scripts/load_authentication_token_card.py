import string
import random

class load_authentication_token_card(NebriOS):
    listens_to = ['load_authentication_token_card']

    def check(self):
        return self.load_authentication_token_card is True

    def action(self):
        self.token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(36))
        load_card('nebrios-authentication-token')
