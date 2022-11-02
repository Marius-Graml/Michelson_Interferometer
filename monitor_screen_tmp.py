# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'monitor_screen.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Plot_window(object):
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

    def retranslateUi(self, Plot_window):
        _translate = QtCore.QCoreApplication.translate
        Plot_window.setWindowTitle(_translate("Plot_window", "MainWindow"))
        self.start_plot_button.setText(_translate("Plot_window", "Start plot"))
        self.stop_plot_button.setText(_translate("Plot_window", "Stop plot"))
        self.append_checkbox.setText(_translate("Plot_window", "Appending"))
        self.reset_button.setText(_translate("Plot_window", "Reset"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Plot_window = QtWidgets.QMainWindow()
    ui = Ui_Plot_window()
    ui.setupUi(Plot_window)
    Plot_window.show()
    sys.exit(app.exec_())