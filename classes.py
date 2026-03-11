
class Admin:
    def __init__(self, Occupation, Name, Email, Password, ID):
        self.Occupation = Occupation
        self.Name = Name
        self.Email = Email
        self.Password = Password
        self.ID = ID

class Employee:
    def __init__(self, Occupation, Name, Email, Password, ID):
        self.Occupation = Occupation
        self.Name = Name
        self.Email = Email
        self.Password = Password
        self.ID = ID

    def employee_add():
        print("Would you like to add employees?: ")