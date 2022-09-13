#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 12:54:36 2021

@author: maduar
"""

import plotly.graph_objects as go


class SpecGraphics:
    def __init__(self, spec_parms, graph_nos):
        chans_nzero = spec_parms.cnt_array_like.chans_nzero
        chans_nzero = spec_parms.cnt_array_like.chans_nzero
        counts_nzero = spec_parms.cnt_array_like.counts_nzero
        unc_y_4plot = spec_parms.cnt_array_like.unc_y_4plot
        chans = spec_parms.cnt_array_like.chans
        xs_bl_out_reg = spec_parms.cnt_array_like.xs_bl_out_reg
        ys_bl_out_reg = spec_parms.cnt_array_like.ys_bl_out_reg
        eval_smoo_cts = spec_parms.cnt_array_like.eval_smoo_cts

    def plot_simple_scattergl(self, chans_nzero=None, counts_nzero=None, unc_y=None, f_name=None):
        # Initialize figure
        figw1 = go.FigureWidget();

        # Add Traces

        figw1.add_trace(
            go.Scattergl(x=chans_nzero,
                         y=counts_nzero,
                         error_y=dict(
                             color='orange', width=3.0,
                             type='data',  # value of error bar given in data coordinates
                             array=unc_y,
                             visible=True),
                         name="Counts & uncertaintes",
                         line=dict(color='orange', width=0.7)));

        # Set title and scale type
        figw1.update_layout(title_text='Fig 1: ' + f_name)
        figw1.update_yaxes(type="log");

        figw1.write_html('figw1.html', auto_open=True)

# Melhor não abrir inline, que seria simplesmente entrar com o nome do objeto:
# figw2
# Além de ficar com visualização incômoda, não funciona no JupyterLab; dá o erro:
# Error displaying widget: model not found.
