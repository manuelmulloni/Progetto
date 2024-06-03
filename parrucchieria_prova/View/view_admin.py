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
         self.ad = controller_admin('C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Admin.pickle')

         loadUi("C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\File_ui\\viewAdmin.ui", self)
         self.setWindowTitle(username)
         self.VediUtenti.clicked.connect(self.view_and_delete_users)
         self.pushButton_2.clicked.connect(self.view_and_delete_bookings)

         self.comboBox_2.addItems(["Profilo","Vedi Profilo", "Cambia Profilo"])
         self.comboBox.addItems(
             ["Parrucchieri","Vedi Parrucchieri", "Cambia Parrucchieri", "Elimina Parrucchieri", "Aggiungi Parrucchieri"])

         # Connect the combo boxes to methods
         self.comboBox_2.currentTextChanged.connect(self.handle_profile_action)
         self.comboBox.currentTextChanged.connect(self.handle_hairdresser_action)
     def handle_profile_action(self, action):
             if action == "Vedi Profilo":
                 self.view_profile()
             elif action == "Cambia Profilo":
                 self.change_profile() # da inserire

     def handle_hairdresser_action(self, action):
             if action == "Vedi Parrucchieri":
                 self.view_hairdressers()
             elif action == "Cambia Parrucchieri":
                 self.change_hairdressers()
             elif action == "Elimina Parrucchieri":
                 self.delete_hairdressers()
             elif action == "Aggiungi Parrucchieri":
                 self.add_hairdressers()


     def view_profile(self):
                 self.ad.initialize_user()
                 admin_profile = self.ad.admins[self.username]  # Assuming the first admin in the list is the logged-in admin

                 # Create a string with the admin's profile information
                 profile_info = f"Username: {admin_profile['Username']}\nPassword: {admin_profile['Password']}\nUser Type: {admin_profile['User_type']}"

                 # Display the profile information in a dialog box
                 QMessageBox.information(self, "Admin Profile", profile_info)

     def change_credentials(self, old_username, new_username, new_password):
         # Find the admin with the old username
         self.ad.initialize_user()
         for admin in self.ad.admins:
             if admin.username == old_username:
                 # Update the admin's credentials
                 admin.username = new_username
                 admin.password = new_password

                 # Save the updated list of admins to the file
                 self.save_to_file()
                 return

         print("Admin not found")

     def view_hairdressers(self):
         parrucchiere_controller = controller_parrucchiere(
             'C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Parrucchieri.pickle')

         parrucchiere_controller.initialize_user()
         # Get all hairdressers

         # Create a string with all the hairdresser information
         parrucchieri_info = ""
         for parrucchiere in parrucchiere_controller.parrucchieri:
             parrucchieri_info += f"Username: {parrucchiere['username']}\n\n"

         # Display the hairdresser information in a dialog box
         QMessageBox.information(self, "All Hairdressers", parrucchieri_info)


     def change_hairdressers(self):
        # Create an instance of controller_parrucchiere
        parrucchiere_controller = controller_parrucchiere(
            'C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Parrucchieri.pickle')

        # Ask the user for the username of the hairdresser they want to update
        old_username, ok = QInputDialog.getText(self, 'Update Hairdresser',
                                                'Enter the username of the hairdresser you want to update:')

        # If the user clicked OK and entered a username
        if ok and old_username:
            # Find the hairdresser with the specified username
            for parrucchiere in parrucchiere_controller.parrucchieri:
                if parrucchiere['username'] == old_username:
                    # Ask the user for the new username and password
                    new_username, ok = QInputDialog.getText(self, 'Update Hairdresser', 'Enter the new username:')
                    new_password, ok = QInputDialog.getText(self, 'Update Hairdresser', 'Enter the new password:')

                    if ok and new_username and new_password:
                        # Update the hairdresser's details
                        new_parrucchiere = {'username': new_username, 'password': new_password,
                                            'user_type': 'Parrucchiere'}
                        parrucchiere_controller.update_parrucchiere(parrucchiere, new_parrucchiere)
                        QMessageBox.information(self, "Update Hairdresser",
                                                f"Hairdresser {old_username} has been updated.")
                        return

            # If the hairdresser was not found
            QMessageBox.warning(self, "Update Hairdresser", "Hairdresser not found.")


     def delete_hairdressers(self):
        # Create an instance of controller_parrucchiere
        parrucchiere_controller = controller_parrucchiere(
            'C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Parrucchieri.pickle')

        # Ask the user for the username of the hairdresser they want to delete
        username_to_delete, ok = QInputDialog.getText(self, 'Delete Hairdresser',
                                                      'Enter the username of the hairdresser you want to delete:')

        # If the user clicked OK and entered a username
        if ok and username_to_delete:
            # Find the hairdresser with the specified username
            for parrucchiere in parrucchiere_controller.parrucchieri:
                if parrucchiere['username'] == username_to_delete:
                    # Delete the hairdresser
                    parrucchiere_controller.delete_parrucchiere(parrucchiere)
                    QMessageBox.information(self, "Delete Hairdresser",
                                            f"Hairdresser {username_to_delete} has been deleted.")
                    return

            # If the hairdresser was not found
            QMessageBox.warning(self, "Delete Hairdresser", "Hairdresser not found.")


     def add_hairdressers(self):
         # Create an instance of controller_parrucchiere
         parrucchiere_controller = controller_parrucchiere(
             'C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Parrucchieri.pickle')

         # Ask the user for the username and password of the new hairdresser
         new_username, ok = QInputDialog.getText(self, 'Add Hairdresser', 'Enter the username of the new hairdresser:')
         new_password, ok = QInputDialog.getText(self, 'Add Hairdresser', 'Enter the password of the new hairdresser:')

         # If the user clicked OK and entered a username and password
         if ok and new_username and new_password:
             # Create the new hairdresser
             new_parrucchiere = {'username': new_username, 'password': new_password, 'user_type': 'Parrucchiere'}

             # Add the new hairdresser
             parrucchiere_controller.add_parrucchiere(new_parrucchiere)
             QMessageBox.information(self, "Add Hairdresser", f"Hairdresser {new_username} has been added.")

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

        pr = controller_prenotazioni(
            'C:\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Prenotazioni.pickle')
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


    def delete_selected_booking(self, row, column):  # Get the date of the clicked booking
        booking_date_to_delete = self.tableWidget.item(row, 1).text()

        # Get the controller for the bookings
        pr = controller_prenotazioni(
            'C:\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Prenotazioni.pickle')
        pr.initialize_prenotazioni()

        # Get the user's bookings
        try:
            if pr.prenotazioni is None:
                raise TypeError
            else:
                # Find and delete the clicked booking
                for booking in pr.prenotazioni:
                   pr.delete_prenotazione(booking)
                   QMessageBox.information(self, "Delete Booking",
                                                f"Booking {booking_date_to_delete} has been deleted.")
                   return

                QMessageBox.information(self, "Delete Booking", "No booking found with that date.")
        except TypeError:
            QMessageBox.information(self, "Delete Booking", "No bookings found.")


class vedi_utenti(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utenti")
        self.layout = QVBoxLayout()

        # Create an instance of controller_utente
        utente_controller = controller_utente(
            'C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Utenti.pickle')
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
    def delete_selected_user(self, row, column):
        # Get the username of the clicked user
        username_to_delete = self.tableWidget.item(row, 0).text()

        # Create an instance of controller_utente
        utente_controller = controller_utente(
            'C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Utenti.pickle')
        utente_controller.initialize_user()
        # Find and delete the clicked user
        for user in utente_controller.users:
            if user['username'] == username_to_delete:
                utente_controller.delete_user(user)
                QMessageBox.information(self, "Delete User", f"User {username_to_delete} has been deleted.")
                return

        QMessageBox.information(self, "Delete User", "No user found with that username.")



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = view_admin('admin')
    window.show()
    app.exec()