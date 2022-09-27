# Created on Fri Nov  5 12:00:42 2021

# @author: mmaduar
import numpy as np

from src.genericcalib_class import ChannelEnergyCalib, EnergyFwhmCalib, EnergyEfficiencyCalib
from src.specchn_class import SpecChn
from src.speciec_class import SpecIec
from src.cntarraylike_class import CntArrayLike
# from src.peaksparms_class import PeaksParms
from src.generic_series_analysis_class import GenericSeriesAnalysis

class SpecParms:
    """Given spectrum parameters (count time, sample description etc)."""

    def __init__(self, f_name, sufx):
        self.sufx = sufx
        if self.sufx == '.chn':
            self.spec_io = SpecChn(f_name)
        elif self.sufx == '.iec':
            self.spec_io = SpecIec(f_name)

        #
        n_ch = self.spec_io.n_ch

        self.cnt_array_like = CntArrayLike(self.spec_io.sp_counts)

        # self.peaks_parms = PeaksParms()
        self.ser_an = GenericSeriesAnalysis()

        #        self.channel_energy_calib = ChannelEnergyCalib(self.spec_io.en_ch_calib,
        #                                                       self.spec_io.chan_calib,
        #                                                       self.spec_io.coeffs_ch_en)
        self.channel_energy_calib = ChannelEnergyCalib(self.spec_io.coeffs_ch_en)
        #       self.energy_fwhm_calib = EnergyFwhmCalib(self.spec_io.en_fw_calib,
        #                                                self.spec_io.fwhm_calib,
        #                                                self.spec_io.coeffs_en_fw)
        self.energy_fwhm_calib = EnergyFwhmCalib(self.spec_io.coeffs_en_fw)
        #        self.energy_efficiency_calib = EnergyEfficiencyCalib(self.spec_io.en_ef_calib,
        #                                                            self.spec_io.effi_calib)

        #        self.channel_energy_calib = ChannelEnergyCalib()
        #        self.energy_fwhm_calib = EnergyFwhmCalib()
        try:  # 2022-Jun-23
            self.spec_io.en_ef_calib
        except AttributeError:
            pass
        else:
            self.energy_efficiency_calib = EnergyEfficiencyCalib(self.spec_io.en_ef_calib)

    #    def total_analysis(self, smoo, widths_range, k_sep_pk=5.0):
    def spe_analysis(self, k_sep_pk, smoo, widths_ranges):
        """
        Initialize a minimal members set from a read spectrum file.

        :param k_sep_pk: Spectrum's complete file name.
        :type f_name: str
        # :raise lumache.InvalidKindError: If the kind is invalid.
        :return: 0 if spectrum was successfully opened; -1 otherwise.
        :rtype: int

        # sequência:
        #    incia obj spec_parms
        #    initial_peaks_search: acha picos candidatos, põe em peaks_parms.peaks
        #    define_multiplets_regions:
        #       em init do cnt_array_like, define eval_smoo_cts
        #       em define_multiplets_regions: define is_reg com base em bons picos
        #    em define_multiplets_limits: define mix_regions (lims reg)
        #    calculate_base_line
        #    calculate_net_spec
        #
        #
        #
        #
        """
        #        dá pobrema fazer em eval_smoo_cts
        #        self.peaks_parms.initial_peaks_search(self.cnt_array_like.n_ch,
        #                                              self.cnt_array_like.eval_smoo_cts)

        if self.cnt_array_like.n_ch > 0:
            print('k_sep_pk: ', k_sep_pk)
            print('smoo: ', smoo)
            print('widths_ranges: ', widths_ranges)
            print('=================')
            print('Exec peaks_search(gross=True)')
            self.peaks_parms.peaks_search(cts_to_search=self.cnt_array_like.y0s, gross=True)
            # print("self.peaks_parms.peaks_gro: ", self.peaks_parms.peaks_gro)
            # print("self.peaks_parms.propts_gro['widths']: ", self.peaks_parms.propts_gro['widths'])
            # print("self.peaks_parms.gross_widths = (ws_min, ws_max): ", self.peaks_parms.gross_widths)
            print('=================')
            print('Exec redefine_widths_range(self.gross_widths)')
            self.peaks_parms.redefine_widths_range(self.peaks_parms.gross_widths, gross=True)
            print('=================')
            print('Exec peaks_search(gross=True)')
            self.peaks_parms.peaks_search(cts_to_search=self.cnt_array_like.y0s, gross=True,
                                          widths_range=self.peaks_parms.gross_widths)
            # print("self.peaks_parms.peaks_gro: ", self.peaks_parms.peaks_gro)
            # print("self.peaks_parms.propts_gro: ", self.peaks_parms.propts_gro)
            # print("self.peaks_parms.gross_widths = (ws_min, ws_max): ", self.peaks_parms.gross_widths)
            print('=================')
            self.peaks_parms.define_width_lines(gross=True)

            print(self.cnt_array_like.is_gro_reg)
            print(self.cnt_array_like.is_gro_reg.size)

            self.peaks_parms.define_multiplets_regions(self.cnt_array_like.is_gro_reg,
                                                       k_sep_pk=k_sep_pk)
            self.cnt_array_like.calculate_base_line(self.peaks_parms.mix_regions, smoo)

            print('self.cnt_array_like.calculated_step_counts:')
            # for i in self.cnt_array_like.calculated_step_counts:
            #     print(i)
            # print (len(self.cnt_array_like.calculated_step_counts))

            print('self.cnt_array_like.chans_in_multiplets_list:')
            # for i in self.cnt_array_like.chans_in_multiplets_list:
            #     print(i)
            # print (len(self.cnt_array_like.chans_in_multiplets_list))

            self.cnt_array_like.united_step_baselines()
            print('united:')
            # print(self.cnt_array_like.plotsteps_x)
            # print(self.cnt_array_like.plotsteps_y)

            # 2022-set-27 Aqui começam os cálculos em cima do espectro líquido
            print('=================')
            print('Exec peaks_search(gross=False)')
            self.peaks_parms.peaks_search(cts_to_search=self.cnt_array_like.net_spec, gross=False,
                                          widths_range=self.peaks_parms.net_widths)
            print("self.peaks_parms.peaks_net: ", self.peaks_parms.peaks_net)
            print("self.peaks_parms.propts_net: ", self.peaks_parms.propts_net)
            print("self.peaks_parms.net_widths = (ws_min, ws_max): ", self.peaks_parms.net_widths)

            print('=================')
            self.peaks_parms.define_width_lines(gross=False)

            print(self.cnt_array_like.is_net_reg)
            print(self.cnt_array_like.is_net_reg.size)

            self.peaks_parms.define_net_multiplets_regions(self.cnt_array_like.is_net_reg,
                                                           k_sep_pk=k_sep_pk)

            print('=================')
            self.peaks_parms.define_width_lines(gross=False)
            self.peaks_parms.net_width_lines()
            self.peaks_parms.define_net_multiplets_regions(self.cnt_array_like.is_net_reg,
                                                           k_sep_pk=k_sep_pk)
        else:
            print('No analysis applicable as spectrum is empty.')
        # print(vars(self.peaks_parms))

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
