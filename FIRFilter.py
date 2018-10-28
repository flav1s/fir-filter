import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

#-----------------------------------#
#-              Filtro             -#
#-----------------------------------#
class FIRFilter:
    def __init__(self, low_border, high_border, ripple, transition_band, band_pass_attenuation, fs):
        self.low = low_border
        self.low_w = self.low * np.pi / (fs / 2)  # low-pass normalize
        self.high = high_border
        self.high_w = self.high * np.pi / (fs / 2)  # low-pass normalize
        self.band = self.high - self.low
        self.ripple_db = ripple
        self.transition_band = transition_band
        self.band_pass_attenuation_db = -np.abs(band_pass_attenuation)
        self.fs = fs
        self.ripple = 10 ** (self.ripple_db/20) # sigma 1
        self.band_pass_attenuation = 10 ** (self.band_pass_attenuation_db/20) # sigma 2
        self.sigma = min(self.ripple,self.band_pass_attenuation) # sigma minimo = usado para definicao do filtro
        self.transition_band_w = ((2.0 * np.pi) * (self.transition_band / self.fs))  # Banda de transicao (angular)
        self.M = int()
        print("sigma = " + str(self.sigma))
        self.window_create()
        # Resposta ao impulso
        self.hc = np.empty(self.M)
        count = np.arange(self.M)
        self.hc = self.high_w/np.pi * np.sinc((self.high_w*(count-self.M/2))/np.pi) - \
                  self.low_w/np.pi * np.sinc((self.low_w*(count-self.M/2))/np.pi)
        # Aplicar janela
        self.h = np.multiply(self.window, self.hc)
        self.H = []
        self.H_db = []
        self.freqs = []

    def fft(self, n):
        # Espectro do filtro
        self.H = fftpack.fft(self.h, n)
        self.H_db = 20 * np.log10(np.abs(self.H))
        self.freqs = fftpack.fftfreq(len(self.H)) * self.fs  # vetor de frequencia scipy
        # Plot filtro
        plt.figure()
        plt.plot(self.freqs, self.H_db)
        plt.xlabel("Frequencia[Hz]")
        plt.ylabel("Magnitude [dB]")
        plt.title("Filtro")
        plt.grid()

    def window_create(self):
        # Decisao e criacao de janela
        # Janela retangular
        if self.band_pass_attenuation_db >= -21:
            self.M = int(((4*np.pi) / self.transition_band_w) - 1)
            print("Janela retangular => M = " + str(self.M))
            self.window = np.ones(self.M)

        # Janela Bartlett
        elif self.band_pass_attenuation_db >= -25:
            self.M = int((8*np.pi) / self.transition_band_w)
            self.window = np.empty(self.M)
            print("Janela Bartlett => M = " + str(self.M))
            for a in range(int(self.M)):
                if a <= int(self.M/2):
                    self.window[a] = 2*a/self.M
                else:
                    self.window[a] = 2 - (2 * a/self.M)
        # Janela Hann
        elif self.band_pass_attenuation_db >= -44:
            self.M = int((8*np.pi) / self.transition_band_w)
            print("Janela Hann => M = " + str(self.M))
            self.window = 0.5 - 0.5 * np.cos((2 * np.arange(self.M) * np.pi) / self.M)
        # Janela Hamming
        elif self.band_pass_attenuation_db >= -53:
            self.M = int((8*np.pi) / self.transition_band_w)
            print("Janela Hamming => M = " + str(self.M))
            self.window = 0.54 - 0.46 * np.cos((2 * np.arange(self.M) * np.pi) / self.M)
        # Janela Blackman
        elif self.band_pass_attenuation_db >= -74:
            self.M = int((12*np.pi) / self.transition_band_w)
            print("Janela Blackman => M = " + str(self.M))
            cout = np.arange(self.M)
            self.window = 0.42 - 0.5 * np.cos((2 * cout * np.pi) / self.M) + 0.08 * np.cos((4 * cout * np.pi) / self.M)
        else:
            print("Cant do!")
    def apply_filter_frequency(self, signal):
        self.S = np.multiply(self.H, signal)
        plt.figure()
        plt.stem(self.freqs, np.abs(self.S))
        plt.grid()
        plt.xlabel("Frequencia[Hz]")
        plt.ylabel("Magnitude")
        plt.title("Sinal Filtrado: Espectro")
        plt.show(False)
        return self.S
