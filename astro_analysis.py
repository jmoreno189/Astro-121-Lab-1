import numpy as np
import matplotlib.pyplot as plt
import os
import ugradio.dft as dft

class DataAnalyzer:
    """A toolset for processing and plotting radio lab data."""
    
    def __init__(self, file_path):
        # Load the compressed data and metadata
        self.archive = np.load(file_path, allow_pickle=True)
        self.data = self.archive['data']
        self.meta = self.archive['metadata'].item()
        self.vsamp = self.meta['sample_rate']

    def get_power_spectrum(self, block_index=0, use_gpu_fft=True):
        """
        Computes the power spectrum for a specific block of data.
        Handles both Real (Direct) and Complex (IQ) data.
        """
        v_data = self.data[block_index]
        
        # If IQ data, convert the (nsamples, 2) array to a complex array
        if not self.meta['direct_mode']:
            v_data = v_data[..., 0] + 1j * v_data[..., 1]
            
        # Use numpy.fft for speed
        freqs = np.fft.fftfreq(len(v_data), 1/self.vsamp)
        v_spec = np.fft.fft(v_data)
        
        # Power is proportional to voltage squared
        p_spec = np.abs(v_spec)**2
        
        # Shift frequencies for plotting (negative to positive)
        return np.fft.fftshift(freqs), np.fft.fftshift(p_spec)

    def plot_time_and_freq(self, block_index=0):
        """Generates the standard two-panel plot for the report."""
        f, p = self.get_power_spectrum(block_index)
        t = np.arange(len(self.data[block_index])) / self.vsamp

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Time Domain Plot
        ax1.plot(t * 1e6, self.data[block_index])
        ax1.set_xlabel('Time ($\mu s$)')
        ax1.set_ylabel('ADC Counts (int8)')
        ax1.set_title(f"Time Series: {self.meta.get('section_name', 'Data')}")

        # Frequency Domain Plot
        ax2.semilogy(f / 1e6, p) # Log scale helps find leakage
        ax2.set_xlabel('Frequency (MHz)')
        ax2.set_ylabel('Power')
        
        plt.tight_layout()
        plt.show()

    def compute_acf(self, block_index=0):
        """Computes Autocorrelation for comparison with Power Spectrum."""
        v_data = self.data[block_index]
        acf = np.correlate(v_data, v_data, mode='full')
        lags = np.arange(-len(v_data) + 1, len(v_data))
        return lags / self.vsamp, acf