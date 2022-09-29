import numpy as np
from scipy.interpolate import splrep, splev


class CountsSeriesArrays:
    def __init__(self, sp_counts, to_smooth):
        self.y_s = np.array(sp_counts)
        self.nzero = self.y_s > 0
        self.n_ch = self.y_s.size
        self.x_s = np.linspace(0, self.n_ch - 1, self.n_ch)
        self.chans_nzero = self.x_s[self.y_s > 0]
        # Talvez melhor deixar 0.0 em vez de 0.9
        self.counts_nzero = self.y_s[self.nzero]
        self.unc_y = np.sqrt(self.counts_nzero)
        if to_smooth:
            # self.new_y_s = np.array(self.y_s)
            self.new_y_s = self.eval_smoo_counts()
        else:
            self.new_y_s = np.array(self.y_s)
        self.unc_y_4plot = np.where(self.unc_y < 1.4, 0.0, self.unc_y)

        self.plotsteps_x = []
        self.plotsteps_y = []

        self.xs_bl_out_reg = np.array([])
        self.ys_bl_out_reg = np.array([])
        self.ws_bl_out_reg = np.array([])

        self.is_reg = np.zeros(self.n_ch, dtype=bool)

    def eval_smoo_counts(self):
        if self.n_ch > 0:
            smoo_cts = splrep(x=self.chans_nzero,
                              y=self.counts_nzero,
                              w=1.0 / self.unc_y, k=3)
            evaluated = splev(self.x_s, smoo_cts)
            return evaluated

    def calculate_base_line(self, mix_regions, smoo):
        """Calculate baseline."""
        x_1 = self.chans_outof_regs()
        _first_nz = np.nonzero(self.y0s)[0][0]
        _init_fill = np.mean(self.y0s[_first_nz:_first_nz + 7]).astype(int)
        _y = self.counts_outof_regs()
        _y[0:_first_nz] = _init_fill
        _raiz_y = np.sqrt(_y)
        _raiz_y[_raiz_y < 2] = 1.0
        _w = 1.0 / _raiz_y
        # _w = _raiz_y
        self.spl_baseline = splrep(x=x_1, y=_y, w=_w, k=3, s=smoo)
        # self.eval_baseline = splev(x_1, self.spl_baseline)
        self.eval_baseline = splev(self.chans, self.spl_baseline)
        self.xs_bl_out_reg = x_1
        # print(x_1)
        self.ys_bl_out_reg = _y
        # print(_y)
        self.ws_bl_out_reg = _w

        self.xs_bl_in_reg = self.chans_in_regs()
        self.ys_bl_in_reg = self.counts_in_regs()
        for multiplet_region in mix_regions:
            _xs = self.chans[slice(*multiplet_region)]
            _ys = self.y0s[slice(*multiplet_region)]
            _bl_in = splev(multiplet_region[0] - 1, self.spl_baseline)
            _bl_fi = splev(multiplet_region[1], self.spl_baseline)
            _a_step = self.step_baseline(_bl_in, _bl_fi, _ys)
            self.chans_in_multiplets_list.append(_xs)
            self.calculated_step_counts.append(_a_step)
            # print('multiplet_region: ', multiplet_region)
            # print('chans: ', _chans)
            # print('_ys: ', _ys)
            # print('_bl_in: ', _bl_in)
            # print('_bl_fi: ', _bl_fi)
            # print('a_step: ', _a_step)
            # print('============================')
            net_mplet = _ys - _a_step
            #    self.xs_all_mplets.extend(list(xs_mplet))
            #    self.xs_all_mplets.append( None )
            #    self.ys_all_mplets.extend(list(net_mplet))
            #    self.ys_all_mplets.append( None )
            #    self.ys_all_steps.extend(list(a_step))
            #    self.ys_all_steps.append( None )
            self.net_spec[slice(*multiplet_region)] = np.where(net_mplet < 0.0, 0.0, net_mplet)
            self.final_baseline = self.y0s - self.net_spec

    def step_baseline(self, bl_in, bl_fi, y_s):
        """Calculate step baseline inside a region. Called just by calculate_base_line."""
        contin = np.zeros(y_s.size)
        gross_area = np.sum(y_s) + bl_fi
        delta_y = bl_fi - bl_in
        delta_x = y_s.size
        for i in range(delta_x):
            sum_y = np.sum(y_s[0:i + 1])
            contin[i] = bl_in + delta_y * sum_y / gross_area
        return contin
