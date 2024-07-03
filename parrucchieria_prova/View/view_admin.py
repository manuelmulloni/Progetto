import os

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt6.uic import loadUi
from parrucchieria_prova.Controller.controller_prenotazioni import controller_prenotazioni
from parrucchieria_prova.Controller.controller_admin import controller_admin
from parrucchieria_prova.Controller.controller_utente import controller_utente
from parrucchieria_prova.Controller.controller_parrucchiere import controller_parrucchiere

class view_admin(QtWidgets.QWidget):
     def __init__(self,username):
             super(view_admin, self).__init__()
             self.username = username
             self.ad = controller_admin()

             cartella_file = 'File_ui'
             nome_file = 'viewAdmin.ui'
             self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cartella_file, nome_file))
             loadUi(self.db_path, self)

             self.setWindowTitle(username)
             self.VediUtenti.clicked.connect(self.view_and_delete_users)
             self.pushButton_2.clicked.connect(self.view_and_delete_bookings)

             self.comboBox_2.addItems(["Profilo","Vedi Profilo", "Cambia Profilo"])
             self.comboBox.addItems(
                 ["Parrucchieri","Vedi Parrucchieri", "Cambia Parrucchieri","Aggiungi Parrucchieri"])

             # Connect the combo boxes to methods
             self.comboBox_2.currentTextChanged.connect(self.handle_profile_action)
             self.comboBox.currentTextChanged.connect(self.handle_hairdresser_action)

     def handle_profile_action(self, action):
         if action == "Vedi Profilo":
             self.view_profile()
         elif action == "Cambia Profilo":
             self.change_credentials(self.username)

         # Reset the comboBox to allow re-selection of the same action
         self.comboBox_2.setCurrentIndex(0) #resetta l indice combobox

     def handle_hairdresser_action(self, action):
         if action == "Vedi Parrucchieri":
             self.view_hairdressers()
         elif action == "Cambia Parrucchieri":
             self.change_hairdressers()
         elif action == "Aggiungi Parrucchieri":
             self.add_hairdressers()

         # Reset the comboBox to allow re-selection of the same action
         self.comboBox.setCurrentIndex(0)

     def view_profile(self):
                 self.ad.initialize_user()
                 admin_profile = self.ad.admins[0]  # Assuming the first admin in the list is the logged-in admin

                 # Create a string with the admin's profile information
                 profile_info = f"Username: {admin_profile['Username']}\nPassword: {admin_profile['Password']}\nUser Type: {admin_profile['User_type']}"

                 # Display the profile information in a dialog box
                 QMessageBox.information(self, "Admin Profile", profile_info)

     def change_credentials(self, old_username):
         pr = controller_parrucchiere()
         pr.initialize_user()
         ut = controller_utente()
         ut.initialize_user()

         try:
             # Prompt for new username
             new_username, ok_username = QInputDialog.getText(self, 'Cambia Credenziali',
                                                              'Inserisci il nuovo username:')

             if not ok_username or not new_username.strip():
                 raise ValueError("L'user inserito non è valido")

             # Check if new username is already in use by a parrucchiere
             for parrucchiere in pr.parrucchieri:
                 if new_username.strip() == parrucchiere['username']:
                     raise ValueError("Il nuovo username è già in uso da un parrucchiere")

             # Check if new username is already in use by a user
             for user in ut.users:
                 if new_username.strip() == user['username']:
                     raise ValueError("Il nuovo username è già in uso da un utente")

             # Prompt for new password
             new_password, ok_password = QInputDialog.getText(self, 'Cambia Credenziali',
                                                              'Inserisci la nuova password:')

             if not ok_password or not new_password.strip():
                 raise ValueError("La password inserita non è valida")

             # Update the credentials if both inputs are valid
             if ok_username and ok_password:
                 self.ad.initialize_user()
                 for admin in self.ad.admins:
                     if admin['Username'] == old_username:
                         # Update the admin's credentials
                         admin['Username'] = new_username.strip()
                         admin['Password'] = new_password.strip()

                         # Save the updated list of admins to the file
                         self.ad.save_to_file()
                         QMessageBox.information(self, "Credenziali cambiate",
                                                 f"Le credenziali per {old_username} sono state aggiornate.")
                         return

                 # If the admin is not found, show a warning
                 QMessageBox.warning(self, "Cambia Credenziali", "Admin non trovato.")

         except ValueError as e:
             QMessageBox.warning(self, "Cambia Credenziali", f"Errore nell'inserimento delle credenziali: {e}")

         except Exception as e:
             QMessageBox.warning(self, "Cambia Credenziali", f"Si è verificato un errore: {e}")

     def view_hairdressers(self):
                 try:
                     self.pa = view_parrucchieri()
                     self.pa.show()

                 except TypeError as e:
                     QMessageBox.information(self, "View Hairdressers", "No hairdressers found.")
                 except Exception as e:
                     QMessageBox.critical(self, "View Hairdressers", f"An unexpected error occurred: {e}")

     def change_hairdressers(self):
         # Create an instance of controller_parrucchiere
         parrucchiere_controller = controller_parrucchiere()
         utente_controller = controller_utente()
         utente_controller.initialize_user()

         # Load the hairdressers data
         try:
             parrucchiere_controller.initialize_user()
         except Exception as e:
             QMessageBox.critical(self, "Errore", f"Impossibile caricare i dati dei parrucchieri: {e}")
             return

         # Ask the user for the username of the hairdresser they want to update
         try:
             old_username, ok = QInputDialog.getText(self, 'Aggiorna Parrucchiere',
                                                     'Inserisci il nome del parrucchiere di cui vuoi cambiare le credenziali:')
             if not ok or not old_username.strip():
                 raise ValueError("Input non valido per il nome del parrucchiere")
         except Exception as e:
             QMessageBox.warning(self, "Aggiorna Parrucchiere",
                                 f"Errore nell'inserimento del nome del parrucchiere: {e}")
             return

         # Find the hairdresser with the specified username
         found = False
         for parrucchiere in parrucchiere_controller.parrucchieri:
             if parrucchiere['username'] == old_username:
                 found = True
                 try:
                     new_username, ok_username = QInputDialog.getText(self, 'Aggiorna Parrucchiere',
                                                                      'Inserisci il nuovo username:')
                     if not ok_username or not new_username.strip():
                         raise ValueError("Input non valido per il nuovo username")

                     new_password, ok_password = QInputDialog.getText(self, 'Aggiorna Parrucchiere',
                                                                      'Inserisci la nuova password:')
                     if not ok_password or not new_password.strip():
                         raise ValueError("Input non valido per la nuova password")

                     # Check if the new username is already in use by any user or hairdresser
                     username_in_use = any(
                         p['username'] == new_username.strip() for p in parrucchiere_controller.parrucchieri)
                     if username_in_use or any(
                             u['username'] == new_username.strip() for u in utente_controller.users):
                         raise ValueError("Il nuovo username è già in uso da un altro utente o parrucchiere")

                     # Update the hairdresser's details if inputs are valid
                     if ok_username and ok_password:
                         new_parrucchiere = {'username': new_username.strip(), 'password': new_password.strip(),
                                             'user_type': 'Parrucchiere'}
                         parrucchiere_controller.update_parrucchiere(parrucchiere, new_parrucchiere)
                         QMessageBox.information(self, "Aggiorna Parrucchiere",
                                                 f"Le credenziali del parrucchiere {old_username} sono state aggiornate.")
                         return
                 except ValueError as e:
                     QMessageBox.warning(self, "Aggiorna Parrucchiere",
                                         f"Errore nell'inserimento delle nuove credenziali: {e}")
                     return
                 except Exception as e:
                     QMessageBox.warning(self, "Aggiorna Parrucchiere",
                                         f"Errore durante l'aggiornamento delle credenziali: {e}")
                     return

         # If the hairdresser was not found
         if not found:
             QMessageBox.warning(self, "Aggiorna Parrucchiere", "Parrucchiere non trovato.")
     def add_hairdressers(self):
         parrucchiere_controller = controller_parrucchiere()
         try:
             parrucchiere_controller.initialize_user()
         except Exception as e:
             QMessageBox.critical(self, "Errore", f"Impossibile caricare i dati dei parrucchieri: {e}")
             return

         try:
             new_username, ok_username = QInputDialog.getText(self, 'Aggiungi Parrucchiere',
                                                              'Inserisci il username del nuovo parrucchiere:')
             # Check if username already exists among users or hairdressers
             if new_username.strip() in [user['username'] for user in parrucchiere_controller.parrucchieri]:
                 QMessageBox.warning(self, "Aggiungi Parrucchiere",
                                     "Il nome utente è già stato preso da un parrucchiere.")
                 return

             for user in controller_utente().users:
                 if new_username.strip() == user['username']:
                     QMessageBox.warning(self, "Aggiungi Parrucchiere",
                                         "Il nome utente è già stato preso da un utente.")
                     return

             if not ok_username or not new_username.strip():
                 raise ValueError("Input non valido per il username")

             new_password, ok_password = QInputDialog.getText(self, 'Aggiungi Parrucchiere',
                                                              'Inserisci la password del nuovo parrucchiere:')
             if not ok_password or not new_password.strip():
                 raise ValueError("Input non valido per la password")

             if ok_username and ok_password:
                 new_parrucchiere = {'username': new_username.strip(), 'password': new_password.strip(),
                                     'user_type': 'Parrucchiere'}
                 parrucchiere_controller.add_parrucchiere(new_parrucchiere)
                 QMessageBox.information(self, "Aggiungi Parrucchiere",
                                         f"Parrucchiere {new_username} è stato aggiunto.")
                 # Update table or perform any other necessary updates
                 # self.load_parrucchieri_data() or any method that updates the UI
         except ValueError as e:
             QMessageBox.warning(self, "Aggiungi Parrucchiere", f"Errore nell'inserimento delle credenziali: {e}")
         except Exception as e:
             QMessageBox.critical(self, "Aggiungi Parrucchiere", f"Si è verificato un errore: {e}")

     def view_and_delete_bookings(self):
         self.p = vedi_prenotazioni()
         self.p.show()

     def view_and_delete_users(self):
         self.u = vedi_utenti()
         self.u.show()


class vedi_prenotazioni(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prenotazioni")
        self.layout = QVBoxLayout()

        # Initialize booking controller and fetch bookings
        self.prenotazioni_controller = controller_prenotazioni()
        self.prenotazioni_controller.initialize_prenotazioni()
        prenotazioni = self.prenotazioni_controller.prenotazioni

        # Create a table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Username", "Data", "Ora", "Parrucchiere", "Servizio"])

        # Add bookings to the table
        for i, prenotazione in enumerate(prenotazioni):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(prenotazione['username']))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(prenotazione['data']))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(prenotazione['ora']))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(prenotazione['parrucchiere']))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(prenotazione['servizio']))

        # Connect cellClicked signal to delete_selected_booking function
        self.tableWidget.cellClicked.connect(self.delete_selected_booking)

        # Add table to the layout
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def delete_selected_booking(self, row, column):
        # Ensure only the first column (date) is clickable for deletion
        if column != 1:
            return

        # Get the date of the clicked booking
        booking_date_to_delete = self.tableWidget.item(row, 1).text()

        # Ask for user confirmation before deleting
        confirmation = QMessageBox.question(self, "Conferma Eliminazione",
                                            f"Vuoi eliminare la prenotazione del {booking_date_to_delete}?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # If the user clicks No, return without deleting
        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            # Find and delete the clicked booking
            for prenotazione in self.prenotazioni_controller.prenotazioni:
                if prenotazione['data'] == booking_date_to_delete:
                    self.prenotazioni_controller.delete_prenotazione(prenotazione)
                    self.prenotazioni_controller.save_to_file()  # Ensure changes are saved
                    QMessageBox.information(self, "Elimina Prenotazione",
                                            f"La prenotazione del {booking_date_to_delete} è stata eliminata.")
                    # Update the table after deletion
                    self.update_table()
                    return

            QMessageBox.information(self, "Elimina Prenotazione", "Nessuna prenotazione trovata con quella data.")
        except Exception as e:
            QMessageBox.critical(self, "Elimina Prenotazione", f"Si è verificato un errore inaspettato: {e}")

    def update_table(self):
        # Clear the table and reload bookings
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        prenotazioni = self.prenotazioni_controller.prenotazioni

        for i, prenotazione in enumerate(prenotazioni):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(prenotazione['username']))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(prenotazione['data']))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(prenotazione['ora']))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(prenotazione['parrucchiere']))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(prenotazione['servizio']))


class vedi_utenti(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utenti")
        self.layout = QVBoxLayout()

        # Create an instance of controller_utente
        utente_controller = controller_utente()
        utente_controller.initialize_user()
        # Create a table widget
        self.tableWidget = QTableWidget()

        # Set the column count for the table
        self.tableWidget.setColumnCount(2)

        # Set the headers for the table
        self.tableWidget.setHorizontalHeaderLabels(["Username", "Password", "User Type"])

        # Add the users to the table
        for i in utente_controller.users:
            a = 0
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(a, 0, QTableWidgetItem(i['username']))
            self.tableWidget.setItem(a, 1, QTableWidgetItem(i['password']))
            self.tableWidget.setItem(a, 2, QTableWidgetItem(i['user_type']))
            a += 1

        # Connect the cellClicked signal to a method that deletes the clicked user
        self.tableWidget.cellClicked.connect(self.delete_selected_user)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show the table
    def delete_selected_user(self, row):
        # Get the username of the clicked user
        username_to_delete = self.tableWidget.item(row, 0).text()

        # Ask for user confirmation before deleting
        confirmation = QMessageBox.question(self, "Conferma Eliminazione",
                                            f"Vuoi eliminare l'utente {username_to_delete}?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            QMessageBox.StandardButton.No)

        # If the user clicks No, return without deleting
        if confirmation == QMessageBox.StandardButton.No:
            return

        # Create an instance of controller_utente
        utente_controller = controller_utente()

        try:
            # Load the users
            utente_controller.initialize_user()

            # Find and delete the clicked user
            for user in utente_controller.users:
                if user['username'] == username_to_delete:
                    utente_controller.delete_user(user)
                    utente_controller.save_to_file()  # Ensure changes are saved
                    QMessageBox.information(self, "Elimina Utente", f"L'utente {username_to_delete} è stato eliminato.")
                    return

            QMessageBox.information(self, "Elimina Utente", "Nessun utente trovato con quel username.")
        except Exception as e:
            QMessageBox.critical(self, "Elimina Utente", f"Si è verificato un errore: {e}")

class view_parrucchieri(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parrucchieri")
        self.layout = QVBoxLayout(self)

        # Create table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)  # Set column count for the table

        # Set headers for the table
        headers = ["Username", "Password", "User Type"]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # Load parrucchieri data
        self.load_parrucchieri_data()

        # Add table widget to layout
        self.layout.addWidget(self.tableWidget)

        # Connect cell clicked signal to delete method
        self.tableWidget.cellClicked.connect(self.delete_selected_parrucchiere)

    def load_parrucchieri_data(self):
        try:
            # Initialize controller for parrucchieri
            parrucchiere_controller = controller_parrucchiere()
            parrucchiere_controller.initialize_user()

            # Clear existing table content
            self.tableWidget.setRowCount(0)

            # Populate table with parrucchieri data
            for index, parrucchiere in enumerate(parrucchiere_controller.parrucchieri):
                username = parrucchiere['username']
                password = parrucchiere['password']
                user_type = parrucchiere['user_type']

                # Insert a new row
                self.tableWidget.insertRow(index)

                # Set items in the table
                self.tableWidget.setItem(index, 0, QTableWidgetItem(username))
                self.tableWidget.setItem(index, 1, QTableWidgetItem(password))
                self.tableWidget.setItem(index, 2, QTableWidgetItem(user_type))

        except Exception as e:
            QMessageBox.critical(self, "Errore Caricamento Parrucchieri", f"Si è verificato un errore: {e}")

    def delete_selected_parrucchiere(self, row, column):
        if column != 0:
            return  # Ignore clicks on non-username cells

        parrucchiere_name_to_delete = self.tableWidget.item(row, column).text()

        confirmation = QMessageBox.question(self, "Conferma Eliminazione",
                                            f"Vuoi eliminare il parrucchiere {parrucchiere_name_to_delete}?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.No:
            return

        try:
            # Initialize controller for parrucchieri
            parrucchiere_controller = controller_parrucchiere()
            parrucchiere_controller.initialize_user()

            # Find and delete the selected parrucchiere
            for parrucchiere in parrucchiere_controller.parrucchieri:
                if parrucchiere['username'] == parrucchiere_name_to_delete:
                    parrucchiere_controller.delete_parrucchiere(parrucchiere)
                    parrucchiere_controller.save_to_file()  # Save changes to file
                    QMessageBox.information(self, "Elimina Parrucchiere",
                                            f"Il parrucchiere {parrucchiere_name_to_delete} è stato eliminato.")
                    # Reload data after deletion
                    self.load_parrucchieri_data()
                    return

            QMessageBox.information(self, "Elimina Parrucchiere", f"Nessun parrucchiere trovato con username {parrucchiere_name_to_delete}.")

        except Exception as e:
            QMessageBox.critical(self, "Elimina Parrucchiere", f"Si è verificato un errore durante l'eliminazione: {e}")

"""
class view_parrucchieri(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parrucchieri")
        self.layout = QVBoxLayout()
        pr = controller_parrucchiere()
        pr.initialize_user()

        # Create a table widget
        self.tableWidget = QTableWidget()


        # Set the column count for the table

        self.tableWidget.setColumnCount(3)

        # Set the headers for the table
        self.tableWidget.setHorizontalHeaderLabels(["Username", "Password", "User Type"])

        # Add the bookings to the table
        for i in pr.parrucchieri:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            a = 0
            self.tableWidget.setItem(a, 0, QTableWidgetItem(i['username']))
            self.tableWidget.setItem(a, 1, QTableWidgetItem(i['password']))
            self.tableWidget.setItem(a, 2, QTableWidgetItem(i['user_type']))
            a+=1
        # Show the table

        self.layout.addWidget(self.tableWidget)
        self.tableWidget.cellClicked.connect(self.delete_selected_parrucchiere)
        self.setLayout(self.layout)


    def delete_selected_parrucchiere(self, row):        # Get the date of the clicked booking
        parrucchiere_name_to_delete = self.tableWidget.item(row, 0).text()

        confirmation = QMessageBox.question(self, "Conferma Eliminazione",
                                            f"Vuoi eliminare il parrucchiere {parrucchiere_name_to_delete}?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            QMessageBox.StandardButton.No)

        # Get the controller for the bookings
        if confirmation == QMessageBox.StandardButton.No:
            return

            # Create an instance of controller_parrucchiere
        parrucchiere_controller = controller_parrucchiere()

        try:
            # Load the parrucchieri
            parrucchiere_controller.initialize_user()

            # Find and delete the clicked parrucchiere
            for parrucchiere in parrucchiere_controller.parrucchieri:
                if parrucchiere['username'] == parrucchiere_name_to_delete:
                        parrucchiere_controller.delete_parrucchiere(parrucchiere)
                        parrucchiere_controller.save_to_file()  # Ensure changes are saved
                        QMessageBox.information(self, "Elimina Parrucchiere",
                                                f"Il parrucchiere {parrucchiere_name_to_delete} è stato eliminato.")
                        return

                QMessageBox.information(self, "Elimina Parrucchiere", "Nessun parrucchiere trovato "
                                                                      "con quella data e username.")
        except Exception as e:
            QMessageBox.critical(self, "Elimina Parrucchiere", f"Si è verificato un errore: {e}")

"""

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = view_admin('admin')
    window.show()
    app.exec()