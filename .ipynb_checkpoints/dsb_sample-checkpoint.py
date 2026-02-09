import ugradio.sdr as sdr
from astro_data import DataCollector

collector = DataCollector()
nsamples=4096
nblocks=5

while True:
# Direct mode is used to sample the IF output of the external mixer
    print(f"Preparing to sample DSB mixer data ({nblocks}, {nsamples}). Please enter sample rate (Mhz):")
    sample_rate = float(input())*1e6
    print("Please enter radio frequency (Mhz):")
    rf_freq_mhz = float(input())
    print(f"Please enter local oscillator frequency (hz) (recommended: [{(rf_freq*0.95):.2}, {(rf_freq*1.05):.2}]):")
    lo_freq = float(input())
     
    sdr_dsb_mhz = sdr.SDR(direct=True, sample_rate)

# RF = LO + Delta_nu
    collector.capture_and_save(
    sdr_dsb, 
    section_name="7_1_dsb_mixer", 
    nsamples, 
    nblocks,
    lo_freq_mhz,
    rf_freq_mhz,
    delta_nu_khz=abs(lo_freq_mhz-rf_freq_mhz),
    notes="Capturing sum and difference frequencies for Fourier filtering"
    )

    sdr_dsb.close()

    print("Sample again? (y/n)")
    ans = input()
    if ans == "n":
        break