#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NOAA Weather Radio
# Author: Brian McLaughlin
# Description: Tune to one of the 7 US NOAA weather stations.
# Generated: Wed Jan 20 15:29:07 2016
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

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import osmosdr
import sip
import sys
import time


class noaa_weather(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NOAA Weather Radio")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NOAA Weather Radio")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "noaa_weather")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.valid_gains = valid_gains = [0.0, 0.9, 1.4, 2.7, 3.7, 7.7, 8.7, 12.5, 14.4, 15.7, 16.6, 19.7, 20.7, 22.9, 25.4, 28.0, 29.7, 32.8, 33.8, 36.4, 37.2, 38.6, 40.2, 42.1, 43.4, 43.9, 44.5, 48.0, 49.6]
        self.noaa_stations = noaa_stations = [(162.400e6,'WX2') , (162.425e6, 'WX4'), (162.450e6, 'WX5'), (162.475e6,'WX3'), (162.500e6, 'WX6'), (162.525e6, 'WX7'), (162.550e6, 'WX1')]
        self.samp_rate = samp_rate = 250e3
        self.range_ppm_corr = range_ppm_corr = 9
        self.noaa_stations_labels = noaa_stations_labels = ['{:>7.3f} MHz (Channel {:3})'.format(f[0]/1e6, f[1]) for f in noaa_stations]
        self.chooser_gain = chooser_gain = valid_gains[-1]
        self.chooser_frequency = chooser_frequency = noaa_stations[0][0]

        ##################################################
        # Blocks
        ##################################################
        self.notebook_top = Qt.QTabWidget()
        self.notebook_top_widget_0 = Qt.QWidget()
        self.notebook_top_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_top_widget_0)
        self.notebook_top_grid_layout_0 = Qt.QGridLayout()
        self.notebook_top_layout_0.addLayout(self.notebook_top_grid_layout_0)
        self.notebook_top.addTab(self.notebook_top_widget_0, "RF")
        self.notebook_top_widget_1 = Qt.QWidget()
        self.notebook_top_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_top_widget_1)
        self.notebook_top_grid_layout_1 = Qt.QGridLayout()
        self.notebook_top_layout_1.addLayout(self.notebook_top_grid_layout_1)
        self.notebook_top.addTab(self.notebook_top_widget_1, "Audio")
        self.top_grid_layout.addWidget(self.notebook_top, 2, 0, 1, 2)
        self._range_ppm_corr_range = Range(-50, 50, 1, 9, 200)
        self._range_ppm_corr_win = RangeWidget(self._range_ppm_corr_range, self.set_range_ppm_corr, "PPM Correction", "counter_slider", int)
        self.notebook_top_grid_layout_0.addWidget(self._range_ppm_corr_win, 0, 1, 1, 1)
        self.notebook_rf = Qt.QTabWidget()
        self.notebook_rf_widget_0 = Qt.QWidget()
        self.notebook_rf_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_rf_widget_0)
        self.notebook_rf_grid_layout_0 = Qt.QGridLayout()
        self.notebook_rf_layout_0.addLayout(self.notebook_rf_grid_layout_0)
        self.notebook_rf.addTab(self.notebook_rf_widget_0, "Spectrum")
        self.notebook_rf_widget_1 = Qt.QWidget()
        self.notebook_rf_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_rf_widget_1)
        self.notebook_rf_grid_layout_1 = Qt.QGridLayout()
        self.notebook_rf_layout_1.addLayout(self.notebook_rf_grid_layout_1)
        self.notebook_rf.addTab(self.notebook_rf_widget_1, "Waterfall")
        self.notebook_top_layout_0.addWidget(self.notebook_rf)
        self._chooser_gain_options = valid_gains
        self._chooser_gain_labels = ['{}'.format(g) for g in valid_gains]
        self._chooser_gain_tool_bar = Qt.QToolBar(self)
        self._chooser_gain_tool_bar.addWidget(Qt.QLabel("RF Gain"+": "))
        self._chooser_gain_combo_box = Qt.QComboBox()
        self._chooser_gain_tool_bar.addWidget(self._chooser_gain_combo_box)
        for label in self._chooser_gain_labels: self._chooser_gain_combo_box.addItem(label)
        self._chooser_gain_callback = lambda i: Qt.QMetaObject.invokeMethod(self._chooser_gain_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._chooser_gain_options.index(i)))
        self._chooser_gain_callback(self.chooser_gain)
        self._chooser_gain_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_chooser_gain(self._chooser_gain_options[i]))
        self.notebook_top_grid_layout_0.addWidget(self._chooser_gain_tool_bar, 0, 0, 1, 1)
        self._chooser_frequency_options = [f[0] for f in noaa_stations]
        self._chooser_frequency_labels = noaa_stations_labels
        self._chooser_frequency_tool_bar = Qt.QToolBar(self)
        self._chooser_frequency_tool_bar.addWidget(Qt.QLabel("NOAA Frequency"+": "))
        self._chooser_frequency_combo_box = Qt.QComboBox()
        self._chooser_frequency_tool_bar.addWidget(self._chooser_frequency_combo_box)
        for label in self._chooser_frequency_labels: self._chooser_frequency_combo_box.addItem(label)
        self._chooser_frequency_callback = lambda i: Qt.QMetaObject.invokeMethod(self._chooser_frequency_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._chooser_frequency_options.index(i)))
        self._chooser_frequency_callback(self.chooser_frequency)
        self._chooser_frequency_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_chooser_frequency(self._chooser_frequency_options[i]))
        self.top_grid_layout.addWidget(self._chooser_frequency_tool_bar, 0, 0, 1, 1)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(chooser_frequency, 0)
        self.rtlsdr_source_0.set_freq_corr(range_ppm_corr, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(chooser_gain, 0)
        self.rtlsdr_source_0.set_if_gain(1, 0)
        self.rtlsdr_source_0.set_bb_gain(1, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(16e3),
                decimation=int(samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	16e3, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1.enable_grid(False)
        
        if not True:
          self.qtgui_waterfall_sink_x_1.disable_legend()
        
        if "float" == "float" or "float" == "msg_float":
          self.qtgui_waterfall_sink_x_1.set_plot_pos_half(not False)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [3, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_1.set_intensity_range(-80, -40)
        
        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_1_win, 0,1,1,1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        
        if not False:
          self.qtgui_waterfall_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-80, -20)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.notebook_rf_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	16e3, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-80, -40)
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0_0.disable_legend()
        
        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not False)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_win, 0,0,1,1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	chooser_frequency, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-80, -20)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.notebook_rf_layout_0.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 6e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.high_pass_filter_0 = filter.fir_filter_fff(1, firdes.high_pass(
        	1, 16e3, 15, 5, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(16000, "", True)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=int(16e3),
        	quad_rate=int(16e3),
        	tau=75e-6,
        	max_dev=4e3,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.high_pass_filter_0, 0))    
        self.connect((self.high_pass_filter_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.high_pass_filter_0, 0), (self.qtgui_freq_sink_x_0_0, 0))    
        self.connect((self.high_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_1, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "noaa_weather")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_valid_gains(self):
        return self.valid_gains

    def set_valid_gains(self, valid_gains):
        self.valid_gains = valid_gains
        self.set_chooser_gain(self.valid_gains[-1])

    def get_noaa_stations(self):
        return self.noaa_stations

    def set_noaa_stations(self, noaa_stations):
        self.noaa_stations = noaa_stations
        self.set_chooser_frequency(self.noaa_stations[0][0])
        self.set_noaa_stations_labels(['{:>7.3f} MHz (Channel {:3})'.format(f[0]/1e6, f[1]) for f in self.noaa_stations])

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 6e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.chooser_frequency, self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_range_ppm_corr(self):
        return self.range_ppm_corr

    def set_range_ppm_corr(self, range_ppm_corr):
        self.range_ppm_corr = range_ppm_corr
        self.rtlsdr_source_0.set_freq_corr(self.range_ppm_corr, 0)

    def get_noaa_stations_labels(self):
        return self.noaa_stations_labels

    def set_noaa_stations_labels(self, noaa_stations_labels):
        self.noaa_stations_labels = noaa_stations_labels

    def get_chooser_gain(self):
        return self.chooser_gain

    def set_chooser_gain(self, chooser_gain):
        self.chooser_gain = chooser_gain
        self._chooser_gain_callback(self.chooser_gain)
        self.rtlsdr_source_0.set_gain(self.chooser_gain, 0)

    def get_chooser_frequency(self):
        return self.chooser_frequency

    def set_chooser_frequency(self, chooser_frequency):
        self.chooser_frequency = chooser_frequency
        self._chooser_frequency_callback(self.chooser_frequency)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.chooser_frequency, self.samp_rate)
        self.rtlsdr_source_0.set_center_freq(self.chooser_frequency, 0)


def main(top_block_cls=noaa_weather, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
