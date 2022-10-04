import numpy as np
from scipy.signal import find_peaks
from src.peaksparms_class import PeaksParms


class GenericSeriesAnalysis:
    """Analyze a generic number series to find peaks, estimate their parameters and possibly find baseline."""

    def __init__(self, cnt_arrs):
        # self.cts = counts_to_search
        # self.chans_nzero =
        self.cnt_arrs = cnt_arrs
        self.ys = cnt_arrs.new_y_s
        self.n_ch = self.ys.size
        self.pk_parms = PeaksParms()
        # self.peaks = np.array([])
        # self.pk_hei = np.array([])
        # self.propts = {}
        # self.widths = (None, None)
        # self.width_heights_f = np.array([])
        # self.left_ips_f = np.array([])
        # self.right_ips_f = np.array([])
        self.is_reg = np.zeros(self.n_ch)

        # self.xs_fwhm_lines = np.array([])
        # self.ys_fwhm_lines = np.array([])
        # self.xs_fwb_lines = np.array([])
        # self.ys_fwb_lines = np.array([])
        # self.mix_regions = np.array([])
        # self.plateaux = np.array([])

    def resolve_peaks_and_regions(self, k_sep_pk):
        self.peaks_search()
        print('resolve_peaks_and_regions:')
        print(vars(self.pk_parms))
        # 2022-out-4: Não está funcionando:
        # self.redefine_widths_range()
        # self.peaks_search(self.ys, widths_range=self.widths_pair)
        # self.define_width_lines()
        self.define_multiplets_regions(k_sep_pk)

        # self.ser_an.redefine_widths_range(self.peaks_parms.gross_widths, gross=True)

        # self.ser_an.peaks_search(cts_to_search=self.cnt_array_like.y0s, gross=True,
        #                          widths_range=self.peaks_parms.gross_widths)

        # self.ser_an.define_width_lines(gross=True)
        # self.peaks_parms.define_multiplets_regions(self.cnt_array_like.is_gro_reg,
        #                                            k_sep_pk=k_sep_pk)
        # AQUI calculate_base_line não fica dentro de seires_analysis. Manter aqui.
        # self.c. cnt_array_like.calculate_base_line(self.peaks_parms.mix_regions, smoo)


    #    def initial_peaks_search(self, n_ch, cts_to_search, peaks_to_set, propts_to_set,
    #                             peak_sd_fact=3.0, widths_range=(None, None),
    #                             areas_calc='under_fwhm',
    #                             set_plateaux=False):


    def peaks_search(self, peak_sd_fact=3.0, widths_range=(None, None)):
        """Peaks search; use scipy.signal.find_peaks."""
        height = peak_sd_fact * np.sqrt(self.ys)
        prominence = peak_sd_fact * np.sqrt(self.ys)
        if widths_range == (None, None):
            widths_range = (self.n_ch * 0.0003, self.n_ch * 0.01)
        self.widths_range = widths_range
        peaks, propts = find_peaks(
            self.ys,
            height=height,
            threshold=(None, None),
            prominence=prominence,
            width=widths_range,
            rel_height=0.5)

        plateaux = propts['peak_heights'] - propts['prominences']
        self.pk_parms.peaks = peaks
        self.pk_parms.propts = propts
        self.pk_parms.plateaux = plateaux
        self.pk_parms.fwhm_ch_ini = np.ceil(propts['left_ips']).astype(int)
        self.pk_parms.fwhm_ch_fin = np.floor(propts['right_ips']).astype(int)

    def redefine_widths_range(self):
        """Redefine widths range."""
        ws_min = np.percentile(self.pk_parms.propts['widths'], 25) * 0.5
        ws_max = np.percentile(self.pk_parms.propts['widths'], 75) * 2.0
        self.widths_pair = (ws_min, ws_max)


    def define_multiplets_regions(self, k_sep_pk):
        """Define multiplet regions from already found peaks with proper widths."""
        # k_sep_pk: Fator de fwhm para ampliar multipletos:
        # 2021-06-28
        # 2022-03-24 Vamos refatorar tudo:

        widths_extd = k_sep_pk * self.pk_parms.propts['widths']
        ini_extd = np.round(self.pk_parms.peaks - widths_extd).astype(int)
        fin_extd = np.round(self.pk_parms.peaks + widths_extd).astype(int)
        if self.pk_parms.peaks.any():
            for i_pk, ch_pk in enumerate(self.pk_parms.peaks):
                for i_ch in range(ini_extd[i_pk], fin_extd[i_pk] + 1):
                    if (i_ch >= 0) & (i_ch < self.n_ch):
                        self.is_reg[i_ch] = True

        comuta = np.zeros(self.n_ch)
        for i in range(1, self.n_ch):
            comuta[i] = self.is_reg[i].astype(int) - self.is_reg[i - 1].astype(int)

        # np.nonzero gera uma tupla, não sei por quê.
        inis = np.nonzero(comuta > 0)[0]
        # fins = np.append(np.nonzero(comuta<0), n)
        fins = np.nonzero(comuta < 0)[0]

        # Ajusta comprimento dos arrays. Têm de ser iguais.
        min_size = np.minimum(inis.size, fins.size)
        inis = inis[:min_size]
        fins = fins[:min_size]
        self.mix_regions = np.concatenate(np.array([[inis], [fins]])).T

        print('define_multiplets_regions completado. Define:')
        print('self.mix_regions: ', self.mix_regions)
