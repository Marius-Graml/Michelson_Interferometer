
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from simple_pid import PID
from moku.instruments import Oscilloscope
from monitor_screen import Ui_Plot_window
from scipy import signal
import numpy as np
import pyqtgraph as pg

class globalData():
    def __init__(self, osc_moku=None, input_ch_number=None, timebase=None, dith_freq=None, theta=None, num_coeff=None, cutoff=None, Kp=None, Ki=None, Kd=None, pid=None, max_ripple=None, min_attenuation=None, filtertype=None, fs=8928571.42857143):
        self.osc_moku = osc_moku
        self.input_ch_number = input_ch_number
        self.timebase = timebase
        self.dith_freq = dith_freq
        self.theta = theta
        self.num_coeff = num_coeff
        self.cutoff = cutoff
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.pid = pid
        self.max_ripple = max_ripple
        self.min_attenuation = min_attenuation
        self.filtertype = filtertype
        self.fs = fs
class main_screen(QMainWindow):
    def __init__(self, osc=None, demodulation=None, filter=None, controller=None):
        self.osc = osc
        self.demodulation = demodulation
        self.filter = filter
        self.controller = controller
        super(main_screen, self).__init__()
        loadUi('main_screen.ui', self)
        self.osc_button.clicked.connect(self.toosc)
        self.demod_button.clicked.connect(self.todemod)
        self.filter_button.clicked.connect(self.tofilter)
        self.controller_button.clicked.connect(self.tocontroller)
        self.monitor_button.clicked.connect(self.tomonitor)

    def toosc(self):
        self.osc = osc_screen()
        widget.addWidget(self.osc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def todemod(self):
        self.demodulation = demod_screen()
        widget.addWidget(self.demodulation)
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
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Plot_window(data_collector)
        self.window.show()
        self.ui.setupUi(self.window)

class osc_screen(QMainWindow):
    def __init__(self):
        super(osc_screen, self).__init__()
        loadUi('osc_screen.ui', self)
        self.in_ch_line.setText('1')
        self.timebase_line.setText('0 1e-4')
        self.osc_running_label.setText('')
        self.insert_button.clicked.connect(self.insert_function)
        self.return_button.clicked.connect(self.return_function)

    def osc_config(self, ip_address):
        ## Oscilloscope config
        osc = Oscilloscope(ip_address, force_connect = True)
        # Trigger on input Channel 1, rising edge, 0V 
        osc.set_trigger(type='Edge', source='Input1', level=0)
        # View +-5usec, i.e. trigger in the centre
        osc.set_timebase(data_collector.timebase[0], data_collector.timebase[1])
        # Generate an output ramp wave on Channel 1, 1Vpp, 10000Hz, 0V offset
        # osc.generate_waveform(channel=1, type='Ramp', amplitude=1, frequency=10000, duty=0.9, symmetry=0.5, edge_time=0.5)
        osc.generate_waveform(channel=1, type='Sine', amplitude=2.5, frequency=data_collector.dith_freq, phase=0, offset=2.5)
        # Set the data source of Channel 1 to be Input 1
        osc.set_source(data_collector.input_ch_number, 'Output1')
        # osc.set_source(data_collector.input_ch_number, 'Input1')
        return osc

    def insert_function(self):
        input_ch_number_tmp = self.in_ch_line.text()
        timebase_tmp = self.timebase_line.text()

        # Cast string to int and float
        input_ch_number_tmp = int(input_ch_number_tmp)
        timebase_tmp = [float(x) for x in timebase_tmp.split()]
        if timebase_tmp[0] < 0 or timebase_tmp[1] < 0:
            self.timebase_label.setText('Negative time values not applicable.')
        elif timebase_tmp[0] > timebase_tmp[1]:
            self.timebase_label.setText('Starting value must be higher than end value.')
        else:
            # Store data
            data_collector.input_ch_number = input_ch_number_tmp
            data_collector.timebase = timebase_tmp
            print('Selected input channel: ' + str(data_collector.input_ch_number))
            print('Timebase: ' + str(data_collector.timebase))

            # Config oscilloscope
            if data_collector.dith_freq == None:
                self.osc_running_label.setStyleSheet('color: red;')
                self.osc_running_label.setText('Please insert dither frequency first.')
            else:
                self.osc_running_label.setStyleSheet('color: green;')
                self.osc_running_label.setText('Starting oscilloscope...')
                print('Starting oscilloscope...')
                data_collector.osc_moku = self.osc_config('[fe80:0000:0000:0000:7269:79ff:feb9:0c22%10]')
                print('Oscilloscope is running.')
                self.osc_running_label.setStyleSheet('color: green;')
                self.osc_running_label.setText('Oscilloscope is running.')

    def return_function(self):
        ui = main_screen()
        widget.addWidget(ui)
        widget.setCurrentIndex(widget.currentIndex()-1)

class demod_screen(QMainWindow):
    def __init__(self):
        super(demod_screen, self).__init__()
        loadUi('demodulation_screen.ui', self)
        self.insert_button.clicked.connect(self.insert_function)
        self.return_button.clicked.connect(self.return_function)

    def insert_function(self):
        demod_freq_tmp = self.dith_fre_line.text()
        theta_tmp = self.phase_diff_line.text()

        if len(demod_freq_tmp) == 0 or len(theta_tmp) == 0:
            self.error_label.setText('Please insert all fields.')

        else:
            # Cast to float and store data
            data_collector.dith_freq = float(demod_freq_tmp)
            data_collector.theta = float(theta_tmp)
            print('Dither frequency: ' + str(data_collector.dith_freq))
            print('Phase difference: ' + str(data_collector.theta))
            ui = main_screen()
            widget.addWidget(ui)
            widget.setCurrentIndex(widget.currentIndex()-2)

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
        if not self.FIR_checkbox.isChecked() and not self.Butterworth_checkbox.isChecked() and not self.Chebyshev1_checkbox.isChecked() and not self.Elliptic_checkbox.isChecked():
            self.error_label.setText('Please choose filter type.')
        else:
            self.error_label.setText('')
            num_coeff_tmp = self.num_coeff_line.text()
            cutoff_tmp = self.cut_off_fre_line.text()

            if self.FIR_checkbox.isChecked() or self.Butterworth_checkbox.isChecked():
                if self.FIR_checkbox.isChecked():
                    data_collector.filtertype = 'FIR'
                else:
                    data_collector.filtertype = 'butter'
                if len(num_coeff_tmp) == 0 or len(cutoff_tmp) == 0:
                    self.error_label.setText('Please insert all fields.')
                elif float(cutoff_tmp) > data_collector.fs/2:
                    self.error_label.setText('Cut-off frequency must be lower than \n' + str(int(data_collector.fs/2)/1e6) + ' MHz')
                else:
                    # Cast to int and float and store data
                    data_collector.num_coeff = int(num_coeff_tmp)
                    data_collector.cutoff = float(cutoff_tmp)
                    print('Number of filter coefficients: ' + str(data_collector.num_coeff))
                    print('Cut-off frequency: ' + str(data_collector.cutoff))
                    # Plot bode diagram
                    self.plot_bode()

            if self.Chebyshev1_checkbox.isChecked():
                data_collector.filtertype = 'cheby'
                max_ripple_tmp = self.max_ripple_line.text()
                if len(num_coeff_tmp) == 0 or len(cutoff_tmp) == 0 or len(max_ripple_tmp) == 0:
                    self.error_label.setText('Please insert all fields.')
                elif float(cutoff_tmp) > data_collector.fs/2:
                    self.error_label.setText('Cut-off frequency must be lower than \n' + str(int(data_collector.fs/2)/1e6) + ' MHz')
                else:
                    # Cast to int and float and store data
                    data_collector.num_coeff = int(num_coeff_tmp)
                    data_collector.cutoff = float(cutoff_tmp)
                    data_collector.max_ripple = float(max_ripple_tmp)
                    print('Number of filter coefficients: ' + str(data_collector.num_coeff))
                    print('Cut-off frequency: ' + str(data_collector.cutoff))
                    print('Max. ripple: ' + str(data_collector.max_ripple))
                    # Plot bode diagram
                    self.plot_bode()
            
            if self.Elliptic_checkbox.isChecked():
                data_collector.filtertype = 'elliptic'
                max_ripple_tmp = self.max_ripple_line.text()
                min_attenuation_tmp = self.min_attenuation_line.text()
                if len(num_coeff_tmp) == 0 or len(cutoff_tmp) == 0 or len(max_ripple_tmp) == 0 or len(min_attenuation_tmp) == 0:
                    self.error_label.setText('Please insert all fields.')
                elif float(cutoff_tmp) > data_collector.fs/2:
                    self.error_label.setText('Cut-off frequency must be lower than \n' + str(int(data_collector.fs/2)/1e6) + ' MHz')
                elif max_ripple_tmp > min_attenuation_tmp:
                    self.error_label.setText('Max. ripple must be lower than min. attenuation.')
                else:
                    # Cast to int and float and store data
                    data_collector.num_coeff = int(num_coeff_tmp)
                    data_collector.cutoff = float(cutoff_tmp)
                    data_collector.max_ripple = float(max_ripple_tmp)
                    data_collector.min_attenuation = float(min_attenuation_tmp)
                    print('Number of filter coefficients: ' + str(data_collector.num_coeff))
                    print('Cut-off frequency: ' + str(data_collector.cutoff))
                    print('Max. ripple: ' + str(data_collector.max_ripple))
                    print('Min. attenuation: ' + str(data_collector.min_attenuation))
                    # Plot bode diagram
                    self.plot_bode()

    def plot_bode(self):
        fs = data_collector.fs
        if self.FIR_checkbox.isChecked():
            b = signal.firwin(data_collector.num_coeff, data_collector.cutoff, fs=fs)
            a=1
            w, h = signal.freqz(b,a)
        elif self.Butterworth_checkbox.isChecked():
            b, a = signal.butter(N=data_collector.num_coeff, Wn = data_collector.cutoff, btype='low', analog=False, fs=fs)
            w, h = signal.freqz(b,a)
        elif self.Chebyshev1_checkbox.isChecked():
            b, a = signal.cheby1(N=data_collector.num_coeff, rp=data_collector.max_ripple, Wn = data_collector.cutoff, btype='low', analog=False, fs=fs)
            w, h = signal.freqz(b,a)
        elif self.Elliptic_checkbox.isChecked():
            b, a = signal.ellip(N=data_collector.num_coeff, rp=data_collector.max_ripple, rs=data_collector.min_attenuation, Wn = data_collector.cutoff, fs=fs)
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

    def pid_config(self):
        return PID(data_collector.Kp, data_collector.Ki, data_collector.Kd, setpoint=0)

    def insert_function(self):
        Kp_tmp = self.p_factor_line.text()
        Ki_tmp = self.i_factor_line.text()
        Kd_tmp = self.d_factor_line.text()

        if len(Kp_tmp) == 0 or len(Ki_tmp) == 0 or len(Kd_tmp) == 0:
            self.error_label.setText('Please insert all fields.')

        else:
            # Cast to float and store data
            data_collector.Kp = float(Kp_tmp)
            data_collector.Ki = float(Ki_tmp)
            data_collector.Kd = float(Kd_tmp)
            print('P-factor: ' + str(data_collector.Kp))
            print('I-factor: ' + str(data_collector.Ki))
            print('D-factor: ' + str(data_collector.Kd))

            # Config PID controller
            data_collector.pid = self.pid_config()

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
demod_s = demod_screen()
filter_s = low_pass_filter_screen()
controller_s = pid_controller_screen()
ui_s = main_screen(osc_s, demod_s, filter_s, controller_s)
widget = QtWidgets.QStackedWidget()
widget.addWidget(ui_s)
widget.addWidget(osc_s)
widget.addWidget(demod_s)
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
