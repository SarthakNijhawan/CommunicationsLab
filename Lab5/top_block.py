#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Sep  1 04:52:02 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")

        ##################################################
        # Variables
        ##################################################
        self.slider = slider = 0
        self.samp_rate = samp_rate = 2e6

        ##################################################
        # Blocks
        ##################################################
        _slider_sizer = wx.BoxSizer(wx.VERTICAL)
        self._slider_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_slider_sizer,
        	value=self.slider,
        	callback=self.set_slider,
        	label='slider',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._slider_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_slider_sizer,
        	value=self.slider,
        	callback=self.set_slider,
        	minimum=-100,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_slider_sizer)
        self.notebook = self.notebook = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook.AddPage(grc_wxgui.Panel(self.notebook), "modulated")
        self.notebook.AddPage(grc_wxgui.Panel(self.notebook), "FFT modulated")
        self.Add(self.notebook)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.notebook.GetPage(0).GetWin(),
        	title='Scope Plot',
        	sample_rate=samp_rate/16,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.notebook.GetPage(0).Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_f(
        	self.notebook.GetPage(1).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate/16,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.notebook.GetPage(1).Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(1155.002e6 , 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(60, 0)
        self.rtlsdr_source_0.set_if_gain(60, 0)
        self.rtlsdr_source_0.set_bb_gain(60, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_fff(16, firdes.low_pass(
        	1, samp_rate, 20e3, 4e3, firdes.WIN_HAMMING, 6.76))
        self.iir_filter_xxx_1_0 = filter.iir_filter_ffd(([1,]), ([1,0.95+0.1*slider]), True)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_arg_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))    
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_arg_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.iir_filter_xxx_1_0, 0))    
        self.connect((self.iir_filter_xxx_1_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))    

    def get_slider(self):
        return self.slider

    def set_slider(self, slider):
        self.slider = slider
        self._slider_slider.set_value(self.slider)
        self._slider_text_box.set_value(self.slider)
        self.iir_filter_xxx_1_0.set_taps(([1,]), ([1,0.95+0.1*self.slider]))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate/16)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate/16)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 20e3, 4e3, firdes.WIN_HAMMING, 6.76))


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
