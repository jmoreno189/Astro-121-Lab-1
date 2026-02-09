from astro_analysis import DataAnalyzer

# Example: Analyzing the Noise data
analysis = DataAnalyzer(r".\data_collection\measurements\5_8_noise\your_timestamp_file.npz")

# 1. Plot power spectrum to see flatness
analysis.plot_time_and_freq()

# 2. Compare ACF to Power Spectrum to verify Correlation Theorem
lags, acf = analysis.compute_acf()