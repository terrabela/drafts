class Ograyspy:

    def __init__(self, speed=0):
        self.speed = speed
        self.odometer = 0
        self.time = 0

    def say_state(self):
        print("I'm going {} kph!".format(self.speed))

    def accelerate(self):
        self.speed += 5

    def brake(self):
        if self.speed < 5:
            self.speed = 0
        else:
            self.speed -= 5

    def step(self):
        self.odometer += self.speed
        self.time += 1

    def average_speed(self):
        if self.time != 0:
            if self.time != 0:
                return self.odometer / self.time
        else:
            pass


if __name__ == '__main__':

    my_ogra = Ograyspy()
    print("I'm a OGRaySPy (gamma-ray spectra analyzer!")
    while True:
        action = input("What should I do? [A]ccelerate, [B]rake, "
                       "show [O]dometer, or show average [S]peed?").upper()
        if action not in "ABOS" or len(action) != 1:
            print("I don't know how to do that")
            continue
        if action == 'A':
            my_ogra.accelerate()
        elif action == 'B':
            my_ogra.brake()
        elif action == 'O':
            print("The car has driven {} kilometers".format(my_ogra.odometer))
        elif action == 'S':
            print("The car's average speed was {} kph".format(my_ogra.average_speed()))
        my_ogra.step()
        my_ogra.say_state()