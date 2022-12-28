
import numpy as np
from dither_class import dither 
from MDT_COMMAND_LIB import *
        
my_dither = dither(ip_address='[fe80:0000:0000:0000:7269:79ff:feb9:0b52%7]', output_ch=1, dith_freq=100, theta=0, amp_dith=0.5)
my_dither.generate()

devs = mdtListDevices()
hdl = mdtOpen(devs[0][0], nBaud=115200, timeout=1)

def generate(hdl, random_const):
        mdtSetAllVoltage(hdl=hdl, voltage=random_const)

while True:
    random_const = np.random.rand(1)
    generate(hdl, random_const)