
import numpy as np
import pandas as pd

def demodulate(input_signal_df, w_dith, theta):
    t = np.array(input_signal_df['time'])
    input_signal = np.array(input_signal_df.iloc[:,1])

    demod_signal = input_signal*np.sin(w_dith*t + theta)

    demod_signal = np.concatenate((np.reshape(t, (-1,1)), np.reshape(demod_signal, (-1,1))), axis=1)

    return pd.DataFrame(demod_signal, columns=['time', 'ch'])