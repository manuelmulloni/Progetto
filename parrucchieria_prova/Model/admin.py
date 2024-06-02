

class admin:
    def __init__(self, username, password):
          self.username = username
          self.password = password



    def get_Admin(self):
         return {
             'Username': self.username,
             'Password': self.password,
             'User_type': "Admin"
        } #creo dizionario