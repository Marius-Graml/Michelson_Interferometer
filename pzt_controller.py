
try:
    from MDT_COMMAND_LIB import *
except OSError as ex:
    print("Warning:",ex)

def main():
    try:
        devs = mdtListDevices()
        if(len(devs)<=0):
           print('There is no devices connected')
           exit()

        hdl = mdtOpen(devs[0][0], nBaud=115200, timeout=1)
        print(hdl)
        mdtSetAllVoltage(hdl=hdl, voltage=17)

    except Exception as ex:
        print("Warning:", ex)
    print("*** End ***")
    input()
main()