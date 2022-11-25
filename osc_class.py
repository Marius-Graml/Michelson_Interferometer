
from moku.instruments import Oscilloscope
import pandas as pd
import numpy as np

class osc():
    def __init__(self, ip_address, timebase, input_ch, output_ch):
        self.ip_address = ip_address
        self.timebase = timebase
        self.input_ch = input_ch
        self.output_ch = output_ch
        self.obj = Oscilloscope(self.ip_address, force_connect = True)
        t = self.obj.get_data()['time']
        self.fs = 1/(t[1] - t[0])
        self.osc_input_collector = []
        self.signal = None

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

    def get_osc_input(self, append):
        output = self.get_one_ch_data() 
        if append == True:
            data = output['ch'].values.tolist()
            for item in data:
                self.osc_input_collector.append(item)
            osc_input = np.reshape(np.array(self.osc_input_collector), (-1,1))
            n_axis = np.arange(np.shape(osc_input)[0])
            t_axis = np.reshape(n_axis/self.fs, (-1,1)) # in s
            osc_input = np.concatenate((t_axis, osc_input), axis=1)
            output = pd.DataFrame(osc_input, columns=['time', 'ch'])

        return output

    def get_one_ch_data(self):
        data = self.obj.get_data()
        self.fs = 1/(data['time'][1] - data['time'][0])
        if self.input_ch:
            signal_df = pd.DataFrame(data).iloc[:,[0,1]]
            signal_df = signal_df.rename({'ch1': 'ch'}, axis=1)
        elif self.input_ch == 2:
            signal_df = pd.DataFrame(data).iloc[:,[0,2]]
            signal_df = signal_df.rename({'ch2': 'ch'}, axis=1)
        
        return signal_df

    def clear_collector(self):
        self.osc_input_collector = []

    def stop(self):
        self.obj.disable_input(channel=self.input_ch)