
from PyQt5 import QtCore, QtWidgets
from pyqtgraph import PlotWidget
from demodulation_code import demodulate
import pyqtgraph as pg

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
            plot_handle.setLabel(axis='bottom', text='time [ms]')
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

    def start_plot(self):
        if self.data_collector.osc == None:
            self.error_label.setText('Please start oscilloscope first.')
        elif self.data_collector.filter==None:
            self.error_label.setText('Please insert filter values.')
        elif self.data_collector.pid == None:
            self.error_label.setText('Please insert PID controller values.')
        else:
            # Set timer for plot update
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.update_plot)
            self.timer.start()

    def update_plot(self):

        self.stop_plot_button.clicked.connect(self.stop_plot)

        # Clear all windows
        window_list = [self.plot_window_1, self.plot_window_2, self.plot_window_3, self.plot_window_4]
        for window in window_list:
            window.clear()

        # Plot new data
        color_list = [pg.mkPen(color=(255, 0, 0)), pg.mkPen(color=(0, 255, 0)), pg.mkPen(color=(0, 0, 255)), pg.mkPen(color=(100, 100, 100))]
        signal_list = self.get_signals()
        for n, window in enumerate(window_list):
            window.plot(signal_list[n]['time']*1e3, signal_list[n]['ch'], pen=color_list[n]) # in ms

    def get_signals(self):
        # osc input
        osc_input_df = self.data_collector.osc.get_osc_input(append=self.append_checkbox.isChecked())
        self.reset_button.clicked.connect(self.data_collector.osc.clear_collector)
        self.append_checkbox.stateChanged.connect(self.data_collector.osc.clear_collector)
        # demodulated signal
        demod_signal_df = demodulate(osc_input_df, self.data_collector.osc.dith_freq, self.data_collector.osc.theta)
        # filter ouput
        filter_output = self.data_collector.filter.apply(demod_signal_df)
        # PID controller output
        pid_output = self.data_collector.pid.get_PID_output(filter_output)
        # return signal list
        return [osc_input_df, demod_signal_df, filter_output, pid_output]

    def stop_plot(self):
        self.timer.stop()