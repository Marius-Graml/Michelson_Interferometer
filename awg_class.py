
from moku.instruments import ArbitraryWaveformGenerator

class awg():
    def __init__(self, ip_address, output_ch):
        self.ip_address = ip_address
        self.output_ch = output_ch
        self.obj = ArbitraryWaveformGenerator(ip_address, force_connect=True)

    def generate(self, gen_signal_df, output_freq):
        # gen_signal = pd-Series
        if output_freq <= 0:
            output_freq = 100
        gen_signal_df = 1/10 * gen_signal_df
        gen_signal_list = gen_signal_df.values.tolist()
        self.obj.generate_waveform(channel=1, sample_rate='Auto',lut_data=gen_signal_list, frequency=output_freq, amplitude=10)

    def output(self, enable):
        self.obj.enable_output(channel=self.output_ch, enable=enable)
