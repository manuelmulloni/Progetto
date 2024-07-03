from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
import sys
from parrucchieria_prova.Controller.controller_utente import controller_utente
from parrucchieria_prova.Controller.controller_admin import controller_admin
from parrucchieria_prova.Controller.controller_parrucchiere import controller_parrucchiere
from parrucchieria_prova.View.view_utente import view_utente
from parrucchieria_prova.View.view_admin import view_admin
from parrucchieria_prova.View.view_parrucchiere import view_parrucchiere
from parrucchieria_prova.Model.utente import utente

class pagina_login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Page")

        layout = QVBoxLayout()

        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_credentials)

        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.clicked.connect(self.create_account)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.create_account_button)

        self.setLayout(layout)


    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user_controller = controller_utente()
        admin_controller = controller_admin()
        parruchiere_controller = controller_parrucchiere()
        parruchiere_controller.initialize_user()
        admin_controller.initialize_user()
        user_controller.initialize_user()

        try:
            # Check admin credentials
            for admin in admin_controller.admins:
                if (admin['Username'] == username and
                       admin['Password'] == password and
                        admin['User_type'] == "Admin"):
                    self.pagina_admin = view_admin(username)
                    self.pagina_admin.show()
                    self.close()
                    return

            # Check parrucchiere credentials
            for parrucchiere in parruchiere_controller.parrucchieri:
                if (parrucchiere['username'] == username and
                        parrucchiere['password'] == password and
                        parrucchiere['user_type'] == "Parrucchiere"):
                    self.pagina_parrucchiere = view_parrucchiere(username)
                    self.pagina_parrucchiere.show()
                    self.close()
                    return

            # Check user credentials
            for user in user_controller.users:
                if (user['username'] == username and
                        user['password'] == password and
                        user['user_type'] == "Utente"):
                    self.pagina_utente = view_utente(username)  # Pass the username to the view_utente constructor
                    self.pagina_utente.show()  # Show the view_utente page
                    self.close()
                    return  # Close the login page

            # If no match found, show error message
            QMessageBox.warning(self, "Errore", "Credenziali errate")

        except Exception as e:
            # Log the exception (optional)
            print(f"C'è stato un errore: {e}")
            QMessageBox.warning(self, "Errore", "Si è verificato un errore. Riprova.")

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user_controller = controller_utente()
        parruchiere_controller = controller_parrucchiere()
        admin_controller = controller_admin()
        user_controller.initialize_user()
        parruchiere_controller.initialize_user()
        admin_controller.initialize_user()
        try:

            for admin in admin_controller.admins:
                if admin['Username'] == username:
                    QMessageBox.warning(self, "Errore", "L'username è già stato utilizzato")
                    return

            # Check if username already exists among parrucchieri
            for parrucchiere in parruchiere_controller.parrucchieri:
                if parrucchiere['username'] == username:
                    QMessageBox.warning(self, "Errore", "L'username è già stato utilizzato")
                    return

            # Check if username already exists among users
            user_controller.initialize_user()
            for user in user_controller.users:
                if user['username'] == username:
                    QMessageBox.warning(self, "Errore", "L'username è già stato utilizzato")
                    return

            # If username is unique, create new utente account
            new_utente = utente(username, password)
            a = new_utente.to_dict()
            user_controller.add_user(a)
            self.pagina_utente = view_utente(username)
            self.pagina_utente.show()
            self.close()

        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Si è verificato un errore durante la creazione dell'account: {e}")

app = QApplication(sys.argv)

window = pagina_login()
window.show()

sys.exit(app.exec())

"""
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, \
    QInputDialog
import sys
from parrucchieria_prova.Controller.controller_utente import controller_utente
from parrucchieria_prova.Controller.controller_admin import controller_admin
from parrucchieria_prova.Controller.controller_parrucchiere import controller_parrucchiere
from parrucchieria_prova.View.view_utente import view_utente
from parrucchieria_prova.View.view_admin import view_admin
from parrucchieria_prova.View.view_parrucchiere import view_parrucchiere
from parrucchieria_prova.Model.utente import utente
class pagina_login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Page")

        layout = QVBoxLayout()

        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_credentials)

        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.clicked.connect(self.create_account)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.create_account_button)

        self.setLayout(layout)


    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user_controller = controller_utente()
        admin_controller = controller_admin()
        parruchiere_controller = controller_parrucchiere()
        parruchiere_controller.initialize_user()
        admin_controller.initialize_user()
        user_controller.initialize_user()

        try:
            # Check admin credentials
            for admin in admin_controller.admins:
                if (admin['Username'] == username and
                       admin['Password'] == password and
                        admin['User_type'] == "Admin"):
                    self.pagina_admin = view_admin(username)
                    self.pagina_admin.show()
                    self.close()
                    return

            for parrucchiere in parruchiere_controller.parrucchieri:
                if (parrucchiere['username'] == username and
                        parrucchiere['password'] == password and
                        parrucchiere['user_type'] == "Parrucchiere"):
                    self.pagina_parrucchiere = view_parrucchiere(username)
                    self.pagina_parrucchiere.show()
                    self.close()
                    return

            # Check user credentials
            for user in user_controller.users:
                if (user['username'] == username and
                        user['password'] == password and
                        user['user_type'] == "Utente"):
                    self.pagina_utente = view_utente(username)  # Pass the username to the view_utente constructor
                    self.pagina_utente.show()  # Show the view_utente page
                    self.close()
                    return  # Close the login page

            # If no match found, show error message
            QMessageBox.warning(self, "Errore", "Credenziali errate")
        except Exception as e:
            # Log the exception (optional)
            print(f"C'è stato un errore: {e}")
            QMessageBox.warning(self, "Errore", "Si è verificato un errore. Riprova.")

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user_controller = controller_utente()
        user_controller.initialize_user()

        for user in user_controller.users:
            if user['username'] == username:
                QMessageBox.warning(self, "Errore", "L'username è stato già utilizzato")
                return

        new_utente = utente(username, password)
        a = new_utente.to_dict()
        user_controller.add_user(a)
        self.pagina_utente = view_utente(username)
        self.pagina_utente.show()
        self.close()
        return


    #manca laccesso dei parrucchieri





app = QApplication(sys.argv)

window = pagina_login()
window.show()

sys.exit(app.exec())
"""