import soundfile as sf
from scipy import signal

from plot import plot_fft, get_integrals

# read .wav file
input_signal, fs = sf.read("files/Sound_Noise.wav")
# sampling frequency of Input signal
sampl_freq = fs
# order of the filter
order = 4
# cutoff frquency 4kHz
# cutoff_freq = 4000.0
cutoff_freq = 2770.0
# digital frequency
Wn = 2 * cutoff_freq / sampl_freq
# b and a are numerator and denominator polynomials_respectively
b, a = signal.butter(order, Wn, "low")
# filter the input signal with butterworth filter
output_signal = signal.filtfilt(b, a, input_signal)
# output signal = signal.lfilter(b, a, input_signal)
for i in range(20):
    output_signal = signal.filtfilt(b, a, output_signal)

# write the output signal into .wav file
sf.write("out/Sound_Low_Noise.wav", output_signal, fs)

# Plot
fft, freq = plot_fft(output_signal, "Sound_Low_Noise", fs)

# Get integrals
int_bef, int_aft = get_integrals(fft, freq, cutoff_freq)
print("\nintegral_before ", int_bef, "\nintegral_after", int_aft)
