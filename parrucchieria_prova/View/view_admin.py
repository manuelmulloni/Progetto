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

             loadUi("C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\File_ui\\viewAdmin.ui", self)
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
                 self.change_credentials(self.username) # da inserire

     def handle_hairdresser_action(self, action):
             if action == "Vedi Parrucchieri":
                 self.view_hairdressers()  #implementato
             elif action == "Cambia Parrucchieri":
                 self.change_hairdressers()
             elif action == "Aggiungi Parrucchieri":
                 self.add_hairdressers()


     def view_profile(self):
                 self.ad.initialize_user()
                 admin_profile = self.ad.admins[0]  # Assuming the first admin in the list is the logged-in admin

                 # Create a string with the admin's profile information
                 profile_info = f"Username: {admin_profile['Username']}\nPassword: {admin_profile['Password']}\nUser Type: {admin_profile['User_type']}"

                 # Display the profile information in a dialog box
                 QMessageBox.information(self, "Admin Profile", profile_info)

     def change_credentials(self, old_username):
                 try:
                     # Prompt for new username
                     new_username, ok_username = QInputDialog.getText(self, 'Cambia Credenziali',
                                                                      'Inserisci il nuovo username:')
                     if not ok_username or not new_username.strip():
                         raise ValueError("L'user inserito non è valido")

                     # Prompt for new password
                     new_password, ok_password = QInputDialog.getText(self, 'Cambia Credenziali',
                                                                      'Inserisci la nuova password:')
                     if not ok_password or not new_password.strip():
                         raise ValueError("la password inserita non è valida")

                     # Update the credentials if both inputs are valid
                     if ok_username and ok_password:
                         self.ad.initialize_user()
                         for admin in self.ad.admins:
                             if admin['Username'] == old_username:
                                 # Update the admin's credentials
                                 admin['Username'] = new_username
                                 admin['Password'] = new_password

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
                 parrucchiere_controller = controller_parrucchiere
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
                 for parrucchiere in parrucchiere_controller.parrucchieri:
                     if parrucchiere['username'] == old_username:
                         # Ask the user for the new username and password
                         try:
                             new_username, ok_username = QInputDialog.getText(self, 'Aggiorna Parrucchiere',
                                                                              'Inserisci il nuovo username:')
                             if not ok_username or not new_username.strip():
                                 raise ValueError("Input non valido per il nuovo username")

                             new_password, ok_password = QInputDialog.getText(self, 'Aggiorna Parrucchiere',
                                                                              'Inserisci la nuova password:')
                             if not ok_password or not new_password.strip():
                                 raise ValueError("Input non valido per la nuova password")

                             # Update the hairdresser's details if inputs are valid
                             if ok_username and ok_password:
                                 new_parrucchiere = {'username': new_username, 'password': new_password,
                                                     'user_type': 'Parrucchiere'}
                                 parrucchiere_controller.update_parrucchiere(parrucchiere, new_parrucchiere)
                                 QMessageBox.information(self, "Aggiorna Parrucchiere",
                                                         f"Le credenziali del parrucchiere {old_username} sono state aggiornate.")
                                 return
                         except ValueError as e:
                             QMessageBox.warning(self, "Aggiorna Parrucchiere",
                                                 f"Errore nell'inserimento delle nuove credenziali: {e}")
                         except Exception as e:
                             QMessageBox.warning(self, "Aggiorna Parrucchiere",
                                                 f"Errore durante l'aggiornamento delle credenziali: {e}")
                         return

                 # If the hairdresser was not found
                 QMessageBox.warning(self, "Aggiorna Parrucchiere", "Parrucchiere non trovato.")

     def add_hairdressers(self):
         # Create an instance of controller_parrucchiere
         parrucchiere_controller = controller_parrucchiere()
         try:
             # Load the existing hairdressers
             parrucchiere_controller.initialize_user()
         except Exception as e:
             QMessageBox.critical(self, "Errore", f"Impossibile caricare i dati dei parrucchieri: {e}")
             return

         try:
             # Ask the user for the username and password of the new hairdresser
             new_username, ok_username = QInputDialog.getText(self, 'Aggiungi Parrucchiere',
                                                              'Inserisci il username del nuovo parrucchiere:')
             for parrucchiere in parrucchiere_controller.parrucchieri:
                 if parrucchiere['username'] == new_username:
                     QMessageBox.warning(self, "Aggiungi Parrucchiere", "Il parrucchiere esiste già.")
                     return
                     pass

             if not ok_username or not new_username.strip():
                 raise ValueError("Input non valido per il username")

             new_password, ok_password = QInputDialog.getText(self, 'Aggiungi Parrucchiere',
                                                              'Inserisci la password del nuovo parrucchiere:')
             if not ok_password or not new_password.strip():
                 raise ValueError("Input non valido per la password")

             # If the user clicked OK and entered a username and password
             if ok_username and ok_password:
                 # Create the new hairdresser
                 new_parrucchiere = {'username': new_username.strip(), 'password': new_password.strip(),
                                     'user_type': 'Parrucchiere'}

                 # Add the new hairdresser
                 parrucchiere_controller.add_parrucchiere(new_parrucchiere)
                 QMessageBox.information(self, "Aggiungi Parrucchiere",
                                         f"Parrucchiere {new_username} è stato aggiunto.")

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

        pr = controller_prenotazioni()
        pr.initialize_prenotazioni()

        # Create a table widget
        self.tableWidget = QTableWidget()

        # Set the column count for the table

        self.tableWidget.setColumnCount(4)

        # Set the headers for the table
        self.tableWidget.setHorizontalHeaderLabels(["Username", "Date","Ora", "Parrucchiere", "Service"])

        # Add the bookings to the table
        for i in pr.prenotazioni:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            a = 0
            self.tableWidget.setItem(a, 0, QTableWidgetItem(i['username']))
            self.tableWidget.setItem(a, 1, QTableWidgetItem(i['data']))
            self.tableWidget.setItem(a, 2, QTableWidgetItem(i['ora']))
            self.tableWidget.setItem(a, 3, QTableWidgetItem(i['parruchiere']))
            self.tableWidget.setItem(a, 4, QTableWidgetItem(i['servizio']))
            a += 1
        # Show the table

        self.layout.addWidget(self.tableWidget)
        self.tableWidget.cellClicked.connect(self.delete_selected_booking)
        self.setLayout(self.layout)

    def delete_selected_booking(self, row):
        # Get the date of the clicked booking
        booking_date_to_delete = self.tableWidget.item(row, 1).text()

        # Ask for user confirmation before deleting
        confirmation = QMessageBox.question(self, "Conferma Eliminazione",
                                            f"Vuoi eliminare la prenotazione del {booking_date_to_delete}?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # If the user clicks No, return without deleting
        if confirmation != QMessageBox.StandardButton.Yes:
            return

        # Get the controller for the bookings
        pr = controller_prenotazioni()

        try:
            # Load the bookings
            pr.initialize_prenotazioni()

            if pr.prenotazioni is None:
                raise TypeError("Nessuna prenotazione trovata")

            # Find and delete the clicked booking
            for booking in pr.prenotazioni:
                if booking['data'] == booking_date_to_delete:   # probabilmente da cambiare perche se ci sono piu date uguali darà errore
                    pr.delete_prenotazione(booking)
                    pr.save_to_file()  # Ensure changes are saved
                    QMessageBox.information(self, "Elimina Prenotazione",
                                            f"La prenotazione del {booking_date_to_delete} è stata eliminata.")
                    return

            QMessageBox.information(self, "Elimina Prenotazione", "Nessuna prenotazione trovata con quella data.")
        except TypeError as e:
            QMessageBox.information(self, "Elimina Prenotazione", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Elimina Prenotazione", f"Si è verificato un errore inaspettato: {e}")

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
        self.layout = QVBoxLayout()
        pr = controller_parrucchiere()
        pr.initialize_user()

        # Create a table widget
        self.tableWidget = QTableWidget()


        # Set the column count for the table

        self.tableWidget.setColumnCount(4)

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

                QMessageBox.information(self, "Elimina Parrucchiere", "Nessun parrucchiere trovato con quella data e username.")
        except Exception as e:
                QMessageBox.critical(self, "Elimina Parrucchiere", f"Si è verificato un errore: {e}")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = view_admin('admin')
    window.show()
    app.exec()