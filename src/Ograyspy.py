from random import randrange
from typing import List

from src.dir_listing import DirectoryList
from pathlib import Path
import pickle
import os
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

        my_file = 'ogra_pic_f.pkl'

        if os.path.isfile(my_file):  # if file exists we have already pickled a list
            print('Load existing pickle file')
            with open(my_file, 'rb') as f:
                self.files_list = pickle.load(f)
        else:
            print('Create new pickle file')
            self.files_list = []
            for i in self.curr_path.glob("**/*.[Cc][Hh][Nn]"):
                self.files_list.append('/'.join(i.parts[5:]))
            for i in self.curr_path.glob("**/*.[Ii][Ee][Cc]"):
                self.files_list.append('/'.join(i.parts[5:]))
            with open(my_file, 'wb') as f:
                pickle.dump(self.files_list, f)

        self.n_files = len(self.files_list)

    def choose_random_spectrum(self):
        self.a_spec_ind = randrange(self.n_files)


if __name__ == '__main__':
    my_ogra = Ograyspy()
    print("I'm a OGRaySPy (gamma-ray spectra analyzer!")
    print('No. spec files: ', my_ogra.n_files)

    given_spec_name = "Filtros/2022/Cci/CCI1603-I.Chn"
    if given_spec_name in my_ogra.files_list:
        print("Found!")
        complete_spec_name = '../../../OwnDrive/Genie_Transfer' + '/' + given_spec_name
    else:
        my_ogra.choose_random_spectrum()
        print('Random spec index: ', my_ogra.a_spec_ind)
        a_spec_name: str = my_ogra.files_list[my_ogra.a_spec_ind]
        print('...and its name: ', a_spec_name)
        complete_spec_name = '../../../OwnDrive/Genie_Transfer' + '/' + a_spec_name
    a_spec = Spec(complete_spec_name)
    a_spec.total_analysis()
    # 2022-Jun-24 No momento esses são os que interessam:
    # pann = a_spec.spec_parms
    # cntarr = a_spec.spec_parms.cnt_array_like
    # pkprms = a_spec.spec_parms.peaks_parms
    # 2022-Jun-14
    # (Pode pular e ir direto aos gráficos)
    a_spec.plot_graphics()
