
import numpy as np
import pandas as pd
from moku.instruments import WaveformGenerator

class dither():
    def __init__(self, ip_address, output_ch, dith_freq, theta, amp_dith):
        self.output_ch = output_ch
        self.dith_freq = dith_freq
        self.theta = theta
        self.amp_dith = amp_dith
        self.obj = WaveformGenerator(ip_address, force_connect=True)

    def generate(self):
        self.obj.generate_waveform(channel=1, type='Sine', amplitude=0.5*self.amp_dith, frequency=self.dith_freq, offset=0, phase=self.theta)

    def demodulate(self, input_signal_df):
        t = np.array(input_signal_df['time'])
        input_signal = np.array(input_signal_df.iloc[:,1])

        demod_signal = input_signal*np.sin(2*np.pi*self.dith_freq*t + self.theta)

        demod_signal = np.concatenate((np.reshape(t, (-1,1)), np.reshape(demod_signal, (-1,1))), axis=1)
        output = pd.DataFrame(demod_signal, columns=['time', 'ch'])
        return output