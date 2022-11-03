
from moku.instruments import Oscilloscope
import pandas as pd
import numpy as np

class osc():
    def __init__(self, ip_address, timebase, input_ch, output_ch, dith_freq, theta):
        self.ip_address = ip_address
        self.timebase = timebase
        self.input_ch = input_ch
        self.output_ch = output_ch
        self.dith_freq = dith_freq
        self.theta = theta
        self.fs = 8928571.42857143 # in Hz
        self.obj = Oscilloscope(self.ip_address, force_connect = True)
        self.osc_input_collector = []

    def config(self):
        # Trigger on input Channel 1, rising edge, 0V 
        self.obj.set_trigger(type='Edge', source='Input1', level=0)
        # View +-5usec, i.e. trigger in the centre
        self.obj.set_timebase(self.timebase[0], self.timebase[1])
        # Generate an output ramp wave on Channel 1, 1Vpp, 10000Hz, 0V offset
        # osc.generate_waveform(channel=1, type='Ramp', amplitude=1, frequency=10000, duty=0.9, symmetry=0.5, edge_time=0.5)
        self.obj.generate_waveform(channel=2, type='Sine', amplitude=2.5, frequency=self.dith_freq, phase=self.theta, offset=2.5)
        # Generate dither signal for on channel 2 and measure input signal on channel 1
        self.obj.set_source(self.output_ch, 'Output1') # loop back output
        # self.obj.set_source(self.input_ch, 'Input1')

    def get_one_ch_data(self):
        data = self.obj.get_data()
        if self.input_ch:
            signal_df = pd.DataFrame(data).iloc[:,[0,1]]
            signal_df = signal_df.rename({'ch1': 'ch'}, axis=1)
        elif self.input_ch == 2:
            signal_df = pd.DataFrame(data).iloc[:,[0,2]]
            signal_df = signal_df.rename({'ch2': 'ch'}, axis=1)
        
        return signal_df

    def get_osc_input(self, append):
        fs = self.fs

        osc_input_df = self.get_one_ch_data()
        if append == True:
            data = osc_input_df['ch'].values.tolist()
            for item in data:
                self.osc_input_collector.append(item)

            osc_input = np.reshape(np.array(self.osc_input_collector), (-1,1))
            n_axis = np.arange(np.shape(osc_input)[0])
            t_axis = np.reshape(n_axis/fs, (-1,1)) # in s
            osc_input = np.concatenate((t_axis, osc_input), axis=1)
            osc_input_df = pd.DataFrame(osc_input, columns=['time', 'ch'])

        return osc_input_df

    def clear_collector(self):
        self.osc_input_collector = []