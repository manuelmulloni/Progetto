import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMessageBox, QInputDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QDialog, \
    QAbstractItemView
from PyQt6.uic import loadUi
from parrucchieria_prova.Controller.controller_prenotazioni import controller_prenotazioni
from parrucchieria_prova.Controller.controller_parrucchiere import controller_parrucchiere
from parrucchieria_prova.Model.parrucchiere import parrucchiere
class view_parrucchiere(QWidget):
    def __init__(self, username):
        super(view_parrucchiere, self).__init__()
        self.username = username

        # Load the UI
        cartella_file = 'File_ui'
        nome_file = 'viewparrucchiere.ui'
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cartella_file, nome_file))
        loadUi(self.db_path, self)
        # Set the window title
        self.setWindowTitle("Parrucchiere Page")

        self.pushButton.setText("Vedi prenotazioni")

        # Connect the widgets to their respective methods
        self.pushButton.clicked.connect(self.ViewAllB)
        self.comboBox.addItems(["Profilo", "View Profile", "Modifica Profilo"])
        self.comboBox.currentTextChanged.connect(self.handle_profile)

    def ViewAllB(self):
        self.pr = vedi_prenotazioni()
        self.pr.show()

    def handle_profile(self,action):
        if action == "View Profile":
            self.view_profile()
        elif action == "Modifica Profilo":
            self.modifica_profilo()
        self.comboBox.setCurrentIndex(0)

    def view_profile(self):

        try:
            parrucchiere = controller_parrucchiere()
            parrucchiere.initialize_user()
            for par in parrucchiere.parrucchieri:
                if par['username'] == self.username:
                    return QMessageBox.information(self, "Profile",
                                                   f"Username: {par['username']}\nPassword: {par['password']}")

            QMessageBox.warning(self, "Profilo", "Profilo non trovato.")
        except Exception as e:
            QMessageBox.critical(self, "Profilo", f"C'è stato un errore nel mentre cercavi il profilo: {e}")

    def modifica_profilo(self):
        try:
            parru = controller_parrucchiere()
            parru.initialize_user()

            new_username, ok_username = QInputDialog.getText(self, 'Cambia credenziali', 'Inserisci nuovo username:')
            if not ok_username or not new_username.strip():
                raise ValueError("Username non valido")

            # Ottieni la nuova password dall'utente
            new_password, ok_password = QInputDialog.getText(self, 'Cambia credenziali', 'Inserisci la nuova password:')
            if not ok_password or not new_password.strip():
                raise ValueError("Password non valida")

            # Trova e aggiorna il profilo del parrucchiere
            for par in parru.parrucchieri:
                if par['username'] == self.username:
                    par['username'] = new_username
                    par['password'] = new_password
                    parru.save_to_file()  # Salva le modifiche nel file
                    QMessageBox.information(self, "Cambia credenziali", f"Le credenziali sono state aggiornate con successo.")
                    return

            # Se il profilo non viene trovato
            QMessageBox.warning(self, "Cambia credenziali", "Profilo non trovato.")
        except ValueError as ve:
            QMessageBox.warning(self, "Cambia credenziali", f"Errore: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Cambia credenziali",
                                 f"C'è stato un errore mentre cercavi di cambiare le credenziali: {e}")


class vedi_prenotazioni(QWidget):
    def __init__(self):
        super().__init__()

        # Create a table
        self.table = QTableWidget()
        self.prenotazioni_controller = controller_prenotazioni()
        self.prenotazioni_controller.initialize_prenotazioni()
        prenotazioni = self.prenotazioni_controller.prenotazioni
        # Set the table headers
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Username", "Data","Ora", "Parrucchiere", "Servizio"])

        # Add the bookings to the table
        for i, prenotazione in enumerate(prenotazioni):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(prenotazione['username']))
            self.table.setItem(i, 1, QTableWidgetItem(prenotazione['data']))
            self.table.setItem(i, 2, QTableWidgetItem(prenotazione['ora']))
            self.table.setItem(i, 3, QTableWidgetItem(prenotazione['parrucchiere']))
            self.table.setItem(i, 4, QTableWidgetItem(prenotazione['servizio']))

        # Create a layout and add the table to it
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        # Set the layout
        self.setLayout(layout)




if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = view_parrucchiere("parrucchiere")
    window.show()
    sys.exit(app.exec())