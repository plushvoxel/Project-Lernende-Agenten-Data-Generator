#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fm Noisy Frequency
# Generated: Wed Oct 17 13:57:06 2018
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt


class fm_noisy_frequency(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Fm Noisy Frequency")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2048

        ##################################################
        # Blocks
        ##################################################
        self.fft_vxx_0 = fft.fft_vcc(samp_rate, True, (window.blackmanharris(samp_rate)), True, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, samp_rate)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_rate)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/dev/stdin', True)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/dev/stdout', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=75e-6,
        	max_dev=samp_rate/2,
        	fh=-1.0,
        )
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.01, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_wfm_tx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=fm_noisy_frequency, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
