
from PyQt5 import QtCore, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np
import pandas as pd

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
        self.splitter_3.setGeometry(QtCore.QRect(20, 520, 751, 41))
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.start_plot_button = QtWidgets.QPushButton(self.splitter_3)
        self.start_plot_button.setObjectName("start_plot_button")
        self.stop_plot_button = QtWidgets.QPushButton(self.splitter_3)
        self.stop_plot_button.setObjectName("stop_plot_button")
        self.append_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.append_checkbox.setGeometry(QtCore.QRect(620, 500, 71, 20))
        self.append_checkbox.setObjectName("append_checkbox")
        self.error_label = QtWidgets.QLabel(self.centralwidget)
        self.error_label.setGeometry(QtCore.QRect(20, 560, 371, 16))
        self.error_label.setStyleSheet("color: rgb(255, 0, 0);")
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")
        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setGeometry(QtCore.QRect(700, 500, 71, 20))
        self.reset_button.setObjectName("reset_button")
        self.update_line = QtWidgets.QLineEdit(self.centralwidget)
        self.update_line.setGeometry(QtCore.QRect(20, 500, 41, 20))
        self.update_line.setObjectName("update_line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 500, 21, 20))
        self.label.setObjectName("label")
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

        # Initialize timer
        self.timer = QtCore.QTimer()

        # Set checkbox
        self.append_checkbox.setChecked(True)

        # Buttons
        self.start_plot_button.clicked.connect(self.start_plot)

        # Others
        self.osc_input_collector = []

    def retranslateUi(self, Plot_window):
        _translate = QtCore.QCoreApplication.translate
        Plot_window.setWindowTitle(_translate("Plot_window", "MainWindow"))
        self.start_plot_button.setText(_translate("Plot_window", "Start plot"))
        self.stop_plot_button.setText(_translate("Plot_window", "Stop plot"))
        self.append_checkbox.setText(_translate("Plot_window", "Appending"))
        self.reset_button.setText(_translate("Plot_window", "Reset"))
        self.label.setText(_translate("Plot_window", "[ms]"))
        self.update_line.setText('100')

    def start_plot(self):
        if self.data_collector.osc == None:
            self.error_label.setText('Please start oscilloscope first.')
        elif self.data_collector.filter==None:
            self.error_label.setText('Please insert filter values.')
        elif self.data_collector.pid == None:
            self.error_label.setText('Please insert PID controller values.')
        else:
            # Set timer for plot update
            timer_interval = int(self.update_line.text())
            if timer_interval < 100:
                self.error_label.setText('Smallest possible interval value is 100ms')
            else:
                self.error_label.setText(' ')
                self.timer.setInterval(timer_interval)
                self.timer.timeout.connect(self.update_plot)
                self.timer.start()

    def update_plot(self):

        self.stop_plot_button.clicked.connect(self.stop_plot)
        self.start_plot_button.clicked.connect(self.start_plot)

        # Clear all windows
        window_list = [self.plot_window_1, self.plot_window_2, self.plot_window_3, self.plot_window_4]
        for window in window_list:
            window.clear()

        # Plot new data
        color_list = [pg.mkPen(color=(255, 0, 0)), pg.mkPen(color=(0, 255, 0)), pg.mkPen(color=(0, 0, 255)), pg.mkPen(color=(100, 100, 100))]
        signal_list = self.get_signals()
        for n, window in enumerate(window_list):
            window.plot(signal_list[n]['time'], signal_list[n]['ch'], pen=color_list[n]) # in s
        
        # Output data
        #self.data_collector.awg.generate(signal_list[-1])

    def get_signals(self):
        self.reset_button.clicked.connect(self.data_collector.osc.clear_collector)
        self.append_checkbox.stateChanged.connect(self.data_collector.osc.clear_collector)
        # osc input
        osc_input_df_single = self.data_collector.osc.get_osc_input(append=False)
        osc_input_df_append = self.data_collector.osc.get_osc_input(append=True)
        if self.append_checkbox.isChecked():
            osc_screen = osc_input_df_append
        else:
            osc_screen = osc_input_df_single
        
        # demodulated signal and filter signal
        demod_signal_df_append = self.data_collector.dither.demodulate(osc_input_df_append)
        filter_output_df_append = self.data_collector.filter.apply(demod_signal_df_append)
        if self.append_checkbox.isChecked():
            demod_signal_screen = demod_signal_df_append
            filter_screen = filter_output_df_append
        else:
            demod_signal_screen = self.data_collector.dither.demodulate(osc_input_df_single)
            filter_screen = self.data_collector.filter.apply(demod_signal_screen)
        # PID controller output
        pid_output = self.data_collector.pid.get_PID_output(filter_output_df_append)
        # Add dither signal to pid output
        t = np.array(pid_output['time'])
        pid_output_dith_np = np.array(pid_output['ch']) + self.data_collector.dither.amp_dith * np.sin(2*np.pi*self.data_collector.dither.dith_freq * t)
        # Add offset to pid_output
        pid_output_dith_np = 1/10 * 100/2 + pid_output_dith_np
        # Protection that output signal does not get to high for piezo and not negative
        # Done by using voltage limit switch of piezoelectric controller (voltage limit = 100V)
        # Convert to data frame
        pid_output_dith = pd.DataFrame(np.concatenate((np.reshape(t, (-1,1)), np.reshape(pid_output_dith_np, (-1,1))), axis=1), columns=['time', 'ch'])

        # return signal list
        return [osc_screen, demod_signal_screen, filter_screen, pid_output_dith]

    def stop_plot(self):
        self.timer.stop()