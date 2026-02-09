import ugradio.sdr as sdr
from astro_data import DataCollector

nsamples=16000
nblocks=64
sample_rate=3.2e6

collector = DataCollector()
# Use maximum sample rate permitted by SDR sampling bandwidth to avoid aliasing, i.e. 3.2 mhz
print(f"Preparing to sample noise generator with ({nblocks}, {nsamples}) (blocks, samples) at {sample_rate} hz. Press any key to continue.")
input()
sdr_noise = sdr.SDR(direct=True, sample_rate)

# Capture 64 blocks to allow for averaging (N=2, 4, 8, 16, 32, 64)
collector.capture_and_save(
    sdr_noise, 
    section_name="5_8_noise", 
    nsamples=16000, 
    nblocks=64,
    source="Lab Noise Generator",
    filter="Band-pass connected" # [cite: 175]
)
print("Measurement complete.")