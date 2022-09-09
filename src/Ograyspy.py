from random import randrange
from typing import List

from src.dir_listing import DirectoryList
from pathlib import Path
from spec_class import Spec

class Ograyspy:
    files_list: list[str]

    def __init__(self, speed=0):
        self.speed = speed
        self.odometer = 0
        self.time = 0
        # self.dir_list = DirectoryList()
        self.curr_path = Path('../../../OwnDrive/Genie_Transfer')
        # print(len(self.dir_list))
        self.files_list = []
        for i in self.curr_path.glob("**/*.[Cc][Hh][Nn]"):
            self.files_list.append('/'.join(i.parts[5:]))
        for i in self.curr_path.glob("**/*.[Ii][Ee][Cc]"):
            self.files_list.append('/'.join(i.parts[5:]))
        self.n_files = len(self.files_list)

    def choose_random_spectrum(self):
        self.a_spec_ind = randrange(self.n_files)


if __name__ == '__main__':
    my_ogra = Ograyspy()
    print("I'm a OGRaySPy (gamma-ray spectra analyzer!")
    print('No. spec files: ', my_ogra.n_files)
    my_ogra.choose_random_spectrum()
    print('Random spec index: ', my_ogra.a_spec_ind)
    a_spec_name: str = my_ogra.files_list[my_ogra.a_spec_ind]
    print('...and its name: ', a_spec_name)
    a_spec = Spec(a_spec_name)
