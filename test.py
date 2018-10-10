class Person:
    kind = 'human'

    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __del__(self):
        print('good bye')
    @classmethod
    def what_is_your_kind(cls):
        print('This is a class method.', cls.kind)
    def drive(self):
        if self.age >= 18:
            print('{} is allowed to drive'.format(self.name))
        else:
            raise Exception('{} is not legally allowed to drive'.format(self.name))
    def say_something(self):
        print('Hi, my name is {}, and {} years old.'.format(self.name, self.age))
    def run(self, num):
        print('run' * num)

class Minor(Person):
    def __init_(self, name, age):
        if(age < 18):
            super.__init__(name, age)
        else:
            raise ValueError

class Adult(Person):
    def __init_(self, name, age):
        if(age >= 18):
            super.__init__(name, age)
        else:
            raise ValueError

Person.what_is_your_kind()
minor = Minor('Chucky', 5)
minor.say_something()
adult = Adult('Aoi Sora', 28)
adult.say_something()


class Car:
    def __init__(self, maker):
        self.maker = maker
    def run(self):
        print('run')
    def ride(self, person):
        person.drive()

class Toyota(Car):
    def __init__(self, maker='Toyota', model="Corolla"):
        super().__init__(maker)
        self.model = model
    def run(self):
        print('{} {} is Super fast'.format(self.maker, self.model))

class Tesla(Car):
    def __init__(self, maker='Tesla', model="Model S", enable_auto_run=False):
        super().__init__(maker)
        self.model = model
        self.__enable_auto_run = enable_auto_run
    @property
    def enable_auto_run(self):
        return self.__enable_auto_run
    @enable_auto_run.setter
    def enable_auto_run(self, is_enable=True):
        self.__enable_auto_run = is_enable
    def run(self):
        print('{} {} is electric fast'.format(self.maker, self.model))



supra = Toyota(maker='Toyota', model="Supra RZ")
supra.run()
print(supra.model)


tesla = Tesla()
tesla.run()
tesla.enable_auto_run = True
print(tesla.model, tesla.enable_auto_run)

supra.ride(adult)
