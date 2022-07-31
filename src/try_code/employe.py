
#import name_main

class Employe():

    name: str 
    bornedDate: str
    email: str
    role: str
    extra_pay: float

    def __init__ (self, name, role, email):
        self.name = name
        self.role = role
        self.email = email

    def calculate_payment(self) -> float:        
        if self.role == 'leader': return 1000.0
        if self.role == 'programmer': return 700.0

    def set_attributes_by_console(self):
        self.name = input('Employe name: ')
        self.role = input('Role: ')
        self.email = input('Email: ')
        

if __name__ == '__main__':

    # employe = Employe('peter', 'leader') #ok
    employe = Employe(role='leader', name='employe')
    print (employe.calculate_payment())


    employe.role = 'programmer'
    print (employe.calculate_payment())

    employe.set_attributes_by_console()
    print ( employe.name + ' ' + employe.email )  



