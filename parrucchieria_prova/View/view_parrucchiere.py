from PyQt6.QtWidgets import QWidget, QMessageBox, QInputDialog
from PyQt6.uic import loadUi
from parrucchieria_prova.Controller.controller_prenotazioni import controller_prenotazioni
from parrucchieria_prova.Controller.controller_parrucchiere import controller_parrucchiere
from parrucchieria_prova.Model.parrucchiere import parrucchiere
class view_parrucchiere(QWidget):
    def __init__(self, username):
        super(view_parrucchiere, self).__init__()
        self.username = username

        # Load the UI
        loadUi("C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\File_ui\\viewparrucchiere.ui", self)

        # Set the window title
        self.setWindowTitle("Parrucchiere Page")

        self.pushButton.setText("Vedi prenotazioni")

        # Connect the widgets to their respective methods
        self.pushButton.clicked.connect(self.view_bookings)
        self.comboBox.addItems(["Profilo", "View Profile", "Modifica Profilo"])


    def view_bookings(self):
        prenotazioni = controller_prenotazioni('C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Prenotazioni.pickle')
        prenotazioni.initialize_prenotazioni()
        bookings_info = ""
        for prenotazione in prenotazioni.prenotazioni:
            bookings_info += f"Username: {prenotazione['username']}\nDate: {prenotazione['data']}\nParrucchiere: {prenotazione['parruchiere']}\nService: {prenotazione['servizio']}\n\n"
        QMessageBox.information(self, "Bookings", bookings_info)

    def handle_profile(self):
        if self.comboBox.currentText() == "View Profile":
            self.view_profile()
        elif self.comboBox.currentText() == "Modifica Profilo":
            self.modifica_profilo()
    def view_profile(self):
        parrucchiere = controller_parrucchiere('C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Parrucchieri.pickle')
        parrucchiere.initialize_user()
        for par in parrucchiere.parrucchieri:
            if par['username'] == self.username:
                return QMessageBox.information(self, "Profile", f"Username: {par['username']}\nPassword: {par['password']}")

    def modifica_profilo(self):
        parru = controller_parrucchiere('C:\\Users\\manue\\Documents\\GitHub\\Progetto\\parrucchieria_prova\\Database\\Lista_Parrucchieri.pickle')
        parru.initialize_user()
        new_username, ok = QInputDialog.getText(self, 'Change Credentials', 'Enter your new username:')
        new_password, ok = QInputDialog.getText(self, 'Change Credentials', 'Enter your new password:')


        # If the user clicked OK and entered a new username and password
        if ok and new_username and new_password:
            # Update the user's details
            new_parrucchiere = parrucchiere(new_username, new_password).to_dict()  # non so se funzionass
            parru.update_parrucchiere(self.username, new_parrucchiere)
            QMessageBox.information(self, "Change Credentials", "Your credentials have been updated.")
            self.username = new_username


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = view_parrucchiere("parrucchiere")
    window.show()
    sys.exit(app.exec())