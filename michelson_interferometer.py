
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from monitor_screen import Ui_Plot_window
from scipy import signal
import numpy as np
import pyqtgraph as pg
from osc_class import osc
from dither_class import dither
from low_pass_filter_class import low_pass_filter
from pid_controller_class import pid_controller
from awg_class import awg

class globalData():
    def __init__(self, osc=None, dither=None, filter=None, pid=None, awg=None):
        self.osc = osc
        self.dither = dither
        self.filter = filter
        self.pid = pid
        self.awg = awg

class main_screen(QMainWindow):
    def __init__(self, osc=None, dither=None, filter=None, controller=None):
        self.osc = osc
        self.dither = dither
        self.filter = filter
        self.controller = controller
        super(main_screen, self).__init__()
        loadUi('main_screen.ui', self)
        self.osc_button.clicked.connect(self.toosc)
        self.dither_button.clicked.connect(self.todither)
        self.filter_button.clicked.connect(self.tofilter)
        self.controller_button.clicked.connect(self.tocontroller)
        self.controlling_button.clicked.connect(self.tomonitor)

    def toosc(self):
        self.osc = osc_screen()
        widget.addWidget(self.osc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def todither(self):
        self.dither = dither_screen()
        widget.addWidget(self.dither)
        widget.setCurrentIndex(widget.currentIndex()+2)

    def tofilter(self):
        self.filter = low_pass_filter_screen()
        widget.addWidget(self.filter)
        widget.setCurrentIndex(widget.currentIndex()+3)

    def tocontroller(self):
        self.controller = pid_controller_screen()
        widget.addWidget(self.controller)
        widget.setCurrentIndex(widget.currentIndex()+4)

    def tomonitor(self):
        if data_collector.osc == None or data_collector.dither == None or data_collector.filter == None or data_collector.pid == None:
            self.status_label.setText('Please insert all fields first.')
        else:
            self.status_label.setText(' ')
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_Plot_window(data_collector)
            self.window.show()
            self.ui.setupUi(self.window)

class osc_screen(QMainWindow):
    def __init__(self):
        super(osc_screen, self).__init__()
        loadUi('osc_screen.ui', self)
        self.ip_ch_line.setText('[fe80:0000:0000:0000:7269:79ff:feb9:0c22%12]')
        self.in_ch_line.setText('1')
        self.timebase_line.setText('0 5e-3')
        self.status_label.setText('')
        self.status_label.setStyleSheet('color: red;')
        self.run_button.clicked.connect(self.run_function)
        self.return_button.clicked.connect(self.return_function)

    def run_function(self):
        self.status_label.setText('')
        ip_address = self.ip_ch_line.text()
        input_ch = self.in_ch_line.text()
        timebase = self.timebase_line.text()

        # Error consideration
        if len(ip_address) == 0 or len(input_ch) == 0 or len(timebase) == 0:
            self.status_label.setText('Please insert all fields first.')
        else:
            # Cast string to int and float
            input_ch = int(input_ch)
            timebase = [float(x) for x in timebase.split()]

            if timebase[0] < 0 or timebase[1] < 0:
                self.status_label.setText('Negative time values not applicable.')
            elif timebase[0] > timebase[1]:
                self.status_label.setText('Starting time value must be higher than end value.')
            else:
                print('IP address: ' + str(ip_address))
                print('Selected input channel: ' + str(input_ch))
                print('Timebase: ' + str(timebase))

                # Config oscilloscope
                self.status_label.setStyleSheet('color: green;')
                self.status_label.setText('')
                self.status_label.setText('Starting oscilloscope...')
                print('Starting oscilloscope...')
                data_collector.osc = osc(ip_address=ip_address, timebase=timebase, input_ch=input_ch)
                data_collector.osc.config()
                #data_collector.awg = awg(ip_address='[fe80:0000:0000:0000:7269:79ff:feb9:0b52%7]', output_ch=output_ch)
                print('Oscilloscope is running.')
                self.status_label.setText('Oscilloscope is running.')

    def return_function(self):
        ui = main_screen()
        widget.addWidget(ui)
        widget.setCurrentIndex(widget.currentIndex()-1)

class dither_screen(QMainWindow):
    def __init__(self):
        super(dither_screen, self).__init__()
        loadUi('dither_screen.ui', self)
        self.ip_ch_line.setText('[fe80:0000:0000:0000:7269:79ff:feb9:0b52%7]')
        self.out_ch_line.setText('1')
        self.status_label.setText('')
        self.status_label.setStyleSheet('color: red;')
        self.insert_button.clicked.connect(self.insert_function)
        self.return_button.clicked.connect(self.return_function)

    def insert_function(self):
        ip_address = self.ip_ch_line.text()
        output_ch = self.out_ch_line.text()
        dith_freq = self.dith_freq_line.text()
        theta = self.phase_diff_line.text()
        amp_dith = self.amp_dith_line.text()

        if len(ip_address) == 0 or len(output_ch) == 0 or len(dith_freq) == 0 or len(theta) == 0 or len(amp_dith) == 0:
            self.status_label.setText('Please insert all fields first.')
        else:
            data_collector.dither = dither(ip_address=ip_address, output_ch = int(output_ch), dith_freq=float(dith_freq), theta=float(theta), amp_dith=float(amp_dith))
            data_collector.dither.generate()
            self.status_label.setStyleSheet('color: green;')
            self.status_label.setText('Waveform-Generator is running.')
            print('IP address: ' + str(ip_address))
            print('Selected output channel: ' + str(output_ch))
            print('Dither frequency: ' + str(dith_freq))
            print('Phase difference: ' + str(theta))
            print('Amplitude dither signal: ' + str(amp_dith))

    def return_function(self):
        ui = main_screen()
        widget.addWidget(ui)
        widget.setCurrentIndex(widget.currentIndex()-2)

class low_pass_filter_screen(QMainWindow):
    def __init__(self):
        super(low_pass_filter_screen, self).__init__()
        loadUi('low_pass_filter_screen.ui', self)
        window_list = [self.bode_diagram_amp, self.bode_diagram_phase]
        title_list = ['Amplitude response', 'Phase response']
        ylabel_list = ['Gain [dB]', 'Phase [rad]']
        for n, window in enumerate(window_list):
            window.setBackground('w')
            window.showGrid(x =True, y=True)
            window.setTitle(title_list[n])
            window.setLabel(axis='bottom', text='Frequency [MHz]')
            window.setLabel(axis='left', text=ylabel_list[n])
            self.insert_button.clicked.connect(self.insert_function)
            self.return_button.clicked.connect(self.return_function)

    def insert_function(self):
        if data_collector.osc == None:
            self.error_label.setText('Please start oscilloscpe first\nto determine sample frequency')
        else:
            if not self.FIR_checkbox.isChecked() and not self.Butterworth_checkbox.isChecked() and not self.Chebyshev1_checkbox.isChecked() and not self.Elliptic_checkbox.isChecked():
                self.error_label.setText('Please choose filter type.')
            else:
                self.error_label.setText('')
                num_coeff = self.num_coeff_line.text()
                cutoff = self.cut_off_fre_line.text()

                if self.FIR_checkbox.isChecked() or self.Butterworth_checkbox.isChecked():
                    if self.FIR_checkbox.isChecked():
                        filtertype = 'FIR'
                    else:
                        filtertype = 'butter'
                    if len(num_coeff) == 0 or len(cutoff) == 0:
                        self.error_label.setText('Please insert all fields.')
                    elif filtertype == 'FIR' and int(num_coeff) > 2000:
                        self.error_label.setText('Please reduce filter order.')
                    elif filtertype == 'butter' and int(num_coeff) > 60:
                        self.error_label.setText('Please reduce filter order.')
                    elif float(cutoff) > data_collector.osc.obj.get_samplerate()['sample_rate']/2:
                        self.error_label.setText('Cut-off frequency must be lower than \n' + str(int(data_collector.osc.obj.get_samplerate()['sample_rate']/2)/1e6) + ' MHz')
                    else:
                        # Store data
                        data_collector.filter = low_pass_filter(num_coeff=int(num_coeff), cutoff=float(cutoff), filtertype=filtertype, fs=data_collector.osc.obj.get_samplerate()['sample_rate'])
                        print('Number of filter coefficients: ' + str(data_collector.filter.num_coeff))
                        print('Cut-off frequency: ' + str(data_collector.filter.cutoff))
                        # Plot bode diagram
                        b, a = data_collector.filter.get_coefficients()
                        self.plot_bode(b, a)

                if self.Chebyshev1_checkbox.isChecked():
                    filtertype = 'cheby1'
                    max_ripple = self.max_ripple_line.text()
                    if len(num_coeff) == 0 or len(cutoff) == 0 or len(max_ripple) == 0:
                        self.error_label.setText('Please insert all fields.')
                    elif int(num_coeff) > 60:
                        self.error_label.setText('Please reduce filter order.')
                    elif float(cutoff) > data_collector.osc.obj.get_samplerate()['sample_rate']/2:
                        self.error_label.setText('Cut-off frequency must be lower than \n' + str(int(data_collector.osc.obj.get_samplerate()['sample_rate']/2)/1e6) + ' MHz')
                    else:
                        # Store data
                        data_collector.filter = low_pass_filter(num_coeff=int(num_coeff), cutoff=float(cutoff), filtertype=filtertype, fs=data_collector.osc.obj.get_samplerate()['sample_rate'], max_ripple=float(max_ripple))
                        print('Number of filter coefficients: ' + str(data_collector.filter.num_coeff))
                        print('Cut-off frequency: ' + str(data_collector.filter.cutoff))
                        print('Max. ripple: ' + str(data_collector.filter.max_ripple))
                        # Plot bode diagram
                        b, a = data_collector.filter.get_coefficients()
                        self.plot_bode(b, a)
                
                if self.Elliptic_checkbox.isChecked():
                    filtertype = 'elliptic'
                    max_ripple = self.max_ripple_line.text()
                    min_attenuation = self.min_attenuation_line.text()
                    if len(num_coeff) == 0 or len(cutoff) == 0 or len(max_ripple) == 0 or len(min_attenuation) == 0:
                        self.error_label.setText('Please insert all fields.')
                    elif int(num_coeff) > 60:
                        self.error_label.setText('Please reduce filter order.')
                    elif float(cutoff) > data_collector.osc.obj.get_samplerate()['sample_rate']/2:
                        self.error_label.setText('Cut-off frequency must be lower than \n' + str(int(data_collector.osc.obj.get_samplerate()['sample_rate']/2)/1e6) + ' MHz')
                    elif float(max_ripple) > float(min_attenuation):
                        self.error_label.setText('Max. ripple must be lower than\n min. attenuation.')
                    else:
                        # Cast to int and float and store data
                        data_collector.filter = low_pass_filter(num_coeff=int(num_coeff), cutoff=float(cutoff), filtertype=filtertype, fs=data_collector.osc.obj.get_samplerate()['sample_rate'], max_ripple=float(max_ripple), min_attenuation=float(min_attenuation))
                        print('Number of filter coefficients: ' + str(data_collector.filter.num_coeff))
                        print('Cut-off frequency: ' + str(data_collector.filter.cutoff))
                        print('Max. ripple: ' + str(data_collector.filter.max_ripple))
                        print('Min. attenuation: ' + str(data_collector.filter.min_attenuation))
                        # Plot bode diagram
                        b, a = data_collector.filter.get_coefficients()
                        self.plot_bode(b, a)

    def plot_bode(self, b, a):
        fs = data_collector.osc.obj.get_samplerate()['sample_rate']
        w, h = signal.freqz(b,a)
        f = w/np.pi*fs/2
        pen=pg.mkPen(color=(148, 0, 211), width=2)
        self.bode_diagram_amp.clear()
        self.bode_diagram_phase.clear()
        self.bode_diagram_amp.plot(f/1e6, 20*np.log10(np.abs(h)), pen=pen) # in MHz and dB
        self.bode_diagram_phase.plot(f/1e6, np.angle(h), pen=pen) # in MHz and rad

    def return_function(self):
        ui = main_screen()
        widget.addWidget(ui)
        widget.setCurrentIndex(widget.currentIndex()-3)

class pid_controller_screen(QMainWindow):
    def __init__(self):
        super(pid_controller_screen, self).__init__()
        loadUi('pid_controller_screen.ui', self)
        self.insert_button.clicked.connect(self.insert_function)
        self.return_button.clicked.connect(self.return_function)

    def insert_function(self):
        Kp = self.p_factor_line.text()
        Ki = self.i_factor_line.text()
        Kd = self.d_factor_line.text()
        setpoint = self.setpoint_line.text()

        if len(Kp) == 0 or len(Ki) == 0 or len(Kd) == 0 or len(setpoint) == 0:
            self.error_label.setText('Please insert all fields.')

        else:
            # Store data
            data_collector.pid = pid_controller(Kp=float(Kp), Ki=float(Ki), Kd=float(Kd), setpoint=float(setpoint), dith_freq=data_collector.dither.dith_freq, amp_dith=data_collector.dither.amp_dith)
            print('P-factor: ' + str(data_collector.pid.Kp))
            print('I-factor: ' + str(data_collector.pid.Ki))
            print('D-factor: ' + str(data_collector.pid.Kd))
            print('Setpoint: ' + str(data_collector.pid.setpoint))

            ui = main_screen()
            widget.addWidget(ui)
            widget.setCurrentIndex(widget.currentIndex()-4)

    def return_function(self):
        ui = main_screen()
        widget.addWidget(ui)
        widget.setCurrentIndex(widget.currentIndex()-4)

## main
# Config UI
data_collector = globalData()
app = QApplication(sys.argv)
osc_s = osc_screen()
dither_s = dither_screen()
filter_s = low_pass_filter_screen()
controller_s = pid_controller_screen()
ui_s = main_screen(osc_s, dither_s, filter_s, controller_s)
widget = QtWidgets.QStackedWidget()
widget.addWidget(ui_s)
widget.addWidget(osc_s)
widget.addWidget(dither_s)
widget.addWidget(filter_s)
widget.addWidget(controller_s)
widget.setFixedHeight(601)
widget.setFixedWidth(801)
widget.show()

# Run UI
try:
    sys.exit(app.exec_())
except:
    print('Exiting application')
