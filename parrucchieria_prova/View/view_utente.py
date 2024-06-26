from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt6.uic import loadUi
from parrucchieria_prova.Model.utente import utente
from parrucchieria_prova.Controller.controller_utente import controller_utente
from parrucchieria_prova.Controller.controller_prenotazioni import controller_prenotazioni
class view_utente(QtWidgets.QWidget):
    def __init__(self,username):
        super(view_utente,self).__init__()
        self.username = username

        # self.ut = controller_utente('C:\\Users\\manue\\PycharmProjects\\parrucchieria_prova\\File_ui\\viewUtente.ui')    in teoria non serve

        loadUi("C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\File_ui\\viewUtente.ui", self)

        self.setWindowTitle(username)
        self.pushButton_2.clicked.connect(self.view_bookings)

        self.comboBox.addItems(["Profilo","View Profile","Cambia Credenziali"])
        self.comboBox_2.addItems(["Prenotazioni","View Bookings","Cancella Prenotazioni"])

        self.comboBox.currentIndexChanged.connect(self.handProfile)
        self.comboBox_2.currentIndexChanged.connect(self.handBookings)

    def handProfile(self):
        if self.comboBox.currentText() == "View Profile":
            self.view_profile()
        else:
            self.change_credentials()

    def handBookings(self):
        if self.comboBox_2.currentText() == "View Bookings":
            self.view_bookings(self.username)
        else:
            self.view_bookings(self.username)
    def view_profile(self):
        # Get the user's details
        controller_ut = controller_utente()
        controller_ut.initialize_user()
        user = controller_ut.get_user(self.username)

        print(user)
        # Create a string with the user's details
        user_info = f"Username: {user['username']}\n Password: {user['password']}\n User Type: {user['user_type']}"

        # Display the user's details in a dialog box
        QMessageBox.information(self, "User Profile", user_info)

    def change_credentials(self):
        # Ask the user for the new username and password
        new_username, ok = QInputDialog.getText(self, 'Change Credentials', 'Enter your new username:')
        new_password, ok = QInputDialog.getText(self, 'Change Credentials', 'Enter your new password:')

        controller_ut2 = controller_utente()
        controller_ut2.initialize_user()

        # If the user clicked OK and entered a new username and password
        if ok and new_username and new_password:
            # Update the user's details
            new_user = utente(new_username, new_password).to_dict() # non so se funzionass
            controller_ut2.update_user(self.username, new_user)
            QMessageBox.information(self, "Change Credentials", "Your credentials have been updated.")
            self.username = new_username

    def view_bookings(self, username):
            # Get the user's bookings
            self.p = view_bookings(username)
            self.p.show()
            """
            bookings = pr.get_bookings(self.username)
            try:
             # Create a string with the user's bookings
                bookings_info = "\n".join([
                                              f"Booking ID: {booking['id']}\nDate: {booking['date']}\nTime: {booking['time']}\nService: {booking['service']}\n"
                                              for booking in bookings])


                # Display the user's bookings in a dialog box
                QMessageBox.information(self, "User Bookings", bookings_info)
            except:

                QMessageBox.information(self, "User Bookings", "No bookings found.")
            """


class view_bookings(QDialog):
    def __init__(self,username):
        super().__init__()
        self.setWindowTitle("Prenotazioni")
        self.layout = QVBoxLayout()
        self.username = username
        pr = controller_prenotazioni()
        pr.initialize_prenotazioni()

        # Create a table widget
        self.tableWidget = QTableWidget()


        # Set the column count for the table

        self.tableWidget.setColumnCount(4)

        # Set the headers for the table
        self.tableWidget.setHorizontalHeaderLabels(["Username", "Date","ora", "Parrucchiere", "Service"])

        # Add the bookings to the table
        for i in pr.prenotazioni:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            a = 0
            self.tableWidget.setItem(a, 0, QTableWidgetItem(i['username']))
            self.tableWidget.setItem(a, 1, QTableWidgetItem(i['data']))
            self.tableWidget.setItem(a, 2, QTableWidgetItem(i['ora']))
            self.tableWidget.setItem(a, 3, QTableWidgetItem(i['parruchiere']))
            self.tableWidget.setItem(a, 4, QTableWidgetItem(i['servizio']))
            a+=1
        # Show the table

        self.layout.addWidget(self.tableWidget)
        self.tableWidget.cellClicked.connect(self.delete_selected_booking)
        self.setLayout(self.layout)

    def delete_selected_booking(self, row, column):        # Get the date of the clicked booking
        booking_date_to_delete = self.tableWidget.item(row, 1).text()

        # Get the controller for the bookings
        pr = controller_prenotazioni()
        pr.initialize_prenotazioni()

        # Get the user's bookings
        bookings = pr.get_bookings(self.username)
        try:
            if bookings is None:
                raise TypeError
            else:
            # Find and delete the clicked booking
                for booking in bookings:
                    if booking['username'] == self.username and booking['data'] == booking_date_to_delete:
                        pr.delete_prenotazione(booking)
                        QMessageBox.information(self, "Delete Booking", f"Booking {booking_date_to_delete} has been deleted.")
                        return

                QMessageBox.information(self, "Delete Booking", "No booking found with that date.")
        except TypeError:
            QMessageBox.information(self, "Delete Booking", "No bookings found.")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = view_utente("test")
    window.show()
    sys.exit(app.exec())