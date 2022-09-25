#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 12:54:36 2021

@author: maduar
"""

import plotly.graph_objects as go


class SpecGraphics:
    def __init__(self, spec_parms):
        self.chans_nzero = spec_parms.cnt_array_like.chans_nzero
        self.counts_nzero = spec_parms.cnt_array_like.counts_nzero
        self.unc_y_4plot = spec_parms.cnt_array_like.unc_y_4plot
        self.chans = spec_parms.cnt_array_like.chans
        self.counts = spec_parms.cnt_array_like.y0s
        self.nzero = spec_parms.cnt_array_like.nzero
        self.xs_bl_out_reg = spec_parms.cnt_array_like.xs_bl_out_reg
        self.ys_bl_out_reg = spec_parms.cnt_array_like.ys_bl_out_reg
        self.eval_smoo_cts = spec_parms.cnt_array_like.eval_smoo_cts
        self.net_spec = spec_parms.cnt_array_like.net_spec
        self.is_reg = spec_parms.cnt_array_like.is_reg
        self.xs_all_mplets = spec_parms.cnt_array_like.xs_all_mplets
        self.ys_all_mplets = spec_parms.cnt_array_like.ys_all_mplets
        self.ys_all_steps = spec_parms.cnt_array_like.ys_all_steps
        self.final_baseline = spec_parms.cnt_array_like.final_baseline
        self.chans_in_regs = spec_parms.cnt_array_like.chans_in_regs
        self.counts_in_regs = spec_parms.cnt_array_like.counts_in_regs
        self.chans_outof_regs = spec_parms.cnt_array_like.chans_outof_regs
        self.counts_outof_regs = spec_parms.cnt_array_like.counts_outof_regs

        self.xs_fwb_lines = spec_parms.peaks_parms.xs_fwb_lines
        self.ys_fwb_lines = spec_parms.peaks_parms.ys_fwb_lines

        self.peaks_gro = spec_parms.peaks_parms.peaks_gro
        self.pk_hei_gro = spec_parms.peaks_parms.pk_hei_gro
        self.promns = spec_parms.peaks_parms.propts_gro['prominences']
        self.peaks_net = spec_parms.peaks_parms.peaks_net
        self.pk_hei_net = spec_parms.peaks_parms.propts_net['peak_heights']

        self.xs_fwhm_lines = spec_parms.peaks_parms.xs_fwhm_lines
        self.ys_fwhm_lines = spec_parms.peaks_parms.ys_fwhm_lines

    def plot_figw1(self):
        # Initialize figure
        self.figw1 = go.FigureWidget();

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
            go.Scattergl(x=self.chans,
                         y=self.eval_smoo_cts,
                         name='Smoothed',
                         line=dict(color='navy', width=0.4)))

        # Set title and scale type
        # self.figw1.update_layout(title_text='Fig 1: ')  # + f_name)
        # self.figw1.update_yaxes(type="log");

        # AQUI: não precisa abrir página web nova.
        # self.figw1.write_html('figw1.html', auto_open=True)

    def plot_figw2(self):

        # graphic #2

        self.fig_widths = go.FigureWidget(self.figw1);

        self.fig_widths.add_trace(
            go.Scatter(x=self.xs_fwhm_lines,
                       y=self.ys_fwhm_lines,
                       name='FWHMs',
                       line=dict(color='blue', width=3.0)));
        self.fig_widths.add_trace(
            go.Scatter(x=self.xs_fwb_lines,
                       y=self.ys_fwb_lines,
                       name='FW at base',
                       line=dict(color='magenta', width=3.0)));
        self.fig_widths.add_trace(
            go.Scatter(x=self.peaks_gro,
                       y=self.pk_hei_gro,
                       name='peak_heights',
                       mode='markers',
                       line=dict(color='green', width=3.0)));

        # 2022-09-16
        # AQUI estou fazendo grande confusão com pk_hei, pk_gro, promns...
        # Organizar essa puta zona.
        # fig_widths.add_trace(
        #     go.Scatter(x=self.peaks_gro,
        #                y=self.pk_hei_gro - self.promns,
        #                name='pk_hei-promns',
        #                mode='markers',
        #                line=dict(color='cyan', width=3.0)));
        # Set title and scale type
        # self.fig_widths.update_layout(title_text="Fig 2: Peaks widths")
        # self.fig_widths.update_yaxes(type='log');
        # self.fig_widths.write_html('fig_widths.html', auto_open=True)

    def plot_figw3(self):
        # graphic #3

        self.fig_is_reg = go.FigureWidget(self.fig_widths);

        self.fig_is_reg.add_trace(
            go.Scatter(x=self.chans_in_regs(),
                       y=self.counts_in_regs(),
                       name='Counts in regions',
                       mode='markers',
                       marker=dict(
                           color='LightSkyBlue',
                           size=6,
                           line=dict(color='MediumPurple', width=3)
                       )));
        self.fig_is_reg.add_trace(
            go.Scatter(x=self.chans_outof_regs(),
                       y=self.counts_outof_regs(),
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
        self.figw4 = go.FigureWidget();

        # Add Traces

        self.figw4.add_trace(
            go.Scatter(x=self.chans_nzero,
                       y=self.counts_nzero,
                       error_y=dict(
                           color='orange', width=3.0,
                           type='data',  # value of error bar given in data coordinates
                           array=self.unc_y_4plot,
                           visible=True),
                       name='Counts & uncertaintes',
                       line=dict(color='orange', width=0.3)));
        self.figw4.add_trace(
            go.Scatter(x=self.xs_bl_out_reg,
                       y=self.ys_bl_out_reg,
                       name='eval_baseline',
                       line=dict(color='red', width=0.5)));
        self.figw4.add_trace(
            go.Scatter(x=self.peaks_gro,
                       y=self.pk_hei_gro,
                       name='peak_heights',
                       mode='markers',
                       line=dict(color='green', width=3.0)));

        # Set title and scale type
        self.figw4.update_layout(title_text='Fig 4: Base line')
        self.figw4.update_yaxes(type='log');
        self.figw4.write_html('figw4.html', auto_open=True)

    def plot_figw5(self):

        # graphic #5

        self.fig_steps = go.FigureWidget();
        self.fig_steps.add_trace(
            go.Scatter(x=self.chans[self.nzero & self.is_reg],
                       y=self.counts[self.nzero & self.is_reg],
                       name='Counts in regions',
                       line=dict(color='navy', width=0.3),
                       mode='markers'));
        self.fig_steps.add_trace(
            go.Scatter(x=self.chans[self.nzero & ~self.is_reg],
                       y=self.counts[self.nzero & ~self.is_reg],
                       name='Counts out of regions',
                       line=dict(color='orange', width=0.3),
                       mode='markers'));
        self.fig_steps.add_trace(
            go.Scatter(x=self.xs_all_mplets,
                       y=self.ys_all_steps,
                       name='ys_all_steps',
                       line=dict(color='brown', width=1.5)));
        self.fig_steps.add_trace(
            go.Scatter(x=self.xs_all_mplets,
                       y=self.ys_all_mplets,
                       name='ys_all_mplets',
                       line=dict(color='green', width=3.0)));
        self.fig_steps.add_trace(
            go.Scatter(x=self.chans,
                       y=self.final_baseline,
                       name='final_baseline',
                       line=dict(color='magenta', width=0.7)));
        self.fig_steps.add_trace(
            go.Scatter(x=self.peaks_gro,
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
            go.Scatter(x=self.chans,
                       y=self.net_spec,
                       name='net_spec',
                       line=dict(color='magenta', width=0.7)));

        self.figw6.add_trace(
               go.Scatter(x=self.peaks_net,
                          y=self.pk_hei_net,
                          name='pk_hei_net',
                          marker=dict(color='yellow',
                                      symbol='circle',
                                      size=10,
                                      opacity=0.8,
                                      line=dict(color='magenta', width=2.0)
                                     ),
                          mode='markers',
                          line=dict(color='green',width=3.0)));

        # Set title and scale type
        self.figw6.update_layout(title_text='Fig 6: net spec analysis')
        self.figw6.update_yaxes(type='log');
        self.figw6.write_html('figw6.html', auto_open=True)

    def plot_simple_scattergl(self, chans_nzero=None, counts_nzero=None, unc_y=None, f_name=None):

        self.plot_figw1() # jah estah contida na figw2
        self.plot_figw2() # jah estah contida na figw3
        self.plot_figw3()
        self.plot_figw4()
        # self.plot_figw5()
        # self.plot_figw6()
