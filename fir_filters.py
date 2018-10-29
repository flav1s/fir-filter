import numpy as np
import matplotlib.pyplot as plt
import FIRFilter as ff
from scipy import fftpack


#-----------------------------------#
#               Sinal               #
#-----------------------------------#
class Signal:
    def __init__(self, frequency_1, frequency_2, frequency_3, sample_rate, start, end):
        self.f1 = frequency_1  # Frequencia 1
        self.f2 = frequency_2  # Frequencia 2
        self.f3 = frequency_3  # Frequencia 3
        self.w1 = 2.0 * np.pi * frequency_1  # Frequencia 1 Angular
        self.w2 = 2.0 * np.pi * frequency_2  # Frequencia 2 Angular
        self.w3 = 2.0 * np.pi * frequency_3  # Frequencia 3 Angular
        self.fs = sample_rate  # Frequencia de Amostragem
        self.ts = 1.0/self.fs  # Intervalo entre amostras
        self.ws = 2.0 * np.pi * sample_rate  # Frequencia de Amostragem Normalizada
        self.x = np.arange(start, end, self.ts, np.float)  # Eixo X
        self.y = np.sin(2 * np.pi * self.f1 * self.x) + \
                 np.sin(2 * np.pi * self.f2 * self.x) + \
                 np.sin(2 * np.pi * self.f3 * self.x)  # Eixo Y
        self.Y = []
        self.freqs = []
        self.S = []

    def plot(self):
        plt.figure()
        plt.plot(self.x,self.y)
        plt.grid()
        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude');
        plt.title('Sinal')

    def fft(self):
        self.Y = fftpack.fft(self.y)  # fft scipy
        self.freqs = fftpack.fftfreq(len(self.Y)) * self.fs  # vetor de frequencia scipy
        plt.figure()
        plt.stem(self.freqs, np.abs(self.Y))
        plt.grid()
        plt.xlabel('Frequencia [Hz]')
        plt.ylabel('Magnitude')
        plt.title("Sinal: Espectro")

    def ifft(self, iY):
        self.iy = np.fft.ifft(iY)
        plt.figure()
        plt.plot(self.x, np.abs(self.iy))
        plt.title("Sinal Filtrado")
        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude')
        plt.grid()


#-----------------------------------#
#               Main                #
#-----------------------------------#
signal = Signal(50, 300, 750, 2000, 0, 1) # frequency_1, frequency_2, frequency_3, sample_rate, start, end
signal.plot()
signal.fft()
filter = ff.FIRFilter(500.0, 800.0, 0.1, 100.0, 40.0, signal.fs) # low_border, high_border, ripple, transition_band, band_pass_attenuation, fs
filter.fft(len(signal.Y))
S = filter.apply_filter_frequency(signal.Y)
signal.ifft(S)
<<<<<<< HEAD
plt.show()
=======
plt.show()
>>>>>>> d6173e8ad498b35c2846c91aa3cd4b796ec69948
