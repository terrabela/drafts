#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 12:54:36 2021

@author: maduar
"""

import plotly.graph_objects as go


class SpecGraphics():
    def __init__(self, spec_parms):
        self.parms = spec_parms

        # self.promns = spec_parms.peaks_parms.propts_gro['prominences']
        # self.peaks_net = spec_parms.peaks_parms.peaks_net
        # self.pk_hei_net = spec_parms.peaks_parms.propts_net['peak_heights']

    def plot_figw1(self):
        # Initialize figure
        self.figw1 = go.FigureWidget();

        # Add Traces

        self.figw1.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.chans_nzero,
                         y=self.parms.cnt_array_like.counts_nzero,
                         error_y=dict(
                             color='orange', width=3.0,
                             type='data',  # value of error bar given in data coordinates
                             array=self.parms.cnt_array_like.unc_y_4plot,
                             visible=True),
                         name="Counts & uncertaintes",
                         line=dict(color='orange', width=0.7)));

        # Set title and scale type
        # self.figw1.update_layout(title_text='Fig 1: ')  # + f_name)
        # self.figw1.update_yaxes(type="log");

        # AQUI: não precisa abrir página web nova.
        # self.figw1.write_html('figw1.html', auto_open=True)

    def plot_figw2(self):

        # graphic #2
        self.fig_widths = go.FigureWidget(self.figw1);

        self.fig_widths.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.chans,
                         y=self.parms.cnt_array_like.eval_smoo_cts,
                         name='Smoothed',
                         line=dict(color='navy', width=0.4)))

        self.fig_widths.add_trace(
            go.Scattergl(x=self.parms.peaks_parms.xs_fwhm_lines,
                         y=self.parms.peaks_parms.ys_fwhm_lines,
                         name='FWHMs',
                         line=dict(color='blue', width=3.0)));
        self.fig_widths.add_trace(
            go.Scattergl(x=self.parms.peaks_parms.xs_fwb_lines,
                         y=self.parms.peaks_parms.ys_fwb_lines,
                         name='FW at base',
                         line=dict(color='magenta', width=3.0)));
        self.fig_widths.add_trace(
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
        self.fig_widths.update_layout(title_text="Fig 2: Peaks widths")
        self.fig_widths.update_yaxes(type='log');
        self.fig_widths.write_html('fig_widths.html', auto_open=True)

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
