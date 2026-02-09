import ugradio.sdr as sdr
from astro_data import DataCollector

collector = DataCollector()

# Software Tuning: Turn OFF direct sampling to use the R820T mixer
# We tune to 100MHz (FM band) as a test or your specific RF
sdr_ssb = sdr.SDR(direct=False, center_freq=100e6, sample_rate=2.2e6, gain=20)

collector.capture_and_save(
    sdr_ssb, 
    section_name="7_3_ssb_mixer", 
    nsamples=2048, 
    nblocks=10,
    mode="Internal IQ Sampling",
    notes="Separating USB and LSB using complex voltage spectra" # [cite: 263]
)

print("Measurement complete.")