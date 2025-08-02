# If running in Google Colab, install necessary package
try:
    import google.colab
    IN_COLAB = True
except:
    IN_COLAB = False

if IN_COLAB:
    !pip install -q fooof

# Mount Google Drive if in Colab
if IN_COLAB:
    from google.colab import drive
    drive.mount('/content/drive')

# Imports
import os
import glob
import numbers
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.io import loadmat, savemat
from fooof import FOOOF, FOOOFGroup
from fooof.bands import Bands
from fooof.analysis import get_band_peak_fm, get_band_peak_fg
from fooof.plts.annotate import plot_annotated_model
from fooof.plts.aperiodic import plot_aperiodic_params, plot_aperiodic_fits
from fooof.utils.reports import methods_report_info

# ------------------------------
# Lone PSD Analysis (Single Subject)
# ------------------------------

# Load data from .mat file
data_single = loadmat('/content/drive/MyDrive/fooof/pirmas_powerintas.mat')
freqs_single = np.squeeze(data_single['freq'])
psd_single = np.squeeze(data_single['power'])

# Fit FOOOF model
fm = FOOOF()
fm.report(freqs_single, psd_single, [0, 61])

# Save results to .mat file
fooof_results_dict = fm.get_results()._asdict()
savemat('/content/drive/MyDrive/igb/fooof_results.mat', fooof_results_dict)

# Print model results
print(f"Aperiodic Parameters: {fm.aperiodic_params_}")
print(f"Peak Parameters: {fm.peak_params_}")
print(f"R-squared: {fm.r_squared_}, Error: {fm.error_}")

# Plot FOOOF model
plt.figure(figsize=(10, 5))
plot_annotated_model(fm, plt_log=False)
plt.title("FOOOF Model: PSD with Aperiodic and Periodic Components")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")
plt.grid(True)
plt.show()

# ------------------------------
# Multi-subject PSD Analysis
# ------------------------------

# Load multi-subject PSD data
data_multi = loadmat('/content/drive/MyDrive/fooof/visu poweriai powerinti.mat')
freqs_multi = np.squeeze(data_multi['freq']).astype(float)
psds_multi = np.squeeze(data_multi['power']).astype(float)

# Fit FOOOFGroup model
fg = FOOOFGroup()
fg.report(freqs_multi, psds_multi, [1, 100])

# Extract and save parameters
exponents = fg.get_params('aperiodic_params', 'exponent')
savemat('/content/drive/MyDrive/fooof/exps.mat', {'exps': exponents})

# Report methods and parameters
methods_report_info(fg)

# Save R-squared and offset values
r2s_df = pd.DataFrame(fg.get_params('r_squared'))
r2s_df.to_csv('/content/drive/MyDrive/powerinta data/r_squared.csv')

offset_df = pd.DataFrame(fg.get_params('aperiodic_params', 'offset'))
offset_df.to_csv('/content/drive/MyDrive/powerinta data/offset.csv')

# Save aperiodic parameters
aps = fg.get_params('aperiodic_params')
aps_df = pd.DataFrame(aps, columns=['offset', 'knee', 'exponent'])
aps_df.to_csv('/content/drive/MyDrive/fooof/off ir exp.csv', index=False)

# Save alpha peak center frequencies
bands = Bands({'delta': [0, 4], 'theta': [4, 8], 'alpha': [8, 15], 'beta': [15, 30], 'gamma': [30, 100]})
alpha_peaks = get_band_peak_fg(fg, bands.alpha)
alpha_df = pd.DataFrame(alpha_peaks, columns=['CF', 'PW', 'BW'])
alpha_df.to_csv('/content/drive/MyDrive/powerinta data/alpha center frequencies.csv', index=False)

# Plot aperiodic fits
plot_aperiodic_fits(aps, [1, 30], control_offset=True, log_freqs=False)

# Save FOOOF report
fm.save_report('FOOOF_report', '/content/drive/MyDrive/igb')

# ------------------------------
# CSV Processing for Subject Power
# ------------------------------

# Combine individual subject CSV files
os.chdir('/content/drive/MyDrive/power exceliai')
csv_files = glob.glob('*.csv')
df_combined = pd.concat([pd.read_csv(f) for f in csv_files], axis=1)

# Drop Hz label column
if 'Hz\subj' in df_combined.columns:
    df_combined = df_combined.drop(columns=['Hz\subj'])

# Average power values by column (grouping repeated headers)
df_avg = df_combined.groupby(by=df_combined.columns, axis=1).apply(
    lambda g: g.mean(axis=1) if isinstance(g.iloc[0, 0], numbers.Number) else g.iloc[:, 0])

# Square and transpose for PSD
psd_squared = np.square(df_avg)
psd_transposed = psd_squared.T
psd_transposed.to_csv('/content/drive/MyDrive/fooof/visu_poweriai_powerinti.csv', index=False)

# ------------------------------
# Merge ARSQ Questionnaire with FOOOF Parameters
# ------------------------------

arsq_df = pd.read_excel('/content/drive/MyDrive/fooof/arsq ir parametrai be out powerinti.xlsx', sheet_name='Sheet1')
arsq_cleaned = arsq_df.drop(columns=arsq_df.columns[0])  # Drop subject ID column
print(arsq_cleaned.head())
