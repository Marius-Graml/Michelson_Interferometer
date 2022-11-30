
from simple_pid import PID
import numpy as np
import pandas as pd

class pid_controller():
    def __init__(self, Kp, Ki, Kd, setpoint, amp_dith):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.amp_dith = amp_dith
        self.obj = PID(self.Kp, self.Ki, self.Kd, self.setpoint, output_limits=(-5+self.amp_dith,5-self.amp_dith))

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
        pid_output_dith_np = 1/15 * 150/2 + pid_output_dith_np
        
        output = np.concatenate((t, pid_output_dith_np), axis=1)
        output = pd.DataFrame(output, columns=['time', 'ch'])
        return output

    def get_PID_output_single(self, input_signal, dith_freq, amp_dith, single=True):
        data = np.array(input_signal['ch'])
        t = np.reshape(np.array(input_signal['time']), (-1,1))
        if single:
            data_sample = data[-1]
            output_sample = self.obj(data_sample)
        else:
            # for sample_value in data:
            #     output_sample = self.obj(sample_value)
            output_sample = self.obj(np.mean(data[-1024:]))
            print(np.size(data[-1024:]))
        output_data = output_sample * np.ones((np.shape(data)[0], 1))
        # Add dither signal
        output_data = output_data + amp_dith * np.sin(2*np.pi*dith_freq * t)
        # Add offset to pid_output
        output_data = 1/15 * 150/2 + output_data
        output_data = np.concatenate((t, output_data), axis=1)
        output_data = pd.DataFrame(output_data, columns=['time', 'ch'])
        return output_data

    def reset_pid(self):
        self.obj = PID(self.Kp, self.Ki, self.Kd, self.setpoint, output_limits=(-5+self.amp_dith,5-self.amp_dith))