
from moku.instruments import ArbitraryWaveformGenerator

class awg():
    def __init__(self, ip_address, output_ch):
        self.ip_address = ip_address
        self.output_ch = output_ch
        self.obj = ArbitraryWaveformGenerator(ip_address, force_connect=True)

    def generate(self, gen_signal_df):
        # gen_signal = pd-DataFrame
        gen_signal_list = gen_signal_df['ch'].values.tolist()
        self.obj.generate_waveform(channel=1, sample_rate='Auto',lut_data=gen_signal_list, frequency=1e-3, amplitude=1)
