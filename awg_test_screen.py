
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from dither_class import dither

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 615)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 781, 491))
        self.graphicsView.setObjectName("graphicsView")
        self.stop_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.stop_checkbox.setGeometry(QtCore.QRect(20, 530, 70, 17))
        self.stop_checkbox.setObjectName("stop_checkbox")
        self.output_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.output_checkbox.setGeometry(QtCore.QRect(120, 530, 91, 17))
        self.output_checkbox.setObjectName("output_checkbox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.graphicsView.setBackground('w')
        plot_handle = self.graphicsView.getPlotItem()
        plot_handle.setLabel(axis='bottom', text='time [s]')
        plot_handle.setLabel(axis='left', text='Voltage [V]')
        plot_handle.showGrid(x =True, y=True)

        # Config AWG
        self.t = 0
        self.rand_signal = np.zeros((65536, 1))

        # Initialize timer
        self.timer = QtCore.QTimer()
        # Start plotting
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.check_function)
        self.timer.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.stop_checkbox.setText(_translate("MainWindow", "Stop"))
        self.output_checkbox.setText(_translate("MainWindow", "No output"))

    def check_function(self):
        if not self.output_checkbox.isChecked():
            return
        else:
            self.my_dither.amp_dith = 0

        # Generate random output signal
    def generate_signal(self):

        if not self.stop_checkbox.isChecked():
            self.t, self.rand_signal= self.get_rand_signal()
        else:
            print('stopped')

        # Plot
        self.graphicsView.clear()
        self.graphicsView.plot(self.t, self.rand_signal, pen=pg.mkPen(color=(0,0,255)))


        # Generate output
        if not self.output_checkbox.isChecked():
            self.my_awg.obj.generate_waveform(channel=1, sample_rate='15.625Ms',lut_data=self.rand_signal.tolist(), frequency = 238, amplitude=1)
            #self.my_awg.obj.generate_waveform(channel=2, sample_rate='15.625Ms',lut_data=self.rand_signal.tolist(), frequency = 1e3, amplitude=1)
        else:
            self.my_awg.output(enable=False)

    def get_rand_signal(self):
        freq = 238
        amp = 1
        random_const = np.random.rand(1)
        #random_const = 0  

        print(random_const)

        random_arr = np.repeat(random_const, 65536, axis=0)

        fs = 15.625e6
        t = np.arange(0, 65536)/fs
        dith_signal = amp*np.sin(2*np.pi*freq*t)

        rand_signal = dith_signal + random_arr

        return t, rand_signal


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
