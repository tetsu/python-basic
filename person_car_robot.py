class Person:
    def talk(self):
        print('I can talk.')

class Car:
    def run(self):
        print('I can run.')

class PersonCarRobot(Person, Car):
    def fly(self):
        print('I believe I can fly.')

person_car_robot = PersonCarRobot()
person_car_robot.talk()
person_car_robot.run()
person_car_robot.fly()
