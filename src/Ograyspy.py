from src.dir_listing import DirectoryList
from pathlib import Path

class Ograyspy:

    def __init__(self, speed=0):
        self.speed = speed
        self.odometer = 0
        self.time = 0
        # self.dir_list = DirectoryList()
        self.curr_path = Path('../../../OwnDrive/Genie_Transfer')
        # print(len(self.dir_list))
        self.files_list = ['/'.join(i.parts[5:]) for i in self.curr_path.glob('**/*.[Cc][Hh][Nn]')]
        print('\n printou \n')
        print(self.files_list)
        print(len(self.files_list))

    def choose_spectrum(self):
        # rand_spec = random(len(self.dir_list))
        pass


if __name__ == '__main__':

    my_ogra = Ograyspy()
    print("I'm a OGRaySPy (gamma-ray spectra analyzer!")
