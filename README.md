# EEG Specparam/fooof pipeline

read fooof https://specparam-tools.github.io/

---

## Usage
- After EEG data preprocessing (in this case EEGlab was used) create a .mat file with average power value of each electrode at certain frequency (this is achieved by applying the Fast Fourier transform and obtaining a PSD plot.
- Place .mat file in loadmat(). One axis of .mat file must contain the frequencies (for example from 0 to 30 every 0.5 Hz) and the other axis must contain the averaged powers of each electrode. The arrays must coincide.
- Use the following functions in the code to get periodic and aperiodic parameters of EEG signal
- Lone or multi PSD analysis can be conducted

---

Results in PSD plots, offset, exponent of the aperiodic fit (model parameters), power, bandwidth and center frequency (peak parameters).

<img width="2691" height="534" alt="Screenshot 2023-04-03 140456" src="https://github.com/user-attachments/assets/59c1d78e-6d2c-4ef4-9b12-493b13df3b12" />

<img width="3149" height="1747" alt="Untitled-1" src="https://github.com/user-attachments/assets/34c80b87-79e2-4edb-b8bb-31f396d92175" />
