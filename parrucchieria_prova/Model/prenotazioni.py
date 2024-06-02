


class prenotazioni:
    def __init__(self, username, data,ora, parruchiere, servizio):
        self.username = username
        self.data = data
        self.ora = ora
        self.parruchiere = parruchiere
        self.servizio = servizio



    def get_Prenotazioni(self):
        return {'username': self.username, 'data': self.data, 'ora':self.ora, 'parruchiere': self.parruchiere,
                'servizio': self.servizio}