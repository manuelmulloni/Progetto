
import os
import pickle
from parrucchieria_prova.Model.admin import admin

class controller_admin:
    def __init__(self):
        cartella_file = 'Database'
        nome_file = 'Lista_Admin.pickle'
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cartella_file, nome_file))
        self.admins = []
        self.initialize_user()

    def initialize_user(self):
        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            self.admins = [admin('admin', 'parrucca').get_Admin()]
            self.save_to_file()
        else:
            self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.db_path, 'rb') as db_file:
                self.admins = pickle.load(db_file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            print("Errore nel caricamento del file")
            self.admins = []

    def save_to_file(self):
        with open(self.db_path, 'wb') as db_file:
            pickle.dump(self.admins, db_file)

    def add_admin(self, admin):
        self.admins.append(admin)
        self.save_to_file()

    def delete_admin(self, admin):
        if admin in self.admins:
            self.admins.remove(admin)
            self.save_to_file()

    def update_admin(self, old_admin, new_admin):
        try:
            index = self.admins.index(old_admin)
            self.admins[index] = new_admin
            self.save_to_file()
        except ValueError:
            print("Admin non trovato")

    def read_admin(self, username):
        for admin in self.admins:
            if admin['Username'] == username:
                return admin
        return None


