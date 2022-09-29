def chunks_from_file(self, chunksize=8192):
    """ Read file chunks. """
    file_chunks = []
    with open(self, "rb") as f_file:
        while True:
            chunk = f_file.read(chunksize)
            if chunk:
                yield chunk
                file_chunks.append(chunk)
            else:
                break
    return file_chunks



    def plot_figw2(self):

    def plot_figw3(self):
        # graphic #3

        self.fig_is_reg = go.FigureWidget(self.figw1);

        self.fig_is_reg.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.chans_in_regs(),
                         y=self.parms.cnt_array_like.counts_in_regs(),
                         name='Counts in regions',
                         mode='markers',
                         marker=dict(
                             color='LightSkyBlue',
                             size=6,
                             line=dict(color='MediumPurple', width=3)
                         )));
        self.fig_is_reg.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.chans_outof_regs(),
                         y=self.parms.cnt_array_like.counts_outof_regs(),
                         name='Counts out of regions',
                         mode='markers',
                         marker=dict(
                             color='Pink',
                             size=5,
                             line=dict(color='LightGreen', width=2)
                         )));

        # Set title and scale type
        self.fig_is_reg.update_layout(title_text="Fig 3: Definition of regions")
        self.fig_is_reg.update_yaxes(type='log');
        self.fig_is_reg.write_html('fig_is_reg.html', auto_open=True)

    def plot_figw4(self):
        # Initialize another figure
        self.figw4 = go.FigureWidget(self.figw1);

        # Add Traces

        self.figw4.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.chans,
                         y=self.parms.cnt_array_like.final_baseline,
                         name='final_baseline',
                         line=dict(color='gray', width=0.3)));

        self.figw4.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.plotsteps_x,
                         y=self.parms.cnt_array_like.plotsteps_y,
                         name='calculated_step_counts',
                         line=dict(color='red', width=1.3)));

        self.figw4.add_trace(
            go.Scattergl(x=self.parms.peaks_parms.peaks_gro,
                         y=self.parms.peaks_parms.propts_gro['peak_heights'],
                         name = 'peak_heights',
                         marker = dict(color='yellow',
                                       symbol='circle',
                                       size=10,
                                       opacity=0.8,
                                       line=dict(color='green', width=2.0)
                                       ),
                         mode = 'markers'));
        # Set title and scale type
        self.figw4.update_layout(title_text='Fig 4: Base line')
        self.figw4.update_yaxes(type='log');
        self.figw4.write_html('figw4.html', auto_open=True)

    def plot_figw5(self):

        # graphic #5

        self.fig_steps = go.FigureWidget();
        self.fig_steps.add_trace(
            go.Scattergl(x=self.chans[self.nzero & self.is_reg],
                         y=self.counts[self.nzero & self.is_reg],
                         name='Counts in regions',
                         line=dict(color='navy', width=0.3),
                         mode='markers'));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.chans[self.nzero & ~self.is_reg],
                         y=self.counts[self.nzero & ~self.is_reg],
                         name='Counts out of regions',
                         line=dict(color='orange', width=0.3),
                         mode='markers'));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.xs_all_mplets,
                         y=self.ys_all_steps,
                         name='ys_all_steps',
                         line=dict(color='brown', width=1.5)));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.xs_all_mplets,
                         y=self.ys_all_mplets,
                         name='ys_all_mplets',
                         line=dict(color='green', width=3.0)));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.chans,
                         y=self.final_baseline,
                         name='final_baseline',
                         line=dict(color='magenta', width=0.7)));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.peaks_gro,
                         y=self.pk_hei_gro,
                         name='peak_heights',
                         marker=dict(color='yellow',
                                     symbol='circle',
                                     size=10,
                                     opacity=0.8,
                                     line=dict(color='magenta', width=2.0)
                                     ),
                         mode='markers',
                         line=dict(color='green', width=3.0)));
        # Set title and scale type
        self.fig_steps.update_layout(title_text='Fig 5: fig_steps')
        self.fig_steps.update_yaxes(type='log');
        self.fig_steps.write_html('fig_steps.html', auto_open=True)

    def plot_figw6(self):

    # graphic #6

        self.figw6 = go.FigureWidget();

        self.figw6.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.chans,
                         y=self.parms.cnt_array_like.net_spec,
                         name='net_spec',
                         line=dict(color='magenta', width=0.7)));

        self.figw6.add_trace(
            go.Scattergl(x=self.parms.peaks_parms.peaks_net,
                         y=self.parms.peaks_parms.propts_net['peak_heights'],
                         name='peak_heights',
                         marker=dict(color='orange',
                                     symbol='circle',
                                     size=10,
                                     opacity=0.8,
                                     line=dict(color='blue', width=2.0)
                                     ),
                         mode='markers'));
        # Set title and scale type
        self.figw6.update_layout(title_text='Fig 6: net spec analysis')
        # self.figw6.update_yaxes(type='log');
        self.figw6.write_html('figw6.html', auto_open=True)

    def plot_simple_scattergl(self, chans_nzero=None, counts_nzero=None, unc_y=None, f_name=None):

        self.plot_figw1() # estarah contido em figw2 e figw4
        # self.plot_figw2()
        # self.plot_figw3()
        self.plot_figw4()
        # self.plot_figw5()
        self.plot_figw6()

    def correct_spec_begin(
            self, ct_arr, thresh_first_max=3.0, thresh_stable_var=1.0, ch_win=10):
        n_ct = ct_arr.size
        var_rel = np.array(
            [np.var(ct_arr[i:i + ch_win]) / (abs(np.mean(ct_arr[i:i + ch_win])) + 1)
             for i in range(n_ct - ch_win)]
        )
        loc_step = np.where(var_rel > thresh_first_max)[0][0]
        remaining_arr = var_rel[loc_step:]
        loc_stable_cts = np.where(remaining_arr < thresh_stable_var)[0][0] + loc_step
        return var_rel, loc_stable_cts
        # loc_stable_cts


# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:29:28 2021

@author: mmaduar
"""
# , splder, sproot

class CntArrayLike:
    """ Counts array alike vars class. """


    def __init__(self, sp_counts):
        self.y0s = np.asarray(sp_counts)
        self.n_ch = len(sp_counts)
        self.x_s = np.linspace(0, self.n_ch - 1, self.n_ch)
        # self.terms_2nd_grade = np.zeros(self.n_ch)
        # self.terms_1st_grade = np.zeros(self.n_ch)
        # self.terms_0th_grade = np.zeros(self.n_ch)
        self.varnc_2nd_grade = np.zeros(self.n_ch)

        self.nzero = self.y0s > 0
        self.chans = self.x_s
        self.chans_nzero = self.x_s[self.y0s > 0]
        # Talvez melhor deixar 0.0 em vez de 0.9
        self.counts_nzero = self.y0s[self.nzero]
        self.unc_y = np.sqrt(self.counts_nzero)

        self.unc_y_4plot = np.where(self.unc_y < 1.4, 0.0, self.unc_y)

        self.plotsteps_x = []
        self.plotsteps_y = []

        self.xs_bl_out_reg = np.array([])
        self.ys_bl_out_reg = np.array([])
        self.ws_bl_out_reg = np.array([])

        self.is_gro_reg = np.zeros(self.n_ch, dtype=bool)
        self.is_net_reg = np.zeros(self.n_ch, dtype=bool)





        self.net_spec = np.zeros(self.n_ch)
        self.final_baseline = np.zeros(self.n_ch)
        self.xs_all_mplets = []
        self.ys_all_mplets = []
        self.ys_all_steps = []

        self.chans_in_multiplets_list = []
        self.calculated_step_counts = []

    def chans_in_regs(self):
        """ Channels in regions. """
        return self.chans[self.is_reg]

    def counts_in_regs(self):
        """ Counts in regions. """
        return self.y0s[self.is_reg]

    def chans_outof_regs(self):
        """ Channels out of regions. """
        return self.chans[~self.is_reg]

    def counts_outof_regs(self):
        """  Counts out of regions. """
        return self.y0s[~self.is_reg]


