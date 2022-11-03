
from scipy import signal
import pandas as pd
import numpy as np

class low_pass_filter():
    def __init__(self, num_coeff, cutoff, filtertype, max_ripple=None, min_attenuation=None, fs=8928571.42857143):
        self.num_coeff = num_coeff
        self.cutoff = cutoff
        self.filtertype = filtertype
        self.max_ripple = max_ripple
        self.min_attenuation = min_attenuation
        self.fs = fs

    def apply(self, input_signal):

        # Input signal as dictionary or dataframe
        x_df = pd.DataFrame(input_signal)
        x = np.array(x_df['ch'])

        # Generate filter
        if self.filtertype == 'FIR':
            myfilter = signal.firwin(self.num_coeff, self.cutoff, fs=self.fs)
        elif self.filtertype == 'butter':
            myfilter = signal.butter(self.num_coeff, self.cutoff, fs=self.fs)
        elif self.filtertype == 'cheby1':
            myfilter = signal.cheby1(N=self.num_coeff, rp=self.max_ripple, Wn=self.cutoff, fs=self.fs)
        elif self.filtertype == 'elliptic':
            myfilter = signal.ellip(N=self.num_coeff, rp=self.max_ripple, rs=self.min_attenuation, Wn=self.cutoff, fs=self.fs)

        # Filtering signal
        if self.filtertype == 'FIR':
            y_filtered = signal.lfilter(myfilter, [1.0], x)
        else:
            y_filtered = signal.lfilter(myfilter[0], myfilter[1], x)

        # Output signal as pandas dataframe with time axis
        n_axis = np.arange(np.shape(y_filtered)[0])
        t_axis = n_axis/self.fs

        y = np.concatenate((np.reshape(t_axis, (-1,1)), np.reshape(y_filtered, (-1,1))), axis = 1)
        output_signal_df = pd.DataFrame(y, columns=['time', 'ch'])

        return output_signal_df

    def get_coefficients(self):
        if self.filtertype == 'FIR':
            b = signal.firwin(self.num_coeff, self.cutoff, fs=self.fs)
            a=1
        elif self.filtertype == 'butter':
            b, a = signal.butter(N=self.num_coeff, Wn = self.cutoff, btype='low', analog=False, fs=self.fs)
        elif self.filtertype == 'cheby1':
            b, a = signal.cheby1(N=self.num_coeff, rp=self.max_ripple, Wn = self.cutoff, btype='low', analog=False, fs=self.fs)
        elif self.filtertype == 'elliptic':
            b, a = signal.ellip(N=self.num_coeff, rp=self.max_ripple, rs=self.min_attenuation, Wn = self.cutoff, fs=self.fs)
        return b, a