import numpy as np
import ugradio.sdr as sdr
from astro_data import DataCollector

# Setup hardware and collector
collector = DataCollector()

while True:
    print("Please enter sampling frequency (hz):")
    sample_rate = input() # Hz

# 1. Standard Capture (Internal Anti-Aliasing Filter ON)
    sdr_std = sdr.SDR(direct=True, sample_rate=sample_rate)
    collector.capture_and_save(
    sdr_std, 
    section_name="5_3_nyquist", 
    v_input_mv=2.5, 
    alias_filter="default",
    notes="Testing amplitude response below 500kHz"
    )

    sdr_std.close()

# 2. Aliasing Capture (Internal Filter OFF/Overridden)
# Using the override coeffs from the manual
    custom_fir = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2047])
    sdr_alias = sdr.SDR(direct=True, sample_rate=sample_rate, fir_coeffs=custom_fir)

    collector.capture_and_save(
    sdr_alias, 
    section_name="5_3_nyquist", 
    v_input_mv=2.5, 
    alias_filter="overridden",
    notes="Observing aliasing from higher Nyquist zones"
    )

    sdr_alias.close()
    print("Measurement complete. Take another measurement? (y/n)")
    ans = input()
    if ans == 'n':
        break