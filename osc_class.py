
from moku.instruments import Oscilloscope
import pandas as pd
import numpy as np
from scipy import signal

class osc():
    def __init__(self, ip_address, timebase, input_ch, output_ch):
        self.ip_address = ip_address
        self.timebase = timebase
        self.input_ch = input_ch
        self.output_ch = output_ch
        #8928571.42857143 # in Hz
        self.obj = Oscilloscope(self.ip_address, force_connect = True)
        t = self.obj.get_data()['time']
        self.fs = 1/(t[1] - t[0])
        self.osc_input_collector = []
        self.signal = None
        self.c = 0

    def config(self):
        # Trigger on input Channel 1, auto, 0V 
        self.obj.set_trigger(mode='Auto', level=0, source='Input1')
        # Set timebase
        self.obj.set_timebase(self.timebase[0], self.timebase[1])
        # Generate an output ramp wave on Channel 1, 1Vpp, 10000Hz, 0V offset
        # osc.generate_waveform(channel=1, type='Ramp', amplitude=1, frequency=10000, duty=0.9, symmetry=0.5, edge_time=0.5)
        # self.obj.generate_waveform(channel=2, type='Sine', amplitude=2.5, frequency=self.dith_freq, phase=self.theta, offset=2.5)
        # Generate dither signal for on channel 2 and measure input signal on channel 1
        # self.obj.set_source(self.output_ch, 'Output1') # loop back output
        self.obj.set_source(self.input_ch, 'Input1')
        self.obj.set_interpolation(interpolation='Gaussian')

    def get_osc_input(self, append, dith_freq, filtered):
        output = self.get_one_ch_data() 
        data = output['ch'].values.tolist()
        for item in data:
            self.osc_input_collector.append(item)
        if len(self.osc_input_collector) <= 30720:
            osc_input = np.reshape(np.array(self.osc_input_collector), (-1,1))
            n_axis = np.arange(len(self.osc_input_collector))
            t_axis = np.reshape(n_axis/self.fs, (-1,1)) # in s
        elif len(self.osc_input_collector) > 30720:
            del self.osc_input_collector[0:1024]
            osc_input = np.reshape(np.array(self.osc_input_collector), (-1,1))
            self.c = self.c+1
            n_start = self.c*1024
            n_axis = np.arange(n_start, n_start+30720)
            t_axis = np.reshape(n_axis/self.fs, (-1,1)) # in s
        print(len(self.osc_input_collector))
        osc_input = np.concatenate((t_axis, osc_input), axis=1)
        output = pd.DataFrame(osc_input, columns=['time', 'ch'])
        if filtered:
            myfilter = signal.firwin(1000, dith_freq*2, fs=self.fs)
            output['ch'] = signal.lfilter(myfilter, [1.0], output['ch'])
        # Get mean of input
        sig_mean = np.mean(output['ch'][-1024:]) * np.ones((1024, 1))
        sig_mean = np.concatenate((np.reshape(np.array(output['time'].iloc[-1024:]), (-1,1)), sig_mean), axis=1)
        sig_mean = pd.DataFrame(sig_mean, columns=['time', 'ch'])
        if append == False:
            output_short = output.iloc[-1024:, :]
            output_short = output_short.reset_index(drop=True, inplace=False)
            return output_short, sig_mean
        else:
            return output, sig_mean

    def get_one_ch_data(self):
        data = self.obj.get_data(timeout=0.1)
        self.fs = 1/(data['time'][1] - data['time'][0])
        if self.input_ch:
            signal_df = pd.DataFrame(data).iloc[:,[0,1]]
            signal_df = signal_df.rename({'ch1': 'ch'}, axis=1)
        elif self.input_ch == 2:
            signal_df = pd.DataFrame(data).iloc[:,[0,2]]
            signal_df = signal_df.rename({'ch2': 'ch'}, axis=1)
        
        return signal_df

    def clear_collector(self):
        self.osc_input_collector.clear()

    def stop(self):
        self.obj.disable_input(channel=self.input_ch)