#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 12:54:36 2021

@author: maduar
"""

import plotly.graph_objects as go


class SpecGraphics():
    def __init__(self, f_name, spec_an):
        pass
        # self.promns = spec_an.propts['prominences']
        # self.peaks = spec_an.peaks
        # self.pk_hei = spec_an.propts['peak_heights']


class GrossCountsGraphic(SpecGraphics):
    def __init__(self, f_name, spec_an):
        super().__init__(f_name, spec_an)
        self.f_name = f_name
        self.chans_nzero = spec_an.cnt_arrs.chans_nzero
        self.counts_nzero = spec_an.cnt_arrs.counts_nzero
        self.unc_y_4plot = spec_an.cnt_arrs.unc_y_4plot
        # self.x_s = spec_an.cnt_arrs.x_s
        # self.y_s = spec_an.cnt_arrs.y_s
        # Initialize figure
        self.figw1 = go.FigureWidget();

    def plot_figw1(self, spec_an, graph_name):

        # Add Traces

        self.figw1.add_trace(
            go.Scattergl(x=self.chans_nzero,
                         y=self.counts_nzero,
                         error_y=dict(
                             color='orange', width=3.0,
                             type='data',  # value of error bar given in data coordinates
                             array=self.unc_y_4plot,
                             visible=True),
                         name="Counts & uncertaintes",
                         line=dict(color='orange', width=0.7)));
        self.figw1.add_trace(
            go.Scattergl(x=spec_an.cnt_arrs.x_s,
                         y=spec_an.cnt_arrs.new_y_s,
                         name='y_s, eventually smoothed',
                         line=dict(color='navy', width=0.4)))

        # Set title and scale type
        self.figw1.update_layout(title_text='Fig 1: ' + self.f_name)
        self.figw1.update_yaxes(type="log")
        self.figw1.write_html(graph_name + '.html', auto_open=True)


class PeaksAndRegionsGraphic(SpecGraphics):
    def __init__(self, f_name, spec_an):
        super().__init__(f_name, spec_an)
        self.f_name = f_name
        self.chans_nzero = spec_an.cnt_arrs.chans_nzero
        self.counts_nzero = spec_an.cnt_arrs.counts_nzero
        self.unc_y_4plot = spec_an.cnt_arrs.unc_y_4plot
        self.x_s = spec_an.cnt_arrs.x_s
        # Initialize figure
        self.pk_parms = spec_an.pk_parms
        self.propts = self.pk_parms.propts
        self.fig_widths = go.FigureWidget();

    def define_width_lines(self):
        """Build width peaks related lines, just for plotting."""
        n_pk = self.pk_parms.size
        if n_pk != 0:
            self.xs_fwhm_lines = np.concatenate(np.stack(
                (self.propts['left_ips'], self.propts['right_ips'],
                 np.full(n_pk, None)), axis=1))
            self.ys_fwhm_lines = np.concatenate(np.stack(
                (self.propts['width_heights'],
                 self.propts['width_heights'],
                 np.full(n_pk, None)), axis=1))
            self.xs_fwb_lines = np.concatenate(np.stack(
                (self.fwhm_ch_ini, self.fwhm_ch_fin, np.full(n_pk, None)),
                axis=1))
            self.ys_fwb_lines = np.concatenate(np.stack(
                (self.plateaux, self.plateaux, np.full(n_pk, None)), axis=1))


    def plot_figw2(self, spec_an, graph_name):

        self.fig_widths.add_trace(
            go.Scattergl(x=self.chans_nzero,
                         y=self.counts_nzero,
                         error_y=dict(
                             color='orange', width=3.0,
                             type='data',  # value of error bar given in data coordinates
                             array=self.unc_y_4plot,
                             visible=True),
                         name="Counts & uncertaintes",
                         line=dict(color='orange', width=0.7)));

        self.fig_widths.add_trace(
            go.Scattergl(x=self.pk_parms.xs_fwhm_lines,
                         y=self.pk_parms.ys_fwhm_lines,
                         name='FWHMs',
                         line=dict(color='blue', width=3.0)));
        self.fig_widths.add_trace(
            go.Scattergl(x=self.pk_parms.xs_fwb_lines,
                         y=self.pk_parms.ys_fwb_lines,
                         name='FW at base',
                         line=dict(color='magenta', width=3.0)));
        self.fig_widths.add_trace(
            go.Scattergl(x=self.pk_parms.peaks,
                         y=self.pk_parms.propts['peak_heights'],
                         name = 'peak_heights',
                         marker = dict(color='yellow',
                                       symbol='circle',
                                       size=10,
                                       opacity=0.8,
                                       line=dict(color='green', width=2.0)
                                       ),
                         mode = 'markers'));
        # Set title and scale type
        self.fig_widths.update_layout(title_text="Fig 2: Peaks widths")
        self.fig_widths.update_yaxes(type='log');
        self.fig_widths.write_html(graph_name + '.html', auto_open=True)

    def united_step_baselines(self):
        """Build concatenated arrays of step baselines, just for plotting."""
        self.plotsteps_x = np.concatenate([np.append(i, None) for i in self.chans_in_multiplets_list])
        self.plotsteps_y = np.concatenate([np.append(i, None) for i in self.calculated_step_counts])

