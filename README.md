# EEG Specparam/fooof pipeline

read fooof https://specparam-tools.github.io/

## Usage
- After EEG data preprocessing (in this case EEGlab was used) create a .mat file with average power value of each electrode at certain frequency (this is achieved by applying the Fast Fourier transform and obtaining a PSD plot.
- Place .mat file in loadmat(). One axis of .mat file must contain the frequencies (for example from 0 to 30 every 0.5 Hz) and the other axis must contain the averaged powers of each electrode. The arrays must coincide.
- Use the following functions in the code to get periodic and aperiodic parameters of EEG signal
- Lone or multi PSD analysis can be conducted
