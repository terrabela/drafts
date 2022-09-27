import numpy as np
from scipy.signal import find_peaks


class GenericSeriesAnalysis:
    """Analyze a generic number series to find peaks, estimate their parameters and possibly find baseline."""

    def __init__(self):
        self.peaks = np.array([])
        self.pk_hei = np.array([])
        self.propts = {}
        self.widths = (None, None)
        # self.width_heights_f = np.array([])
        # self.left_ips_f = np.array([])
        # self.right_ips_f = np.array([])

        self.xs_fwhm_lines = np.array([])
        self.ys_fwhm_lines = np.array([])
        self.xs_fwb_lines = np.array([])
        self.ys_fwb_lines = np.array([])
        self.mix_regions = np.array([])
        self.plateaux = np.array([])

    def peaks_search(self, cts_to_search, peak_sd_fact=3.0, widths_range=(None, None)):
        """Peaks search; use scipy.signal.find_peaks."""
        n_ch = cts_to_search.size
        height = peak_sd_fact * np.sqrt(cts_to_search)
        prominence = peak_sd_fact * np.sqrt(cts_to_search)
        if widths_range == (None, None):
            widths_range = (n_ch * 0.0003, n_ch * 0.01)
        self.widths_range = widths_range
        self.peaks, self.propts = find_peaks(
            cts_to_search,
            height=height,
            threshold=(None, None),
            prominence=prominence,
            width=widths_range,
            rel_height=0.5)

        self.plateaux = self.propts['peak_heights'] - self.propts['prominences']
        self.fwhm_ch_ini = np.ceil(self.propts['left_ips']).astype(int)
        self.fwhm_ch_fin = np.floor(self.propts['right_ips']).astype(int)

    def redefine_widths_range(self, widths_pair):
        """Redefine widths range."""
        ws_min = np.percentile(self.propts['widths'], 25) * 0.5
        ws_max = np.percentile(self.propts['widths'], 75) * 2.0
        widths_pair = (ws_min, ws_max)

    def define_width_lines(self, gross):
        """Build width peaks related lines, just for plotting."""
        n_pk = self.peaks.size
        if n_pk != 0:
            self.xs_fwhm_lines_gro = np.concatenate(np.stack(
                (self.propts['left_ips'], self.propts['right_ips'],
                 np.full(n_pk, None)), axis=1))
            self.ys_fwhm_lines_gro = np.concatenate(np.stack(
                (self.propts['width_heights'],
                 self.propts['width_heights'],
                 np.full(n_pk, None)), axis=1))
            self.xs_fwb_lines = np.concatenate(np.stack(
                (self.fwhm_ch_ini, self.fwhm_ch_fin, np.full(n_pk, None)),
                axis=1))
            self.ys_fwb_lines = np.concatenate(np.stack(
                (self.plateaux, self.plateaux, np.full(n_pk, None)), axis=1))

    def define_multiplets_regions(self, is_reg, k_sep_pk):
        """Define multiplet regions from already found peaks with proper widths."""
        # k_sep_pk: Fator de fwhm para ampliar multipletos:
        # 2021-06-28
        # 2022-03-24 Vamos refatorar tudo:
        n_ch = is_reg.size
        widths_extd = k_sep_pk * self.propts['widths']
        ini_extd = np.round(self.peaks - widths_extd).astype(int)
        fin_extd = np.round(self.peaks + widths_extd).astype(int)
        if self.peaks.any():
            for i_pk, ch_pk in enumerate(self.peaks):
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

        print('define_multiplets_regions completado. Define:')
        print('self.mix_regions: ', self.mix_regions)
