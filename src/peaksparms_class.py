# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 12:11:50 2021

@author: mmaduar
"""

import numpy as np
from scipy.signal import find_peaks


class PeaksParms:
    """Peaks set parameters (heights, widths etc)."""

    def __init__(self):
        self.peaks_gro = np.array([])
        self.peaks_net = np.array([])
        self.pk_hei_gro = np.array([])
        self.propts_gro = {}
        self.propts_net = {}
        self.gross_widths = (None, None)
        self.net_widths = (None, None)
        # self.width_heights_f = np.array([])
        # self.left_ips_f = np.array([])
        # self.right_ips_f = np.array([])

        self.xs_fwhm_lines = np.array([])
        self.ys_fwhm_lines = np.array([])
        self.xs_fwb_lines = np.array([])
        self.ys_fwb_lines = np.array([])

        self.mix_regions = np.array([])

        self.plateaux = np.array([])


    #    def initial_peaks_search(self, n_ch, cts_to_search, peaks_to_set, propts_to_set,
    #                             peak_sd_fact=3.0, widths_range=(None, None),
    #                             areas_calc='under_fwhm',
    #                             set_plateaux=False):
    def peaks_search(self, cts_to_search, gross=False, peak_sd_fact=3.0, widths_range=(None, None)):
        """Peaks search; use scipy.signal.find_peaks."""
        n_ch = cts_to_search.size
        height = peak_sd_fact * np.sqrt(cts_to_search)
        prominence = peak_sd_fact * np.sqrt(cts_to_search)
        if gross:
            if widths_range == (None, None):
                widths_range = (n_ch * 0.0003, n_ch * 0.01)
            self.widths_range_gro = widths_range
            self.peaks_gro, self.propts_gro = find_peaks(
                cts_to_search,
                height=height,
                threshold=(None, None),
                prominence=prominence,
                width=widths_range,
                rel_height=0.5)

            self.plateaux = self.propts_gro['peak_heights'] - self.propts_gro['prominences']
            self.fwhm_ch_ini_gro = np.ceil(self.propts_gro['left_ips']).astype(int)
            self.fwhm_ch_fin_gro = np.floor(self.propts_gro['right_ips']).astype(int)
        else:
            if widths_range == (None, None):
                widths_range = (n_ch * 0.0003, n_ch * 0.01)
            self.widths_range_net = widths_range
            self.peaks_net, self.propts_net = find_peaks(
                cts_to_search,
                height=height,
                threshold=(None, None),
                prominence=prominence,
                width=widths_range,
                rel_height=0.5)
            self.fwhm_ch_ini_net = np.ceil(self.propts_gro['left_ips']).astype(int)
            self.fwhm_ch_fin_net = np.floor(self.propts_gro['right_ips']).astype(int)

    def redefine_widths_range(self, widths_pair, gross):
        """Redefine widths range."""
        ws_min = np.percentile(self.propts_gro['widths'], 25) * 0.5
        ws_max = np.percentile(self.propts_gro['widths'], 75) * 2.0
        widths_pair = (ws_min, ws_max)

    def define_width_lines(self, gross):
        """Build width peaks related lines, just for plotting."""
        if gross:
            n_pk = self.peaks_gro.size
        else:
            n_pk = self.peaks_net.size
        if n_pk != 0:
            if gross:
                self.xs_fwhm_lines_gro = np.concatenate(np.stack(
                    (self.propts_gro['left_ips'], self.propts_gro['right_ips'],
                     np.full(n_pk, None)), axis=1))
                self.ys_fwhm_lines_gro = np.concatenate(np.stack(
                    (self.propts_gro['width_heights'],
                     self.propts_gro['width_heights'],
                     np.full(n_pk, None)), axis=1))
                self.xs_fwb_lines = np.concatenate(np.stack(
                    (self.fwhm_ch_ini_gro, self.fwhm_ch_fin_gro, np.full(n_pk, None)),
                    axis=1))
                self.ys_fwb_lines = np.concatenate(np.stack(
                    (self.plateaux, self.plateaux, np.full(n_pk, None)), axis=1))
            else:
                self.xs_fwhm_lines_net = np.concatenate(np.stack(
                    (self.propts_net['left_ips'], self.propts_net['right_ips'],
                     np.full(n_pk, None)), axis=1))
                self.ys_fwhm_lines_net = np.concatenate(np.stack(
                    (self.propts_net['width_heights'],
                     self.propts_net['width_heights'],
                     np.full(n_pk, None)), axis=1))

    def define_multiplets_regions(self, is_reg, k_sep_pk):
        """Define multiplet regions from already found peaks with proper widths."""
        # k_sep_pk: Fator de fwhm para ampliar multipletos:
        # 2021-06-28
        # 2022-03-24 Vamos refatorar tudo:
        n_ch = is_reg.size
        widths_extd = k_sep_pk * self.propts_gro['widths']
        ini_extd = np.round(self.peaks_gro - widths_extd).astype(int)
        fin_extd = np.round(self.peaks_gro + widths_extd).astype(int)
        if self.peaks_gro.any():
            for i_pk, ch_pk in enumerate(self.peaks_gro):
                for i_ch in range(ini_extd[i_pk], fin_extd[i_pk] + 1):
                    if (i_ch >= 0) & (i_ch < n_ch):
                        is_reg[i_ch] = True

        comuta = np.zeros(n_ch)
        for i in range(1, n_ch):
            comuta[i] = is_reg[i].astype(int) - is_reg[i - 1].astype(int)

        # np.nonzero gera uma tupla, não sei por quê.
        inis = np.nonzero(comuta > 0)[0]
        # fins = np.append(np.nonzero(comuta<0), n)
        fins = np.nonzero(comuta < 0)[0]

        # Ajusta comprimento dos arrays. Têm de ser iguais.
        min_size = np.minimum(inis.size, fins.size)
        inis = inis[:min_size]
        fins = fins[:min_size]
        self.mix_regions = np.concatenate(np.array([[inis], [fins]])).T

        print('define_GROSS_multiplets_regions completado. Define:')
        print('self.mix_regions: ', self.mix_regions)

    def define_net_multiplets_regions(self, is_reg, k_sep_pk):
        """Define multiplet regions from already found peaks with proper widths."""
        # k_sep_pk: Fator de fwhm para ampliar multipletos:
        # 2021-06-28
        # 2022-03-24 Vamos refatorar tudo:
        n_ch = is_reg.size
        widths_extd = k_sep_pk * self.propts_net['widths']
        ini_extd = np.round(self.peaks_net - widths_extd).astype(int)
        fin_extd = np.round(self.peaks_net + widths_extd).astype(int)
        if self.peaks_net.any():
            for i_pk, ch_pk in enumerate(self.peaks_net):
                for i_ch in range(ini_extd[i_pk], fin_extd[i_pk] + 1):
                    if (i_ch >= 0) & (i_ch < n_ch):
                        is_reg[i_ch] = True

        comuta = np.zeros(n_ch)
        for i in range(1, n_ch):
            comuta[i] = is_reg[i].astype(int) - is_reg[i - 1].astype(int)

        # np.nonzero gera uma tupla, não sei por quê.
        inis = np.nonzero(comuta > 0)[0]
        # fins = np.append(np.nonzero(comuta<0), n)
        fins = np.nonzero(comuta < 0)[0]

        # Ajusta comprimento dos arrays. Têm de ser iguais.
        min_size = np.minimum(inis.size, fins.size)
        inis = inis[:min_size]
        fins = fins[:min_size]
        self.net_regions = np.concatenate(np.array([[inis], [fins]])).T

        print('define_NET_multiplets_regions completado')

    def net_width_lines(self):
        """Build width peaks related lines, just for plotting."""
        n_pk = self.peaks_net.size
        if n_pk != 0:
            self.net_xs_fwhm_lines = np.concatenate(np.stack(
                (self.propts_net['left_ips'], self.propts_net['right_ips'],
                 np.full(n_pk, None)), axis=1))
            self.net_ys_fwhm_lines = np.concatenate(np.stack(
                (self.propts_net['width_heights'],
                 self.propts_net['width_heights'],
                 np.full(n_pk, None)), axis=1))
