class Car:

    @property
    def start(self):
        return 'car is started'

    def powered_start(self):
        return self.start + ' and powered'


machine = Car()
machine
print ( machine.start )
print ( machine.powered_start() )



