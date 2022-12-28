
from moku.instruments import Oscilloscope
import pandas as pd
import numpy as np
from scipy import signal

class osc():
    def __init__(self, ip_address, timebase, input_ch):
        self.ip_address = ip_address
        self.timebase = timebase
        self.input_ch = input_ch
        #8928571.42857143 # in Hz
        self.obj = Oscilloscope(self.ip_address, force_connect = True)
        #t = self.obj.get_data()['time']
        #self.fs = 1/(t[1] - t[0])
        self.osc_input_collector = []
        self.osc_time_collector = []
        self.c = 0

    def config(self):
        # Trigger on input Channel 1, auto, 0V 
        self.obj.set_trigger(mode='Auto', level=0, source='Input1')
        # Set timebase
        self.obj.set_timebase(self.timebase[0], self.timebase[1])
        # Set acquisition mode 
        self.obj.set_acquisition_mode(mode="Precision")
        # Set source
        self.obj.set_source(self.input_ch, 'Input1')
        # Enable rollmode
        self.obj.enable_rollmode(roll=False)

    def get_osc_input(self, append, dith_freq, filtered):
        output = self.get_one_ch_data()
        data = output['ch'].values.tolist()
        for item in data:
            self.osc_input_collector.append(item)
    # if len(self.osc_input_collector) <= 30720:
        if len(self.osc_input_collector) > 30720:
            del self.osc_input_collector[0:1024]
            del self.osc_time_collector[0:1024]
        osc_input = np.reshape(np.array(self.osc_input_collector), (-1,1))
        self.c = self.c+1
        n_start = self.c*1024
        n_axis_new = np.arange(n_start, n_start+1024)
        print(np.shape(n_axis_new))
        #n_axis = np.arange(len(self.osc_input_collector))
        print(self.obj.get_samplerate()['sample_rate'])
        t_axis_new = np.reshape(n_axis_new/self.obj.get_samplerate()['sample_rate'], (-1,1)) # in s
        print(np.shape(t_axis_new))
        for item in t_axis_new:
            self.osc_time_collector.append(item)
        print(len(self.osc_time_collector))
        t_axis = np.reshape(np.array(self.osc_time_collector), (-1,1))
        print(np.shape(t_axis))
        #t_axis = np.reshape(n_axis/self.obj.get_samplerate()['sample_rate'], (-1,1)) # in s
        # osc_input = np.reshape(np.array(self.osc_input_collector), (-1,1))
        # self.c = self.c+1
        # n_start = self.c*1024
        # n_axis = np.arange(n_start, n_start+30720)
        # t_axis = np.reshape(n_axis/self.obj.get_samplerate()['sample_rate'], (-1,1)) # in s
        print(len(self.osc_input_collector))
        print(np.shape(t_axis))
        print(np.shape(osc_input))
        osc_input = np.concatenate((t_axis, osc_input), axis=1)
        output = pd.DataFrame(osc_input, columns=['time', 'ch'])
        if filtered:
            myfilter = signal.firwin(1000, dith_freq*2, fs=self.obj.get_samplerate()['sample_rate'])
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
        self.osc_input_collector.clear()
        self.osc_time_collector.clear()

    def stop(self):
        self.obj.disable_input(channel=self.input_ch)