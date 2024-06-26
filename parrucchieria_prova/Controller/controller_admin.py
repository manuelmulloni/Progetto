import os
import pickle
from parrucchieria_prova.Model.admin import admin

class controller_admin:
    def __init__(self, ):
        cartella_file = 'Database'

        # Nome del file che vuoi trovare
        nome_file = 'Lista_Admin.pickle'

        # Ottieni il percorso assoluto del file combinando il percorso della directory e il nome del file
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cartella_file, nome_file))
        self.admins = []

    def initialize_user(self):
        if os.path.getsize(self.db_path) == []:
            with open(self.db_path, 'wb') as db_file:
                a = admin('admin', 'parrucca')
                b = a.get_Admin()
                self.admins.append(b)
                self.save_to_file() # cercavo di far diventare admns una lista di dizionari
        elif os.path.exists(self.db_path):
            with open(self.db_path, 'wb') as db_file:
                a = admin('admin', 'parrucca')
                b = a.get_Admin()
                self.admins.append(b)
                self.save_to_file()
        else:
            self.load_from_file()



    def load_from_file(self):
        try:
          with open(self.db_path, 'rb') as db_file:
            self.admins = pickle.load(db_file)  # cercavo di far diventare admns una lista di dizionari e funziona
        except FileNotFoundError:
            return print("File not found")

    def save_to_file(self):
        with open(self.db_path, 'wb') as db_file:
            pickle.dump(self.admins, db_file)
    def add_admin(self, admin):
        self.admins.append(admin)  #probabilmente non serve
        self.save_to_file()

    def delete_admin(self, admin):
        self.admins.remove(admin) #probabilmente non serve
        self.save_to_file()

    def update_admin(self, old_admin, new_admin):
        index = self.admins.index(old_admin)
        self.admins[index] = new_admin
        self.save_to_file()

    def read_admin(self, admin):
        if admin in self.admins:
            return admin


#controller_admin = controller_admin('C:\\Users\\manue\\PycharmProjects\\parrucchieria_prova\\Database\\Lista_Admin.pickle')
#a = admin('boh', 'sturn')

#controller_admin.add_admin(a.get_Admin())