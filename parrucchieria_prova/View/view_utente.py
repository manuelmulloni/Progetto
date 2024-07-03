import os
import re
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QCalendarWidget, QPushButton

from parrucchieria_prova.Model.prenotazioni import prenotazioni
from parrucchieria_prova.Controller.controller_utente import controller_utente
from parrucchieria_prova.Controller.controller_prenotazioni import controller_prenotazioni
from parrucchieria_prova.Controller.controller_parrucchiere import controller_parrucchiere
from PyQt6.uic import loadUi
from parrucchieria_prova.Model.utente import utente



class view_utente(QtWidgets.QWidget):
    def __init__(self, username):
        super(view_utente, self).__init__()
        self.username = username  #erroer dovuto da questo

        cartella_file = 'File_ui'
        nome_file = 'viewUtente.ui'
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cartella_file, nome_file))
        loadUi(self.db_path, self)

        self.setWindowTitle(username)
        self.pushButton_2.clicked.connect(self.prenota)

        self.comboBox.addItems(["Profilo", "View Profile", "Cambia Credenziali"])
        self.comboBox_2.addItems(["Prenotazioni", "View Bookings", "Cancella Prenotazioni"])

        self.comboBox.currentIndexChanged.connect(self.handProfile)
        self.comboBox_2.currentIndexChanged.connect(self.handBookings)

    def handProfile(self):
        if self.comboBox.currentText() == "View Profile":
            self.view_profile()
        elif self.comboBox.currentText() == "Cambia Credenziali":
            self.change_credentials()
        self.comboBox.setCurrentIndex(0)

    def handBookings(self):
        if self.comboBox_2.currentText() == "View Bookings":
            self.p = view_bookings(self.username)
            self.p.show()
        elif self.comboBox_2.currentText() == "Cancella Prenotazioni":
            self.p = view_bookings(self.username)
            self.p.show()
        self.comboBox_2.setCurrentIndex(0)

    def view_profile(self):
        try:
            controller_ut = controller_utente()
            controller_ut.initialize_user()
            for ut in controller_ut.users:
                if ut['username'] == self.username:
                    return QMessageBox.information(self, "Profile",
                                                   f"Username: {ut['username']}\nPassword: {ut['password']}")
            QMessageBox.warning(self, "Profilo", "Profilo non trovato.")
        except Exception as e:
            QMessageBox.critical(self, "Profilo", f"C'è stato un errore nel mentre cercavi il profilo: {e}")

    def change_credentials(self):  #errore nel rivedere il profilo
        try:
            # Initialize user controller
            utent = controller_utente()
            utent.initialize_user()

            # Get new username and validate
            new_username, ok_username = QInputDialog.getText(self, 'Cambia credenziali', 'Inserisci nuovo username:')
            if not ok_username or not new_username.strip():
                raise ValueError("Username non valido")

            # Check if new username already exists
            if any(user['username'] == new_username for user in utent.users if user['username'] != self.username):
                raise ValueError("Username già esistente")

            # Get new password and validate
            new_password, ok_password = QInputDialog.getText(self, 'Cambia credenziali', 'Inserisci la nuova password:')
            if not ok_password or not new_password.strip():
                raise ValueError("Password non valida")

            # Find the user and update credentials
            user_found = False
            for ut in utent.users:
                if ut['username'] == self.username:
                    ut['username'] = new_username
                    ut['password'] = new_password
                    utent.save_to_file()  # Save changes to file (assuming this method exists)
                    self.username = new_username
                    QMessageBox.information(self, "Cambia credenziali",
                                            "Le credenziali sono state aggiornate con successo.")
                    user_found = True
                    break

            if not user_found:
                QMessageBox.warning(self, "Cambia credenziali", "Profilo non trovato.")

        except ValueError as ve:
            QMessageBox.warning(self, "Cambia credenziali", f"Errore: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Cambia credenziali",
                                 f"C'è stato un errore durante l'aggiornamento delle credenziali: {e}")



    def prenota(self):
        try:
            # Initialize booking controller and set up initial data
            prenot = controller_prenotazioni()
            prenot.initialize_prenotazioni()

            # Create the calendar widget for date selection
            calendar = QCalendarWidget()
            calendar.setGridVisible(True)
            calendar.setMinimumDate(QtCore.QDate.currentDate())

            # Set up the calendar dialog
            calendar_dialog = QDialog(self)
            calendar_dialog.setWindowTitle("Seleziona data")
            layout = QVBoxLayout()
            layout.addWidget(calendar)

            # Add the select date button
            btn_select = QPushButton("Seleziona Data")
            layout.addWidget(btn_select)
            calendar_dialog.setLayout(layout)

            selected_date = None

            # Function to handle date selection
            def select_date():
                nonlocal selected_date
                selected_date = calendar.selectedDate().toString(QtCore.Qt.DateFormat.ISODate)
                calendar_dialog.accept()

            btn_select.clicked.connect(select_date)

            # Show the calendar dialog and wait for user selection
            if calendar_dialog.exec() == QDialog.DialogCode.Accepted and selected_date:
                # Check if the selected date is before today
                if calendar.selectedDate() < QtCore.QDate.currentDate():
                    raise ValueError("Non puoi prenotare in un periodo precedente a oggi.")

                # Get the time input from the user
                new_ora, ok_ora = QInputDialog.getText(self, 'Prenota', 'Inserisci l\'ora (hh:mm):')

                if not ok_ora or not new_ora.strip():
                    raise ValueError("Ora non valida: inserisci un'ora nel formato hh:mm")

                # Validate the time format using regular expression
                time_pattern = re.compile(r'^\d{2}:\d{2}$')
                if not time_pattern.match(new_ora.strip()):
                    raise ValueError("Ora non valida: inserisci un'ora nel formato hh:mm")

                # Additional check for valid hour and minute ranges
                hours, minutes = map(int, new_ora.split(':'))
                if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                    raise ValueError("Ora non valida: inserisci un'ora nel formato hh:mm")

                # Read the list of hairdressers from the controller
                parru = controller_parrucchiere()
                parru.initialize_user()
                hairdressers = [parr['username'] for parr in parru.parrucchieri]

                # Get the hairdresser's name from the user from the list
                new_parrucchiere, ok_parrucchiere = QInputDialog.getItem(self, 'Prenota', 'Seleziona il parrucchiere:',
                                                                         hairdressers, 0, False)
                if not ok_parrucchiere or not new_parrucchiere.strip():
                    raise ValueError("Parrucchiere non valido: seleziona un nome valido")

                # Get the service selection from the user
                services = ["Taglio", "Colore", "Piega"]
                selected_service, ok_service = QInputDialog.getItem(self, 'Prenota', 'Seleziona il servizio:', services,
                                                                    0, False)
                if not ok_service:
                    raise ValueError("Nessun servizio selezionato.")

                # Create a new booking and add it to the booking system
                new_prenotazione = prenotazioni(self.username, selected_date, new_ora, new_parrucchiere,
                                                selected_service)
                prenot.add_prenotazione(new_prenotazione.get_Prenotazioni())

                # Show success message
                QMessageBox.information(self, "Prenota", f"Prenotazione effettuata con successo.")

        except ValueError as ve:
            # Handle and display any errors
            QMessageBox.warning(self, "Prenota", f"Errore: {ve}")


class view_bookings(QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Prenotazioni")
        self.layout = QVBoxLayout()
        self.username = username
        self.pr = controller_prenotazioni()
        self.pr.initialize_prenotazioni()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Username", "Data", "Ora", "Parrucchiere", "Servizio"])

        # Popola la tabella con le prenotazioni dell'utente corrente
        self.populate_table_with_user_bookings()

        self.layout.addWidget(self.tableWidget)
        self.tableWidget.cellClicked.connect(self.delete_selected_booking)
        self.setLayout(self.layout)

    def populate_table_with_user_bookings(self):
        self.tableWidget.setRowCount(0)  # Cancella le righe esistenti

        # Itera sulle prenotazioni e aggiungi solo quelle che corrispondono al nome utente corrente
        for prenotazione in self.pr.prenotazioni:
            if prenotazione['username'] == self.username:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                self.set_table_row(row_position, prenotazione)

    def set_table_row(self, row_position, prenotazione):
        self.tableWidget.setItem(row_position, 0, QTableWidgetItem(prenotazione.get('username', '')))
        self.tableWidget.setItem(row_position, 1, QTableWidgetItem(prenotazione.get('data', '')))
        self.tableWidget.setItem(row_position, 2, QTableWidgetItem(prenotazione.get('ora', '')))
        self.tableWidget.setItem(row_position, 3, QTableWidgetItem(prenotazione.get('parrucchiere', '')))
        self.tableWidget.setItem(row_position, 4, QTableWidgetItem(prenotazione.get('servizio', '')))

    def delete_selected_booking(self, row, column):
        booking_date_to_delete = self.tableWidget.item(row, 1).text()

        try:
            bookings = self.pr.get_bookings(self.username)
            if bookings is None:
                raise TypeError

            for booking in bookings:
                if booking['username'] == self.username and booking['data'] == booking_date_to_delete:
                    self.pr.delete_prenotazione(booking)
                    QMessageBox.information(self, "Delete Booking",
                                            f"Prenotazione del {booking_date_to_delete} è stata eliminata.")
                    self.populate_table_with_user_bookings()  # Aggiorna la tabella dopo l'eliminazione
                    return

            QMessageBox.information(self, "Delete Booking", "Nessuna prenotazione selezionata.")
        except TypeError:
            QMessageBox.information(self, "Delete Booking", "Nessuna prenotazione selezionata.")
        except Exception as e:
            QMessageBox.critical(self, "Delete Booking",
                                 f"C'è stato un errore nel mentre cancellavi la prenotazione: {e}")

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = view_utente("Ut")
    window.show()
    sys.exit(app.exec())
