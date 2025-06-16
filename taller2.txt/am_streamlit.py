
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import librosa
import soundfile as sf

# Función para graficar señal en el tiempo
def plot_time(t, signal, title):
    fig, ax = plt.subplots()
    ax.plot(t, signal)
    ax.set_title(title)
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Amplitud")
    st.pyplot(fig)

# Función para graficar espectro en frecuencia
def plot_freq(signal, fs, title):
    N = len(signal)
    freq = np.fft.rfftfreq(N, 1/fs)
    spectrum = np.abs(np.fft.rfft(signal))
    fig, ax = plt.subplots()
    ax.plot(freq, spectrum)
    ax.set_title(title)
    ax.set_xlabel("Frecuencia [Hz]")
    ax.set_ylabel("Magnitud")
    st.pyplot(fig)

# Filtro pasa bajas (Butterworth)
def lowpass_filter(signal, fs, cutoff=4000):
    b, a = butter(6, cutoff / (fs / 2), btype='low')
    return filtfilt(b, a, signal)

# Interfaz Streamlit
st.title("Simulación de Modulación AM - Detección Coherente")

uploaded_file = st.file_uploader("Carga tu archivo de audio (mp3 o wav)", type=["mp3", "wav"])
Fc = st.slider("Frecuencia de la portadora (Hz)", 1000, 20000, 10000)
mod_index = st.slider("Índice de modulación (m)", 0.0, 1.0, 0.8)

if uploaded_file is not None:
    # Cargar fragmento de audio (20 a 25 s)
    y, fs = librosa.load(uploaded_file, sr=None, offset=20.0, duration=5.0)
    t = np.linspace(0, len(y)/fs, len(y))

    Ac = np.max(np.abs(y)) / mod_index  # Para asegurar índice m deseado
    c = Ac * np.cos(2 * np.pi * Fc * t)  # Portadora
    y_mod = (1 + y / Ac) * c             # Señal AM

    # Demodulación coherente
    product = y_mod * np.cos(2 * np.pi * Fc * t)
    y_demod = lowpass_filter(product, fs)

    # Reproductor y gráficos
    st.subheader("Audio original")
    st.audio(uploaded_file, format="audio/wav")

    st.subheader("Gráficas en el tiempo")
    plot_time(t, y, "Mensaje original")
    plot_time(t, c, "Portadora")
    plot_time(t, y_mod, "Señal AM")
    plot_time(t, product, "Producto en demodulación")
    plot_time(t, y_demod, "Señal demodulada")

    st.subheader("Espectros en frecuencia")
    plot_freq(y, fs, "Espectro del mensaje")
    plot_freq(c, fs, "Espectro de la portadora")
    plot_freq(y_mod, fs, "Espectro AM")
    plot_freq(product, fs, "Espectro tras multiplicación")
    plot_freq(y_demod, fs, "Espectro de la señal demodulada")
