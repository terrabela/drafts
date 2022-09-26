# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:06:14 2021

@author: mmaduar
"""

# https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#compile

from pathlib import Path

import numpy as np

from src.spec_graphics_class import SpecGraphics
from src.specparms_class import SpecParms


class Spec:
    """ Spectrum class. """

    def __init__(self, f_name=''):
        """
        Initialize a minimal members set from a read spectrum file.

        :param f_name: Spectrum's complete file name.
        :type f_name: str
        # :raise lumache.InvalidKindError: If the kind is invalid.
        :return: 0 if spectrum was successfully opened; -1 otherwise.
        :rtype: int

        """
        self.f_name = f_name
        self.sufx = Path(f_name).suffix.casefold()
        #
        self.spec_parms = SpecParms(self.f_name, self.sufx)
        # self.spec_graphics = SpecGraphics()
        self.pkl_file = Path(self.f_name).with_suffix('.xz')

    @staticmethod
    def curr_h_win(n_ch, i_ch):
        """ Find the current half windows. """
        _a = 0.00125
        _b = 0.00075 * n_ch
        h_win = np.int(np.round(_a * i_ch + _b))
        return h_win

    def total_analysis(self, k_sep_pk=2.0, smoo=3000.0, widths_range=(4.0, 20.0)):
        """Analyze thoroughly a spectrum."""
        self.spec_parms.total_analysis(k_sep_pk, smoo, widths_range)

    def perform_basic_net_area_calculation(self):
        """Perform a very rough net area calculation"""
        self.spec_parms.peaks_parms.basic_net_area_calculation()

    def plot_graphics(self, parms):
        """Plot graphics (?)."""
        self.spec_graphics = SpecGraphics(parms)
        self.spec_graphics.plot_simple_scattergl()
