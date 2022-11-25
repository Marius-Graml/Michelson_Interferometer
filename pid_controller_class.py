
from simple_pid import PID
import numpy as np
import pandas as pd

class pid_controller():
    def __init__(self, Kp, Ki, Kd, setpoint=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.obj = PID(self.Kp, self.Ki, self.Kd, self.setpoint, output_limits=(-4,4))
        self.signal = None

    def get_PID_output_all(self, input_signal, dith_freq, amp_dith):
        # Data: pd Dataframe with columns 'time' and 'channel'
        data = np.reshape(np.array(input_signal['ch']), (-1,1))
        t = np.reshape(np.array(input_signal['time']), (-1,1))
        output_data = np.zeros(np.shape(data))
        for n, sample_value in enumerate(data):
            output_data[n] = self.obj(sample_value)

        # Add dither signal to pid output
        pid_output_dith_np = output_data + amp_dith * np.sin(2*np.pi*dith_freq * t)
        # Add offset to pid_output
        pid_output_dith_np = 1/10 * 100/2 + pid_output_dith_np
        
        output = np.concatenate((t, pid_output_dith_np), axis=1)
        output = pd.DataFrame(output, columns=['time', 'ch'])
        return output

    # def get_PID_output_single(self, input_signal, dith_freq, amp_dith):
    #     # Data: pd Dataframe with columns 'time' and 'channel'
    #     data = np.reshape(np.array(input_signal['ch']), (-1,1))
    #     t = np.array(input_signal['time'])
    #     for n, sample_value in enumerate(data):
    #         output_sample = self.obj(sample_value) + amp_dith * np.sin(2*np.pi*dith_freq * t[n])

    #     return output_sample