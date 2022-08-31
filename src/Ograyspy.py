from src.dir_listing import DirectoryList


class Ograyspy:

    def __init__(self, speed=0):
        self.speed = speed
        self.odometer = 0
        self.time = 0


if __name__ == '__main__':

    my_ogra = Ograyspy()
    print("I'm a OGRaySPy (gamma-ray spectra analyzer!")
    dir_list = DirectoryList()
    print(dir_list.entries_list)