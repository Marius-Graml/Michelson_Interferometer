
import numpy as np
import pandas as pd

def demodulate(dith_signal_df, w_dith, theta):
    t = np.array(dith_signal_df['time'])
    dith_signal_np = np.array(dith_signal_df.iloc[:,1])

    demod_signal = dith_signal_np*np.sin(w_dith*t + theta)

    demod_signal = np.concatenate((np.reshape(t, (-1,1)), np.reshape(demod_signal, (-1,1))), axis=1)

    return pd.DataFrame(demod_signal, columns=['time', 'ch'])