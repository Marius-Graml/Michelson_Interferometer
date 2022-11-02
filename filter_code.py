
from scipy import signal
import pandas as pd
import numpy as np

def fir_low_pass(x, num_coeff, cutoff, max_ripple, min_attenuation, fs, filtertype):

    # Input signal as dictionary or dataframe
    x_df = pd.DataFrame(x)
    x_ch = np.array(x_df['ch'])

    # Params
    # x: input signal
    # num_coeff: number of transversal coefficients
    # cutoff: Cut-off frequency of low pass filter
    # fs: Sampling rate
    if filtertype == 'FIR':
        myfilter = signal.firwin(num_coeff, cutoff, fs=fs)
    elif filtertype == 'butter':
        myfilter = signal.butter(num_coeff, cutoff, fs=fs)
    elif filtertype == 'cheby':
        myfilter = signal.cheby1(N=num_coeff, rp=max_ripple, Wn=cutoff, fs=fs)
    elif filtertype == 'elliptic':
        myfilter = signal.ellip(N=num_coeff, rp=max_ripple, rs=min_attenuation, Wn=cutoff, fs=fs)

    # Filter signal
    if filtertype == 'FIR':
        y_filtered_ch = signal.lfilter(myfilter, [1.0], x_ch)
    else:
        y_filtered_ch = signal.lfilter(myfilter[0], myfilter[1], x_ch)

    # Output signal as pandas dataframe with time axis
    n_axis = np.arange(np.shape(y_filtered_ch)[0])
    t_axis = n_axis/fs

    data_y = np.concatenate((np.reshape(t_axis, (-1,1)), np.reshape(y_filtered_ch, (-1,1))), axis = 1)
    y_df = pd.DataFrame(data_y, columns=['time', 'ch'])

    return y_df