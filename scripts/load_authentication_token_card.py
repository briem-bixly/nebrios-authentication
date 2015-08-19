class load_authentication_token_card(NebriOS):
    listens_to = ['load_authentication_token_card']

    def check(self):
        return self.load_authentication_token_card is True

    def action(self):
        load_card('nebrios-authentication-token')
