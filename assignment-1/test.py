import ctypes
import soundfile as sf
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import subprocess

print("Generating Sound_Low_Noise.wav")
import my_filter
print("Done\n")

print("Generating .dat files from .wav files")
x, fs = sf.read("out/Sound_Low_Noise.wav")

n = int(2 ** np.floor(np.log2(len(x))))
f = open("out/Sound_Low_Noise.dat", "w")
for i in range(n):
    f.write(str(x[i]) + "\n")
f.close()

x, fs = sf.read("files/Sound_Noise.wav")

n = int(2 ** np.floor(np.log2(len(x))))
f = open("out/Sound_Noise.dat", "w")
for i in range(n):
    f.write(str(x[i]) + "\n")
f.close()
print("Done\n")

print("Compiling and running the C code")
subprocess.run(
    "gcc -fPIC -o out/libsig.so signal.c -lm && cd out/ && ./libsig.so && cd ..",
    shell=True,
    check=True,
    text=True,
)
# ctypes.CDLL("./out/libsig.so").main()
print("Done\n")


print("Generating .wav files from .dat files")
yn = np.loadtxt("out/Sound_Low_Noise_IFFT.dat")
sf.write("out/Sound_Low_Noise_C.wav", yn, fs)

yn = np.loadtxt("out/Sound_Noise_IFFT.dat")
sf.write("out/Sound_Noise_C.wav", yn, fs)
print("Done\n")
print("Finished!")
