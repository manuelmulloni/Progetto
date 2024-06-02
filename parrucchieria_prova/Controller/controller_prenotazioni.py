import os
import pickle

from Model.prenotazioni import prenotazioni
class controller_prenotazioni:
    def __init__(self, db_path):
        self.db_path = db_path
        self.prenotazioni = []


    def initialize_prenotazioni(self):
        if os.path.getsize(self.db_path) == 0:
            with open(self.db_path, 'wb') as db_file:
                p = prenotazioni('boh', 'data', 'or', 'nome', 'servizio')
                b = p.get_Prenotazioni()
                self.prenotazioni.append(b)
                self.save_to_file()
        else:
            self.load_from_file()
    def load_from_file(self):
        try:
            with open(self.db_path, 'rb') as db_file:
                self.prenotazioni = pickle.load(db_file)
        except FileNotFoundError:
            return print("File not found")

    def save_to_file(self):
        with open(self.db_path, 'wb') as db_file:
            pickle.dump(self.prenotazioni, db_file)
    def add_prenotazione(self, prenotazione):
        self.prenotazioni.append(prenotazione)
        self.save_to_file()


    def delete_prenotazione(self, prenotazione):
        self.prenotazioni.remove(prenotazione)
        self.save_to_file()

    def update_prenotazione(self, old_prenotazione, new_prenotazione):
        index = self.prenotazioni.index(old_prenotazione)
        self.prenotazioni[index] = new_prenotazione
        self.save_to_file()

    def read_prenotazione(self, prenotazione):
        if prenotazione in self.prenotazioni:
            return prenotazione

    def get_bookings(self, username):
        bookings = []
        for prenotazione in self.prenotazioni:
            if prenotazione['username'] == username:
                bookings.append(prenotazione)


