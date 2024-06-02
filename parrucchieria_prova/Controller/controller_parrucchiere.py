import os
import pickle
from Model.parrucchiere import parrucchiere

class controller_parrucchiere:
    def __init__(self, db_path):
        self.db_path = db_path
        self.parrucchieri = []



    def initialize_user(self):
        if   os.path.getsize(self.db_path) == 0:
          with open(self.db_path, 'wb') as db_file:
            a = parrucchiere('parrucchiere', 'azzer')
            b = a.to_dict()
            self.parrucchieri.append(b)
            self.save_to_file()
        else:
            self.load_from_file()
    def load_from_file(self):
        try:
            with open(self.db_path, 'rb') as db_file:
                self.parrucchieri = pickle.load(db_file)
        except FileNotFoundError:
            return print("File not found")

    def save_to_file(self):
        with open(self.db_path, 'wb') as db_file:
            pickle.dump(self.parrucchieri, db_file)

    def add_parrucchiere(self, parrucchiere):
        self.parrucchieri.append(parrucchiere)
        self.save_to_file()

    def delete_parrucchiere(self, parrucchiere):
        self.parrucchieri.remove(parrucchiere)
        self.save_to_file()

    def update_parrucchiere(self, old_parrucchiere, new_parrucchiere):
        index = self.parrucchieri.index(old_parrucchiere)
        self.parrucchieri[index] = new_parrucchiere
        self.save_to_file()

    def read_parrucchiere(self, parrucchiere):
        if parrucchiere in self.parrucchieri:
            return parrucchiere