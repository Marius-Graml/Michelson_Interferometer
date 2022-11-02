
import pandas as pd
import numpy as np

def get_one_ch_data(data, ch_number=1):
    if ch_number == 1:
        signal_df = pd.DataFrame(data).iloc[:,[0,1]]
        signal_df = signal_df.rename({'ch1': 'ch'}, axis=1)
    elif ch_number == 2:
        signal_df = pd.DataFrame(data).iloc[:,[0,2]]
        signal_df = signal_df.rename({'ch2': 'ch'}, axis=1)
    
    return signal_df