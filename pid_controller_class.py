
from simple_pid import PID
import numpy as np
import pandas as pd

class pid_controller():
    def __init__(self, Kp, Ki, Kd, setpoint=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.obj = PID(self.Kp, self.Ki, self.Kd, self.setpoint)
        self.fs = 8928571.42857143

    def get_PID_output(self, input_signal):

        # Data: pd Dataframe with columns 'time' and 'channel'
        data = np.reshape(np.array(input_signal['ch']), (-1,1))
        output_data = np.zeros(np.shape(data))
        for n, sample_value in enumerate(data):
            output_data[n] = self.obj(sample_value)
        n_axis = np.arange(np.shape(output_data)[0])
        t_axis = np.reshape(n_axis/self.fs, (-1,1)) # in s
        output = np.concatenate((t_axis, output_data), axis=1)

        output_df = pd.DataFrame(output, columns=['time', 'ch'])
        return output_df