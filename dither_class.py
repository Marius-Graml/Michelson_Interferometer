
import numpy as np
import pandas as pd

class dither():
    def __init__(self, dith_freq, theta, amp_dith):
        self.dith_freq = dith_freq
        self.theta = theta
        self.amp_dith = amp_dith

    def demodulate(self, input_signal_df):
        t = np.array(input_signal_df['time'])
        input_signal = np.array(input_signal_df.iloc[:,1])

        demod_signal = input_signal*np.sin(2*np.pi*self.dith_freq*t + self.theta)

        demod_signal = np.concatenate((np.reshape(t, (-1,1)), np.reshape(demod_signal, (-1,1))), axis=1)

        return pd.DataFrame(demod_signal, columns=['time', 'ch'])