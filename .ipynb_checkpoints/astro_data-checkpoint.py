"""
Author: Joseph Moreno
Description: Python package designed to collect data sampled from an SDR using the ugradio.sdr package. An automatic file saving system is implemented.
"""
import os
import numpy as np
from datetime import datetime
import ugradio.sdr as sdr

class DataCollector:
    """Helper class to automate data collection and file management. It was certainly frustrating at the start of Lab 1 to sift through mismanaged file directories and misplaced data; technical debt is very real. I learned the hard way."""
    
    def __init__(self, base_path=".\\data_collection\\measurements"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def capture_and_save(self, sdr_obj, section_name, nsamples=2048, nblocks=1, **metadata):
        """
        Captures data from the SDR and saves it as a .npz file.
        
        Args:
            sdr_obj: The ugradio.sdr.SDR instance.
            section_name: Subfolder (e.g., 'sampling', 'noise', 'mixer').
            metadata: Custom tags (v_in, v_samp, alias_filter, etc).
        """
        # 1. Create directory for the lab section
        save_dir = os.path.join(self.base_path, section_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 2. Capture the data
        print(f"Capturing {nblocks} blocks of {nsamples} samples...")
        data = sdr_obj.capture_data(nsamples=nsamples, nblocks=nblocks)

        # 3. Consolidate Metadata
        all_metadata = {
            'timestamp': datetime.now().isoformat(),
            'sample_rate': sdr_obj.sample_rate,
            'direct_mode': sdr_obj.direct,
            'center_freq': sdr_obj.center_freq,
            'gain': sdr_obj.gain,
            'nsamples': nsamples,
            'nblocks': nblocks,
            **metadata # Include user-defined tags like 'v_input' or 'target_freq'
        }

        # 4. Generate File Name: YYYYMMDD_HHMM_section_mode.npz
        time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        mode_str = "direct" if sdr_obj.direct else "IQ"
        filename = f"{time_str}_{section_name}_{mode_str}.npz"
        file_path = os.path.join(save_dir, filename)

        # 5. Save using numpy's compressed format
        np.savez(file_path, data=data, metadata=all_metadata)
        print(f"Success! Data saved to: {file_path}")
        return file_path

# --- EXAMPLE USAGE FOR WEEK 1 ---
if __name__ == "__main__":
    # Initialize hardware
    my_sdr = sdr.SDR(direct=True, sample_rate=2.2e6)
    collector = DataCollector()

    # Capture Section 5.3: Sine wave sampling
    collector.capture_and_save(
        my_sdr, 
        section_name="sampling", 
        v_input_mv=3.0, 
        signal_freq_hz=400e3,
        alias_filter="default"
    )