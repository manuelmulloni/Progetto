
import os
import pickle
from parrucchieria_prova.Model.parrucchiere import parrucchiere

class controller_parrucchiere:
    def __init__(self):
        cartella_file = 'Database'
        nome_file = 'Lista_Parrucchieri.pickle'
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cartella_file, nome_file))
        self.parrucchieri = []
        self.initialize_user()

    def initialize_user(self):
        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            self.parrucchieri = [parrucchiere('parrucchiere', 'azzer').to_dict()]
            self.save_to_file()
        else:
            self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.db_path, 'rb') as db_file:
                self.parrucchieri = pickle.load(db_file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            print("Errore nel caricamento del file")
            self.parrucchieri = []

    def save_to_file(self):
        with open(self.db_path, 'wb') as db_file:
            pickle.dump(self.parrucchieri, db_file)

    def add_parrucchiere(self, parrucchiere): #parrucchiere è un  dict
        self.parrucchieri.append(parrucchiere)
        self.save_to_file()

    def delete_parrucchiere(self, parrucchiere):
        if parrucchiere in self.parrucchieri:
            self.parrucchieri.remove(parrucchiere)
            self.save_to_file()

    def update_parrucchiere(self, old_parrucchiere, new_parrucchiere):
        try:
            index = self.parrucchieri.index(old_parrucchiere)
            self.parrucchieri[index] = new_parrucchiere
            self.save_to_file()
        except ValueError:
            print("Parrucchiere non trovato")

    def read_parrucchiere(self, nome):
        for p in self.parrucchieri:
            if p['username'] == nome:
                return p

