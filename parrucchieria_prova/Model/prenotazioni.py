


class prenotazioni:
    def __init__(self, username, data,ora, parrucchiere, servizio):
        self.username = username
        self.data = data
        self.ora = ora
        self.parrucchiere = parrucchiere
        self.servizio = servizio



    def get_Prenotazioni(self):
        return {'username': self.username, 'data': self.data, 'ora': self.ora, 'parrucchiere': self.parrucchiere,
                'servizio': self.servizio}