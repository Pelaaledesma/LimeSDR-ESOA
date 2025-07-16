#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import limesdr
import time
import threading
import top_block_fm_completo_epy_block_0 as epy_block_0  # embedded python block
import top_block_fm_completo_epy_block_1 as epy_block_1  # embedded python block



from gnuradio import qtgui

class top_block_fm_completo(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
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

        self.settings = Qt.QSettings("GNU Radio", "top_block_fm_completo")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.variable_qtgui_label_3 = variable_qtgui_label_3 = 0
        self.tx_gain = tx_gain = 45
        self.samp_rate_mult = samp_rate_mult = 480000
        self.samp_rate = samp_rate = 48000
        self.rx_gain = rx_gain = 0
        self.rb_control = rb_control = 101
        self.q_filter = q_filter = 40
        self.pb_push_to_talk = pb_push_to_talk = 0
        self.movil_avg = movil_avg = 50
        self.label_pot_TX = label_pot_TX = 45
        self.label_pot_RX = label_pot_RX = 0
        self.label_SNR_S = label_SNR_S = 0
        self.label_SNR_ND = label_SNR_ND = 0
        self.label_SNR = label_SNR = 0
        self.label_SINAD_SND = label_SINAD_SND = 0
        self.label_SINAD_ND = label_SINAD_ND = 0
        self.label_SINAD = label_SINAD = 0
        self.function_probe_SNR_S = function_probe_SNR_S = 0
        self.function_probe_SNR_ND = function_probe_SNR_ND = 0
        self.function_probe_SNR = function_probe_SNR = 0
        self.function_probe_SINAD_SND = function_probe_SINAD_SND = 0
        self.function_probe_SINAD_ND = function_probe_SINAD_ND = 0
        self.function_probe_SINAD = function_probe_SINAD = 0
        self.func_probe_rate = func_probe_rate = 2
        self.audio_vol = audio_vol = 0
        self.TX_FREQ_FINE = TX_FREQ_FINE = 0
        self.TX_FREQ_COARSE = TX_FREQ_COARSE = 916000000
        self.RX_FREQ_FINE = RX_FREQ_FINE = 0
        self.RX_FREQ_COARSE = RX_FREQ_COARSE = 916000000
        self.Fc_1F = Fc_1F = 0
        self.AUD_GAIN = AUD_GAIN = 1

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_range = Range(0, 73, 1, 45, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, "'tx_gain'", "dial", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tx_gain_win)
        self._rx_gain_range = Range(0, 60, 1, 0, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, "'rx_gain'", "dial", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_gain_win)
        self._TX_FREQ_FINE_range = Range(-100000, 100000, 1, 0, 200)
        self._TX_FREQ_FINE_win = RangeWidget(self._TX_FREQ_FINE_range, self.set_TX_FREQ_FINE, "'TX_FREQ_FINE'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._TX_FREQ_FINE_win)
        self._TX_FREQ_COARSE_range = Range(140000000, 3000000000, 100000, 916000000, 200)
        self._TX_FREQ_COARSE_win = RangeWidget(self._TX_FREQ_COARSE_range, self.set_TX_FREQ_COARSE, "'TX_FREQ_COARSE'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._TX_FREQ_COARSE_win)
        self._RX_FREQ_FINE_range = Range(-100000, 100000, 1, 0, 200)
        self._RX_FREQ_FINE_win = RangeWidget(self._RX_FREQ_FINE_range, self.set_RX_FREQ_FINE, "'RX_FREQ_FINE'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._RX_FREQ_FINE_win)
        self._RX_FREQ_COARSE_range = Range(40000000, 3000000000, 100000, 916000000, 200)
        self._RX_FREQ_COARSE_win = RangeWidget(self._RX_FREQ_COARSE_range, self.set_RX_FREQ_COARSE, "'RX_FREQ_COARSE'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._RX_FREQ_COARSE_win)
        self._variable_qtgui_label_3_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_3_formatter = None
        else:
            self._variable_qtgui_label_3_formatter = lambda x: str(x)

        self._variable_qtgui_label_3_tool_bar.addWidget(Qt.QLabel("'variable_qtgui_label_3'"))
        self._variable_qtgui_label_3_label = Qt.QLabel(str(self._variable_qtgui_label_3_formatter(self.variable_qtgui_label_3)))
        self._variable_qtgui_label_3_tool_bar.addWidget(self._variable_qtgui_label_3_label)
        self.top_layout.addWidget(self._variable_qtgui_label_3_tool_bar)
        # Create the options list
        self._rb_control_options = [101, 102, 103]
        # Create the labels list
        self._rb_control_labels = ['Full Duplex', 'Push to Talk', 'Test']
        # Create the combo box
        # Create the radio buttons
        self._rb_control_group_box = Qt.QGroupBox("OPTIONS" + ": ")
        self._rb_control_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._rb_control_button_group = variable_chooser_button_group()
        self._rb_control_group_box.setLayout(self._rb_control_box)
        for i, _label in enumerate(self._rb_control_labels):
            radio_button = Qt.QRadioButton(_label)
            self._rb_control_box.addWidget(radio_button)
            self._rb_control_button_group.addButton(radio_button, i)
        self._rb_control_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rb_control_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._rb_control_options.index(i)))
        self._rb_control_callback(self.rb_control)
        self._rb_control_button_group.buttonClicked[int].connect(
            lambda i: self.set_rb_control(self._rb_control_options[i]))
        self.top_layout.addWidget(self._rb_control_group_box)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=10,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_tab_widget_9 = Qt.QTabWidget()
        self.qtgui_tab_widget_9_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_9_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_9_widget_0)
        self.qtgui_tab_widget_9_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_9_layout_0.addLayout(self.qtgui_tab_widget_9_grid_layout_0)
        self.qtgui_tab_widget_9.addTab(self.qtgui_tab_widget_9_widget_0, 'CONTROL')
        self.top_layout.addWidget(self.qtgui_tab_widget_9)
        self.qtgui_tab_widget_8 = Qt.QTabWidget()
        self.qtgui_tab_widget_8_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_8_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_8_widget_0)
        self.qtgui_tab_widget_8_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_8_layout_0.addLayout(self.qtgui_tab_widget_8_grid_layout_0)
        self.qtgui_tab_widget_8.addTab(self.qtgui_tab_widget_8_widget_0, 'SNR')
        self.top_layout.addWidget(self.qtgui_tab_widget_8)
        self.qtgui_tab_widget_7 = Qt.QTabWidget()
        self.qtgui_tab_widget_7_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_7_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_7_widget_0)
        self.qtgui_tab_widget_7_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_7_layout_0.addLayout(self.qtgui_tab_widget_7_grid_layout_0)
        self.qtgui_tab_widget_7.addTab(self.qtgui_tab_widget_7_widget_0, 'RX CONTROL')
        self.top_layout.addWidget(self.qtgui_tab_widget_7)
        self.qtgui_tab_widget_6 = Qt.QTabWidget()
        self.qtgui_tab_widget_6_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_6_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_6_widget_0)
        self.qtgui_tab_widget_6_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_6_layout_0.addLayout(self.qtgui_tab_widget_6_grid_layout_0)
        self.qtgui_tab_widget_6.addTab(self.qtgui_tab_widget_6_widget_0, 'TX CONTROL')
        self.top_layout.addWidget(self.qtgui_tab_widget_6)
        self.qtgui_tab_widget_5 = Qt.QTabWidget()
        self.qtgui_tab_widget_5_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_5_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_5_widget_0)
        self.qtgui_tab_widget_5_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_5_layout_0.addLayout(self.qtgui_tab_widget_5_grid_layout_0)
        self.qtgui_tab_widget_5.addTab(self.qtgui_tab_widget_5_widget_0, 'Push to Talk')
        self.top_layout.addWidget(self.qtgui_tab_widget_5)
        self.qtgui_tab_widget_4 = Qt.QTabWidget()
        self.qtgui_tab_widget_4_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_4_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_4_widget_0)
        self.qtgui_tab_widget_4_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_4_layout_0.addLayout(self.qtgui_tab_widget_4_grid_layout_0)
        self.qtgui_tab_widget_4.addTab(self.qtgui_tab_widget_4_widget_0, 'SINAD')
        self.top_layout.addWidget(self.qtgui_tab_widget_4)
        self.qtgui_tab_widget_3 = Qt.QTabWidget()
        self.qtgui_tab_widget_3_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_3_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_3_widget_0)
        self.qtgui_tab_widget_3_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_3_layout_0.addLayout(self.qtgui_tab_widget_3_grid_layout_0)
        self.qtgui_tab_widget_3.addTab(self.qtgui_tab_widget_3_widget_0, 'FREQ')
        self.qtgui_tab_widget_3_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_3_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_3_widget_1)
        self.qtgui_tab_widget_3_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_3_layout_1.addLayout(self.qtgui_tab_widget_3_grid_layout_1)
        self.qtgui_tab_widget_3.addTab(self.qtgui_tab_widget_3_widget_1, 'TIME')
        self.top_layout.addWidget(self.qtgui_tab_widget_3)
        self.qtgui_tab_widget_2 = Qt.QTabWidget()
        self.qtgui_tab_widget_2_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_2_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_2_widget_0)
        self.qtgui_tab_widget_2_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_2_layout_0.addLayout(self.qtgui_tab_widget_2_grid_layout_0)
        self.qtgui_tab_widget_2.addTab(self.qtgui_tab_widget_2_widget_0, 'FREQ')
        self.qtgui_tab_widget_2_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_2_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_2_widget_1)
        self.qtgui_tab_widget_2_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_2_layout_1.addLayout(self.qtgui_tab_widget_2_grid_layout_1)
        self.qtgui_tab_widget_2.addTab(self.qtgui_tab_widget_2_widget_1, 'TIME')
        self.top_layout.addWidget(self.qtgui_tab_widget_2)
        self.qtgui_tab_widget_1 = Qt.QTabWidget()
        self.qtgui_tab_widget_1_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_1_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_1_widget_0)
        self.qtgui_tab_widget_1_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_1_layout_0.addLayout(self.qtgui_tab_widget_1_grid_layout_0)
        self.qtgui_tab_widget_1.addTab(self.qtgui_tab_widget_1_widget_0, 'FREQ')
        self.qtgui_tab_widget_1_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_1_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_1_widget_1)
        self.qtgui_tab_widget_1_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_1_layout_1.addLayout(self.qtgui_tab_widget_1_grid_layout_1)
        self.qtgui_tab_widget_1.addTab(self.qtgui_tab_widget_1_widget_1, 'TIME')
        self.top_layout.addWidget(self.qtgui_tab_widget_1)
        self.qtgui_tab_widget_0 = Qt.QTabWidget()
        self.qtgui_tab_widget_0_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_0)
        self.qtgui_tab_widget_0_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_0.addLayout(self.qtgui_tab_widget_0_grid_layout_0)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_0, 'SIGNAL+NOISE+DISTORTION')
        self.qtgui_tab_widget_0_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_1)
        self.qtgui_tab_widget_0_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_1.addLayout(self.qtgui_tab_widget_0_grid_layout_1)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_1, 'SIGNAL')
        self.qtgui_tab_widget_0_widget_2 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_2)
        self.qtgui_tab_widget_0_grid_layout_2 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_2.addLayout(self.qtgui_tab_widget_0_grid_layout_2)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_2, 'NOISE+DISTORTION')
        self.top_layout.addWidget(self.qtgui_tab_widget_0)
        self.qtgui_freq_sink_x_2 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_2.set_update_time(0.10)
        self.qtgui_freq_sink_x_2.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_2.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_2.enable_autoscale(False)
        self.qtgui_freq_sink_x_2.enable_grid(False)
        self.qtgui_freq_sink_x_2.set_fft_average(1.0)
        self.qtgui_freq_sink_x_2.enable_axis_labels(True)
        self.qtgui_freq_sink_x_2.enable_control_panel(False)
        self.qtgui_freq_sink_x_2.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_2.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_2_win = sip.wrapinstance(self.qtgui_freq_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_2_win)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            48000, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        _pb_push_to_talk_push_button = Qt.QPushButton('PUSH TO TALK')
        _pb_push_to_talk_push_button = Qt.QPushButton('PUSH TO TALK')
        self._pb_push_to_talk_choices = {'Pressed': 1, 'Released': 0}
        _pb_push_to_talk_push_button.pressed.connect(lambda: self.set_pb_push_to_talk(self._pb_push_to_talk_choices['Pressed']))
        _pb_push_to_talk_push_button.released.connect(lambda: self.set_pb_push_to_talk(self._pb_push_to_talk_choices['Released']))
        self.top_layout.addWidget(_pb_push_to_talk_push_button)
        self.low_pass_filter_1 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate_mult,
                10000,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                0.2,
                samp_rate,
                10000,
                movil_avg,
                window.WIN_HAMMING,
                6.76))
        self.limesdr_source_0 = limesdr.source('0009061C01502103', 0, '')
        self.limesdr_source_0.set_sample_rate(samp_rate_mult)
        self.limesdr_source_0.set_center_freq(RX_FREQ_COARSE+RX_FREQ_FINE, 0)
        self.limesdr_source_0.set_bandwidth(5e6, 0)
        self.limesdr_source_0.set_digital_filter(samp_rate_mult/2,0)
        self.limesdr_source_0.set_gain(rx_gain,0)
        self.limesdr_source_0.set_antenna(255,0)
        self.limesdr_source_0.calibrate(5e6, 0)
        self.limesdr_source_0.set_block_alias("limesdr_source_0")
        self.limesdr_sink_0 = limesdr.sink('0009061c01502103', 0, '', '')
        self.limesdr_sink_0.set_sample_rate(samp_rate_mult)
        self.limesdr_sink_0.set_center_freq(TX_FREQ_COARSE+TX_FREQ_FINE, 0)
        self.limesdr_sink_0.set_bandwidth(5e6,0)
        self.limesdr_sink_0.set_digital_filter(samp_rate_mult/2,0)
        self.limesdr_sink_0.set_gain(tx_gain,0)
        self.limesdr_sink_0.set_antenna(255,0)
        self.limesdr_sink_0.calibrate(5e6, 0)
        self.limesdr_sink_0.set_block_alias("limesdr_sink_0")
        self._label_pot_TX_tool_bar = Qt.QToolBar(self)

        if None:
            self._label_pot_TX_formatter = None
        else:
            self._label_pot_TX_formatter = lambda x: repr(x)

        self._label_pot_TX_tool_bar.addWidget(Qt.QLabel("Gain [dB]"))
        self._label_pot_TX_label = Qt.QLabel(str(self._label_pot_TX_formatter(self.label_pot_TX)))
        self._label_pot_TX_tool_bar.addWidget(self._label_pot_TX_label)
        self.top_layout.addWidget(self._label_pot_TX_tool_bar)
        self._label_pot_RX_tool_bar = Qt.QToolBar(self)

        if None:
            self._label_pot_RX_formatter = None
        else:
            self._label_pot_RX_formatter = lambda x: repr(x)

        self._label_pot_RX_tool_bar.addWidget(Qt.QLabel("Gain [dB]"))
        self._label_pot_RX_label = Qt.QLabel(str(self._label_pot_RX_formatter(self.label_pot_RX)))
        self._label_pot_RX_tool_bar.addWidget(self._label_pot_RX_label)
        self.top_layout.addWidget(self._label_pot_RX_tool_bar)
        self._label_SNR_S_tool_bar = Qt.QToolBar(self)

        if None:
            self._label_SNR_S_formatter = None
        else:
            self._label_SNR_S_formatter = lambda x: repr(x)

        self._label_SNR_S_tool_bar.addWidget(Qt.QLabel("SNR (Signal)"))
        self._label_SNR_S_label = Qt.QLabel(str(self._label_SNR_S_formatter(self.label_SNR_S)))
        self._label_SNR_S_tool_bar.addWidget(self._label_SNR_S_label)
        self.top_layout.addWidget(self._label_SNR_S_tool_bar)
        self._label_SNR_ND_tool_bar = Qt.QToolBar(self)

        if None:
            self._label_SNR_ND_formatter = None
        else:
            self._label_SNR_ND_formatter = lambda x: repr(x)

        self._label_SNR_ND_tool_bar.addWidget(Qt.QLabel("SNR (Noise + Distortion)"))
        self._label_SNR_ND_label = Qt.QLabel(str(self._label_SNR_ND_formatter(self.label_SNR_ND)))
        self._label_SNR_ND_tool_bar.addWidget(self._label_SNR_ND_label)
        self.top_layout.addWidget(self._label_SNR_ND_tool_bar)
        self._label_SNR_tool_bar = Qt.QToolBar(self)

        if None:
            self._label_SNR_formatter = None
        else:
            self._label_SNR_formatter = lambda x: repr(x)

        self._label_SNR_tool_bar.addWidget(Qt.QLabel("SNR"))
        self._label_SNR_label = Qt.QLabel(str(self._label_SNR_formatter(self.label_SNR)))
        self._label_SNR_tool_bar.addWidget(self._label_SNR_label)
        self.top_layout.addWidget(self._label_SNR_tool_bar)
        self._label_SINAD_SND_tool_bar = Qt.QToolBar(self)

        if None:
            self._label_SINAD_SND_formatter = None
        else:
            self._label_SINAD_SND_formatter = lambda x: repr(x)

        self._label_SINAD_SND_tool_bar.addWidget(Qt.QLabel("SINAD (Signal + Noise + Distortion)"))
        self._label_SINAD_SND_label = Qt.QLabel(str(self._label_SINAD_SND_formatter(self.label_SINAD_SND)))
        self._label_SINAD_SND_tool_bar.addWidget(self._label_SINAD_SND_label)
        self.top_layout.addWidget(self._label_SINAD_SND_tool_bar)
        self._label_SINAD_ND_tool_bar = Qt.QToolBar(self)

        if None:
            self._label_SINAD_ND_formatter = None
        else:
            self._label_SINAD_ND_formatter = lambda x: repr(x)

        self._label_SINAD_ND_tool_bar.addWidget(Qt.QLabel("SINAD (Noise + Distortion)"))
        self._label_SINAD_ND_label = Qt.QLabel(str(self._label_SINAD_ND_formatter(self.label_SINAD_ND)))
        self._label_SINAD_ND_tool_bar.addWidget(self._label_SINAD_ND_label)
        self.top_layout.addWidget(self._label_SINAD_ND_tool_bar)
        self._label_SINAD_tool_bar = Qt.QToolBar(self)

        if None:
            self._label_SINAD_formatter = None
        else:
            self._label_SINAD_formatter = lambda x: repr(x)

        self._label_SINAD_tool_bar.addWidget(Qt.QLabel("SINAD"))
        self._label_SINAD_label = Qt.QLabel(str(self._label_SINAD_formatter(self.label_SINAD)))
        self._label_SINAD_tool_bar.addWidget(self._label_SINAD_label)
        self.top_layout.addWidget(self._label_SINAD_tool_bar)
        def _function_probe_SNR_S_probe():
          while True:

            val = self.epy_block_SNR.get_S()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_function_probe_SNR_S,val))
              except AttributeError:
                self.set_function_probe_SNR_S(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (func_probe_rate))
        _function_probe_SNR_S_thread = threading.Thread(target=_function_probe_SNR_S_probe)
        _function_probe_SNR_S_thread.daemon = True
        _function_probe_SNR_S_thread.start()
        def _function_probe_SNR_ND_probe():
          while True:

            val = self.epy_block_SNR.get_ND()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_function_probe_SNR_ND,val))
              except AttributeError:
                self.set_function_probe_SNR_ND(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (func_probe_rate))
        _function_probe_SNR_ND_thread = threading.Thread(target=_function_probe_SNR_ND_probe)
        _function_probe_SNR_ND_thread.daemon = True
        _function_probe_SNR_ND_thread.start()
        def _function_probe_SNR_probe():
          while True:

            val = self.epy_block_SNR.get_SNR()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_function_probe_SNR,val))
              except AttributeError:
                self.set_function_probe_SNR(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (func_probe_rate))
        _function_probe_SNR_thread = threading.Thread(target=_function_probe_SNR_probe)
        _function_probe_SNR_thread.daemon = True
        _function_probe_SNR_thread.start()
        def _function_probe_SINAD_SND_probe():
          while True:

            val = self.epy_block_sinad.get_SND()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_function_probe_SINAD_SND,val))
              except AttributeError:
                self.set_function_probe_SINAD_SND(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (func_probe_rate))
        _function_probe_SINAD_SND_thread = threading.Thread(target=_function_probe_SINAD_SND_probe)
        _function_probe_SINAD_SND_thread.daemon = True
        _function_probe_SINAD_SND_thread.start()
        def _function_probe_SINAD_ND_probe():
          while True:

            val = self.epy_block_sinad.get_ND()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_function_probe_SINAD_ND,val))
              except AttributeError:
                self.set_function_probe_SINAD_ND(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (func_probe_rate))
        _function_probe_SINAD_ND_thread = threading.Thread(target=_function_probe_SINAD_ND_probe)
        _function_probe_SINAD_ND_thread.daemon = True
        _function_probe_SINAD_ND_thread.start()
        def _function_probe_SINAD_probe():
          while True:

            val = self.epy_block_sinad.get_SINAD()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_function_probe_SINAD,val))
              except AttributeError:
                self.set_function_probe_SINAD(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (func_probe_rate))
        _function_probe_SINAD_thread = threading.Thread(target=_function_probe_SINAD_probe)
        _function_probe_SINAD_thread.daemon = True
        _function_probe_SINAD_thread.start()
        self.epy_block_1 = epy_block_1.snr_calculator(sample_rate=samp_rate, signal_freq=, num_samples=1000, q_notch=q_filter, q_bp=q_filter, mov_avg_len=movil_avg)
        self.epy_block_0 = epy_block_0.sinad_calculator(sample_rate=samp_rate, signal_freq=, num_samples=1000, q_param=40, mov_avg_len=50)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1)
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                200,
                5000,
                movil_avg,
                window.WIN_HAMMING,
                6.76))
        self._audio_vol_range = Range(0, 4, 0.05, 0, 200)
        self._audio_vol_win = RangeWidget(self._audio_vol_range, self.set_audio_vol, "Volumen", "dial", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._audio_vol_win)
        self.audio_source_0 = audio.source(48000, '', True)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(0.6545)
        self.analog_fm_preemph_0 = analog.fm_preemph(fs=samp_rate, tau=75e-6, fh=-1.0)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=samp_rate_mult,
        	audio_decim=10,
        	deviation=5000,
        	audio_pass=3000,
        	audio_stop=4000,
        	gain=1.0,
        	tau=75e-6,
        )
        self._AUD_GAIN_range = Range(0, 5, 0.1, 1, 200)
        self._AUD_GAIN_win = RangeWidget(self._AUD_GAIN_range, self.set_AUD_GAIN, "Audio gain", "dial", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._AUD_GAIN_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.epy_block_0, 0))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.epy_block_1, 0))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.analog_fm_preemph_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_fm_preemph_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.epy_block_1, 0), (self.qtgui_freq_sink_x_2, 0))
        self.connect((self.epy_block_1, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.limesdr_source_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.limesdr_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block_fm_completo")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_qtgui_label_3(self):
        return self.variable_qtgui_label_3

    def set_variable_qtgui_label_3(self, variable_qtgui_label_3):
        self.variable_qtgui_label_3 = variable_qtgui_label_3
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_3_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_3_formatter(self.variable_qtgui_label_3))))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.limesdr_sink_0.set_gain(self.tx_gain,0)

    def get_samp_rate_mult(self):
        return self.samp_rate_mult

    def set_samp_rate_mult(self, samp_rate_mult):
        self.samp_rate_mult = samp_rate_mult
        self.limesdr_sink_0.set_digital_filter(self.samp_rate_mult/2,0)
        self.limesdr_source_0.set_digital_filter(self.samp_rate_mult/2,0)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate_mult, 10000, 1000, window.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, 200, 5000, self.movil_avg, window.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.epy_block_0.sample_rate = self.samp_rate
        self.epy_block_1.sample_rate = self.samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(0.2, self.samp_rate, 10000, self.movil_avg, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_2.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.limesdr_source_0.set_gain(self.rx_gain,0)

    def get_rb_control(self):
        return self.rb_control

    def set_rb_control(self, rb_control):
        self.rb_control = rb_control
        self._rb_control_callback(self.rb_control)

    def get_q_filter(self):
        return self.q_filter

    def set_q_filter(self, q_filter):
        self.q_filter = q_filter
        self.epy_block_1.q_bp = self.q_filter
        self.epy_block_1.q_notch = self.q_filter

    def get_pb_push_to_talk(self):
        return self.pb_push_to_talk

    def set_pb_push_to_talk(self, pb_push_to_talk):
        self.pb_push_to_talk = pb_push_to_talk

    def get_movil_avg(self):
        return self.movil_avg

    def set_movil_avg(self, movil_avg):
        self.movil_avg = movil_avg
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, 200, 5000, self.movil_avg, window.WIN_HAMMING, 6.76))
        self.epy_block_1.mov_avg_len = self.movil_avg
        self.low_pass_filter_0.set_taps(firdes.low_pass(0.2, self.samp_rate, 10000, self.movil_avg, window.WIN_HAMMING, 6.76))

    def get_label_pot_TX(self):
        return self.label_pot_TX

    def set_label_pot_TX(self, label_pot_TX):
        self.label_pot_TX = label_pot_TX
        Qt.QMetaObject.invokeMethod(self._label_pot_TX_label, "setText", Qt.Q_ARG("QString", str(self._label_pot_TX_formatter(self.label_pot_TX))))

    def get_label_pot_RX(self):
        return self.label_pot_RX

    def set_label_pot_RX(self, label_pot_RX):
        self.label_pot_RX = label_pot_RX
        Qt.QMetaObject.invokeMethod(self._label_pot_RX_label, "setText", Qt.Q_ARG("QString", str(self._label_pot_RX_formatter(self.label_pot_RX))))

    def get_label_SNR_S(self):
        return self.label_SNR_S

    def set_label_SNR_S(self, label_SNR_S):
        self.label_SNR_S = label_SNR_S
        Qt.QMetaObject.invokeMethod(self._label_SNR_S_label, "setText", Qt.Q_ARG("QString", str(self._label_SNR_S_formatter(self.label_SNR_S))))

    def get_label_SNR_ND(self):
        return self.label_SNR_ND

    def set_label_SNR_ND(self, label_SNR_ND):
        self.label_SNR_ND = label_SNR_ND
        Qt.QMetaObject.invokeMethod(self._label_SNR_ND_label, "setText", Qt.Q_ARG("QString", str(self._label_SNR_ND_formatter(self.label_SNR_ND))))

    def get_label_SNR(self):
        return self.label_SNR

    def set_label_SNR(self, label_SNR):
        self.label_SNR = label_SNR
        Qt.QMetaObject.invokeMethod(self._label_SNR_label, "setText", Qt.Q_ARG("QString", str(self._label_SNR_formatter(self.label_SNR))))

    def get_label_SINAD_SND(self):
        return self.label_SINAD_SND

    def set_label_SINAD_SND(self, label_SINAD_SND):
        self.label_SINAD_SND = label_SINAD_SND
        Qt.QMetaObject.invokeMethod(self._label_SINAD_SND_label, "setText", Qt.Q_ARG("QString", str(self._label_SINAD_SND_formatter(self.label_SINAD_SND))))

    def get_label_SINAD_ND(self):
        return self.label_SINAD_ND

    def set_label_SINAD_ND(self, label_SINAD_ND):
        self.label_SINAD_ND = label_SINAD_ND
        Qt.QMetaObject.invokeMethod(self._label_SINAD_ND_label, "setText", Qt.Q_ARG("QString", str(self._label_SINAD_ND_formatter(self.label_SINAD_ND))))

    def get_label_SINAD(self):
        return self.label_SINAD

    def set_label_SINAD(self, label_SINAD):
        self.label_SINAD = label_SINAD
        Qt.QMetaObject.invokeMethod(self._label_SINAD_label, "setText", Qt.Q_ARG("QString", str(self._label_SINAD_formatter(self.label_SINAD))))

    def get_function_probe_SNR_S(self):
        return self.function_probe_SNR_S

    def set_function_probe_SNR_S(self, function_probe_SNR_S):
        self.function_probe_SNR_S = function_probe_SNR_S

    def get_function_probe_SNR_ND(self):
        return self.function_probe_SNR_ND

    def set_function_probe_SNR_ND(self, function_probe_SNR_ND):
        self.function_probe_SNR_ND = function_probe_SNR_ND

    def get_function_probe_SNR(self):
        return self.function_probe_SNR

    def set_function_probe_SNR(self, function_probe_SNR):
        self.function_probe_SNR = function_probe_SNR

    def get_function_probe_SINAD_SND(self):
        return self.function_probe_SINAD_SND

    def set_function_probe_SINAD_SND(self, function_probe_SINAD_SND):
        self.function_probe_SINAD_SND = function_probe_SINAD_SND

    def get_function_probe_SINAD_ND(self):
        return self.function_probe_SINAD_ND

    def set_function_probe_SINAD_ND(self, function_probe_SINAD_ND):
        self.function_probe_SINAD_ND = function_probe_SINAD_ND

    def get_function_probe_SINAD(self):
        return self.function_probe_SINAD

    def set_function_probe_SINAD(self, function_probe_SINAD):
        self.function_probe_SINAD = function_probe_SINAD

    def get_func_probe_rate(self):
        return self.func_probe_rate

    def set_func_probe_rate(self, func_probe_rate):
        self.func_probe_rate = func_probe_rate

    def get_audio_vol(self):
        return self.audio_vol

    def set_audio_vol(self, audio_vol):
        self.audio_vol = audio_vol

    def get_TX_FREQ_FINE(self):
        return self.TX_FREQ_FINE

    def set_TX_FREQ_FINE(self, TX_FREQ_FINE):
        self.TX_FREQ_FINE = TX_FREQ_FINE
        self.limesdr_sink_0.set_center_freq(self.TX_FREQ_COARSE+self.TX_FREQ_FINE, 0)

    def get_TX_FREQ_COARSE(self):
        return self.TX_FREQ_COARSE

    def set_TX_FREQ_COARSE(self, TX_FREQ_COARSE):
        self.TX_FREQ_COARSE = TX_FREQ_COARSE
        self.limesdr_sink_0.set_center_freq(self.TX_FREQ_COARSE+self.TX_FREQ_FINE, 0)

    def get_RX_FREQ_FINE(self):
        return self.RX_FREQ_FINE

    def set_RX_FREQ_FINE(self, RX_FREQ_FINE):
        self.RX_FREQ_FINE = RX_FREQ_FINE
        self.limesdr_source_0.set_center_freq(self.RX_FREQ_COARSE+self.RX_FREQ_FINE, 0)

    def get_RX_FREQ_COARSE(self):
        return self.RX_FREQ_COARSE

    def set_RX_FREQ_COARSE(self, RX_FREQ_COARSE):
        self.RX_FREQ_COARSE = RX_FREQ_COARSE
        self.limesdr_source_0.set_center_freq(self.RX_FREQ_COARSE+self.RX_FREQ_FINE, 0)

    def get_Fc_1F(self):
        return self.Fc_1F

    def set_Fc_1F(self, Fc_1F):
        self.Fc_1F = Fc_1F

    def get_AUD_GAIN(self):
        return self.AUD_GAIN

    def set_AUD_GAIN(self, AUD_GAIN):
        self.AUD_GAIN = AUD_GAIN




def main(top_block_cls=top_block_fm_completo, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
