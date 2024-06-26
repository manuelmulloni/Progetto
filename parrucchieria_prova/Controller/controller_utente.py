import os
import pickle

from parrucchieria_prova.Model.utente import utente
class controller_utente:
    def __init__(self):
        cartella_file = 'Database'

        # Nome del file che vuoi trovare
        nome_file = 'Lista_Utenti.pickle'

        # Ottieni il percorso assoluto del file combinando il percorso della directory e il nome del file
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cartella_file, nome_file))
        self.users = []



    def initialize_user(self):
        if os.path.getsize(self.db_path) == []:
            with open(self.db_path, 'wb') as db_file:
                a = utente('Ut', 'pr')
                b = a.to_dict()
                self.users.append(b)
                pickle.dump(self.users, db_file)
        elif os.path.exists(self.db_path):
            with open(self.db_path, 'wb') as db_file:
                a = utente('Ut', 'pr')
                b = a.to_dict()
                self.users.append(b)
                pickle.dump(self.users, db_file)
        else:
            self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.db_path, 'rb') as db_file:
                self.users = pickle.load(db_file)  # cercavo di far diventare admns una lista di dizionari e funziona
        except FileNotFoundError:
            return print("File not found")

    def save_to_file(self):
        with open(self.db_path, 'wb') as db_file:
            pickle.dump(self.users, db_file)

    def add_user(self, user):
        self.users.append(user)
        self.save_to_file()

    def delete_user(self, user):
        self.users.remove(user)
        self.save_to_file()

    def update_user(self, old_user, new_user):
        if old_user in self.users:
            self.users.remove(old_user)
            self.users.append(new_user)
            self.save_to_file()

    def read_user(self, user):
        if user in self.users:
            return user

    def get_user(self, username):
        for user in self.users:
            if user['username'] == username:
                return user # non ritorna niente