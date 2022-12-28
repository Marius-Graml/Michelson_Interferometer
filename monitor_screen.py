
from PyQt5 import QtCore, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from MDT_COMMAND_LIB import *

class Ui_Plot_window(object):
    def __init__(self, data_collector):
        self.data_collector = data_collector

    def setupUi(self, Plot_window):
        Plot_window.setObjectName("Plot_window")
        Plot_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Plot_window)
        self.centralwidget.setObjectName("centralwidget")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(20, 10, 751, 241))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.plot_window_1 = PlotWidget(self.splitter)
        self.plot_window_1.setObjectName("plot_window_1")
        self.plot_window_2 = PlotWidget(self.splitter)
        self.plot_window_2.setObjectName("plot_window_2")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setGeometry(QtCore.QRect(20, 260, 751, 231))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.plot_window_3 = PlotWidget(self.splitter_2)
        self.plot_window_3.setObjectName("plot_window_3")
        self.plot_window_4 = PlotWidget(self.splitter_2)
        self.plot_window_4.setObjectName("plot_window_4")
        self.splitter_3 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_3.setGeometry(QtCore.QRect(20, 500, 751, 51))
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.stop_checkbox = QtWidgets.QCheckBox(self.splitter_3)
        self.stop_checkbox.setObjectName("stop_checkbox")
        self.append_checkbox = QtWidgets.QCheckBox(self.splitter_3)
        self.append_checkbox.setObjectName("append_checkbox")
        self.en_out_checkbox = QtWidgets.QCheckBox(self.splitter_3)
        self.en_out_checkbox.setObjectName("en_out_checkbox")
        self.in_filter_checkbox = QtWidgets.QCheckBox(self.splitter_3)
        self.in_filter_checkbox.setObjectName("in_filter_checkbox")
        self.reset_button = QtWidgets.QPushButton(self.splitter_3)
        self.reset_button.setObjectName("reset_button")
        self.pid_output_edit = QtWidgets.QPlainTextEdit(self.splitter_3)
        self.pid_output_edit.setObjectName("pid_output_edit")
        self.splitter_4 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_4.setGeometry(QtCore.QRect(20, 550, 300, 21))
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.dither_checkbox = QtWidgets.QCheckBox(self.splitter_4)
        self.dither_checkbox.setObjectName("dither_checkbox")
        self.consider_checkbox = QtWidgets.QCheckBox(self.splitter_4)
        self.consider_checkbox.setObjectName("consider_checkbox")
        Plot_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Plot_window)
        self.statusbar.setObjectName("statusbar")
        Plot_window.setStatusBar(self.statusbar)
        self.retranslateUi(Plot_window)
        QtCore.QMetaObject.connectSlotsByName(Plot_window)

        # Set background to white
        window_list = [self.plot_window_1, self.plot_window_2, self.plot_window_3, self.plot_window_4]
        for window in window_list:
            window.setBackground('w')

        # PlotItem list
        plotItem_list = [window.getPlotItem() for window in window_list]

        # Set axis labels, grid and title
        title_list = ['Oscilloscope input', 'Demodulated signal', 'Filtered signal', 'PID output']
        for n, plot_handle in enumerate(plotItem_list):
            plot_handle.setLabel(axis='bottom', text='time [s]')
            plot_handle.setLabel(axis='left', text='Voltage [V]')
            plot_handle.showGrid(x =True, y=True)
            plot_handle.setTitle(title_list[n])

        # Set checkboxes
        self.append_checkbox.setChecked(True)
        self.en_out_checkbox.setChecked(True)
        self.consider_checkbox.setChecked(True)

        # Start Stop Flag
        self.flag = 0

        # Initialize timer
        self.timer = QtCore.QTimer()
        # Start plotting
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.check_stop_function)
        self.timer.start()

        # Initialize PZT-Controller
        devs = mdtListDevices()
        self.hdl = mdtOpen(devs[0][0], nBaud=115200, timeout=1)

        # Start Waveform-Generator
        self.data_collector.dither.generate()

    def retranslateUi(self, Plot_window):
        _translate = QtCore.QCoreApplication.translate
        Plot_window.setWindowTitle(_translate("Plot_window", "MainWindow"))
        self.stop_checkbox.setText(_translate("Plot_window", "Stop plot"))
        self.append_checkbox.setText(_translate("Plot_window", "Appending"))
        self.en_out_checkbox.setText(_translate("Plot_window", "Generate output"))
        self.in_filter_checkbox.setText(_translate("Plot_window", "Input filter"))
        self.reset_button.setText(_translate("Plot_window", "Reset"))
        self.dither_checkbox.setText(_translate("Plot_window", "Ignore dither signal"))
        self.consider_checkbox.setText(_translate("Plot_window", "Consider single sample"))

    def check_stop_function(self):
        if not self.stop_checkbox.isChecked():
            self.update_plot()
    
    def update_plot(self):

        self.reset_button.clicked.connect(self.reset_function)

        # Clear all windows
        window_list = [self.plot_window_1, self.plot_window_2, self.plot_window_3, self.plot_window_4]
        for window in window_list:
            window.clear()

        # Plot new data
        color_list = [pg.mkPen(color=(255, 0, 0)), pg.mkPen(color=(0, 255, 0)), pg.mkPen(color=(0, 0, 255)), pg.mkPen(color=(100, 100, 100))]
        if self.append_checkbox.isChecked():
            # Appending
            osc_signal, sig_mean = self.data_collector.osc.get_osc_input(append=True, dith_freq=self.data_collector.dither.dith_freq, filtered=self.in_filter_checkbox.isChecked())
            demod_signal = self.data_collector.dither.demodulate(osc_signal)
            filter_signal = self.data_collector.filter.apply(demod_signal)
        else:
            # No appending
            osc_signal, sig_mean = self.data_collector.osc.get_osc_input(append=False, dith_freq=self.data_collector.dither.dith_freq, filtered=self.in_filter_checkbox.isChecked())
            demod_signal = self.data_collector.dither.demodulate(osc_signal)
            filter_signal = self.data_collector.filter.apply(demod_signal)
        if self.dither_checkbox.isChecked():
            # Dither signal is not applied
            self.data_collector.pid.obj.output_limits = (-3,3)
            cont_sample, pid_output = self.data_collector.pid.get_PID_output_single(osc_signal, 0, 0, single=self.consider_checkbox.isChecked())[1]
        else:
            # Dither signal is applied
            self.data_collector.pid.obj.output_limits = (-3+self.data_collector.dither.amp_dith,3-self.data_collector.dither.amp_dith)
            cont_sample, pid_output = self.data_collector.pid.get_PID_output_single(filter_signal, self.data_collector.dither.dith_freq, self.data_collector.dither.amp_dith, single=self.consider_checkbox.isChecked())
        signal_list = [osc_signal, demod_signal, filter_signal, pid_output]

        for n, window in enumerate(window_list):
            print(n)
            print(window)
            window.plot(signal_list[n]['time'], signal_list[n]['ch'], pen=color_list[n]) # in s
        window_list[0].plot(sig_mean['time'], sig_mean['ch'], pen=pg.mkPen(color=(0, 102, 0)))
        
        print(cont_sample)
        mdtSetAllVoltage(hdl=self.hdl, voltage=cont_sample)

        # if self.en_out_checkbox.isChecked():
        #     self.data_collector.pid.obj.auto_mode = True
        #     self.data_collector.awg.output(enable=True)
        #     self.pid_output_edit.setPlainText('PID output: \n' + str(pid_output['ch'][0]))
        #     self.data_collector.awg.generate(pid_output['ch'], output_freq=self.data_collector.dither.dith_freq)
        # else:
        #     self.data_collector.pid.obj.auto_mode = False
        #     self.data_collector.awg.output(enable=False)




    def start_stop_function(self):
        if self.flag == 0:
            self.timer.stop()
            self.flag = 1
            self.start_stop_button.setText('Start plot')
        else:
            self.timer.start()
            self.flag = 0
            self.start_stop_button.setText('Stop plot')

    def reset_function(self):
        self.data_collector.osc.clear_collector()
        self.data_collector.pid.reset_pid()
        self.pid_output_edit.setPlainText('Input buffer and PID buffer reset.')
