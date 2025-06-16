
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.fft import rfft, rfftfreq
import librosa
import librosa.display
import io

st.set_page_config(layout='wide', page_title="Simulación AM - Coherente")

st.title("🎙️ Simulación de Modulación AM - Detección Coherente")

# Subida de archivo
uploaded_file = st.file_uploader("Carga tu archivo de audio (mp3 o wav)", type=["mp3", "wav"])

# Parámetros ajustables
Fc = st.slider("Frecuencia de la portadora (Hz)", 1000, 20000, 5000)
m_index = st.slider("Índice de modulación (m)", 0.0, 1.0, 0.8)

if uploaded_file is not None:
    # Cargar audio
    audio, Fs = librosa.load(uploaded_file, sr=None, mono=True)
    audio = audio[int(20*Fs):int(25*Fs)]  # Extrae 5 segundos del segundo 20 al 25
    t = np.linspace(0, len(audio)/Fs, len(audio))

    Ac = 1.0  # Amplitud de portadora
    c = Ac * np.cos(2 * np.pi * Fc * t)
    y = (1 + m_index * audio) * c  # Señal AM

    # Demodulación coherente
    z = y * np.cos(2 * np.pi * Fc * t)
    # Filtro paso bajo (Butterworth)
    b, a = butter(6, Fc*2/Fs)
    m_rec = filtfilt(b, a, z)

    # Mostrar señales
    fig, axs = plt.subplots(4, 1, figsize=(12, 10))
    axs[0].plot(t, audio)
    axs[0].set_title("Señal original (mensaje)")
    axs[1].plot(t, y)
    axs[1].set_title("Señal modulada AM")
    axs[2].plot(t, z)
    axs[2].set_title("Producto con oscilador local")
    axs[3].plot(t, m_rec)
    axs[3].set_title("Señal demodulada")
    st.pyplot(fig)

    # Mostrar espectros
    def plot_fft(signal, fs, title):
        N = len(signal)
        yf = rfft(signal)
        xf = rfftfreq(N, 1/fs)
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(xf, np.abs(yf))
        ax.set_title(title)
        ax.set_xlabel("Frecuencia (Hz)")
        ax.set_ylabel("Magnitud")
        st.pyplot(fig)

    plot_fft(audio, Fs, "Espectro del mensaje original")
    plot_fft(y, Fs, "Espectro de la señal AM")
    plot_fft(m_rec, Fs, "Espectro de la señal demodulada")

    # Reproducción
    st.subheader("🎧 Reproduce las señales")
    st.audio(librosa.util.buf_to_float(audio).astype(np.float32).tobytes(), format='audio/wav')
    st.audio(librosa.util.buf_to_float(m_rec).astype(np.float32).tobytes(), format='audio/wav')
