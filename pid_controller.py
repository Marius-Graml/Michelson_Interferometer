
from moku.instruments import PIDController
import numpy as np

pid = PIDController(ip='[fe80:0000:0000:0000:7269:79ff:feb9:0b52%7]', force_connect=True)

# Config
pid.enable_input(channel=1, enable=True)
pid.enable_output(channel=1, signal=True, output=True)
pid.set_control_matrix(channel=1, input_gain1=1, input_gain2=0)

#pid.set_by_frequency(channel=1, prop_gain=20*np.log10(5), int_crossover=100, diff_crossover=1e4, int_saturation=20*np.log10(20), diff_saturation=20*np.log10(20))

pid.set_by_gain(channel=1, prop_gain=5, int_gain=10, diff_gain=3)

pid.set_output_offset(channel=1, offset=2.5)

 