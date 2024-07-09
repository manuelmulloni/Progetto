
import os
import pickle
from parrucchieria_prova.Model.prenotazioni import prenotazioni

class controller_prenotazioni:
    def __init__(self):
        cartella_file = 'Database'
        nome_file = 'Lista_Prenotazioni.pickle'
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cartella_file, nome_file))
        self.prenotazioni = []
        self.initialize_prenotazioni()

    def initialize_prenotazioni(self):
        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            self.prenotazioni = [prenotazioni('boh', 'data', 'or', 'nome', 'servizio').get_Prenotazioni()]
            self.save_to_file()
        else:
            self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.db_path, 'rb') as db_file:
                self.prenotazioni = pickle.load(db_file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            print("Errore nel caricamento del file")
            self.prenotazioni = []

    def save_to_file(self):
        with open(self.db_path, 'wb') as db_file:
            pickle.dump(self.prenotazioni, db_file)

    def add_prenotazione(self, prenotazione):

        self.prenotazioni.append(prenotazione)
        self.save_to_file()

    def delete_prenotazione(self, prenotazione):
        if prenotazione in self.prenotazioni:
            self.prenotazioni.remove(prenotazione)
            self.save_to_file()

    def update_prenotazione(self, old_prenotazione, new_prenotazione):
        try:
            index = self.prenotazioni.index(old_prenotazione)
            self.prenotazioni[index] = new_prenotazione
            self.save_to_file()
        except ValueError:
            print("Prenotazione non trovata")

    def get_bookings(self, username):
        bookings = [prenotazione for prenotazione in self.prenotazioni if prenotazione['username'] == username]
        return bookings

    def is_parrucchiere_available(self, new_parrucchiere, selected_date, new_ora):
        for prenotazione in self.prenotazioni:
            if prenotazione['data'] == selected_date and prenotazione['ora'] == new_ora and prenotazione['parrucchiere'] == new_parrucchiere:
                return False



