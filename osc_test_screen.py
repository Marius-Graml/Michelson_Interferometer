
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
from osc_class import osc
import pyqtgraph as pg

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 10, 771, 441))
        self.graphicsView.setObjectName("graphicsView")
        self.append_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.append_checkbox.setGeometry(QtCore.QRect(30, 490, 70, 17))
        self.append_checkbox.setObjectName("append_checkbox")
        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setGeometry(QtCore.QRect(170, 490, 75, 23))
        self.reset_button.setObjectName("reset_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
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

        self.append_checkbox.setChecked(True)

        # Config OSC
        self.my_osc = osc(ip_address='[fe80:0000:0000:0000:7269:79ff:feb9:0c22%12]', timebase = [-1, 1], input_ch = 1, output_ch=1)

        # Initialize timer
        self.timer = QtCore.QTimer()
        # Start plotting
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.plot_signal)
        self.timer.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.append_checkbox.setText(_translate("MainWindow", "Append"))
        self.reset_button.setText(_translate("MainWindow", "Reset"))

    def plot_signal(self):
        self.reset_button.clicked.connect(self.reset_function)
        out_signal = self.my_osc.get_osc_input(append=self.append_checkbox.isChecked(), dith_freq=0, filtered=0)[0]
        self.graphicsView.clear()
        self.graphicsView.plot(out_signal['time'], out_signal['ch'], pen=pg.mkPen(color=(0, 102, 0)))

    def reset_function(self):
        self.my_osc.clear_collector()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
