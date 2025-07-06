
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, butter, lfilter
from scipy.fft import fft, fftfreq
from scipy.io import wavfile

# Configuración general
st.set_page_config(page_title="SSB-AM Dashboard", layout="wide")
st.title("📡 Dashboard de Modulación y Demodulación SSB-AM")

# Parámetros básicos
fs = 8000  # Frecuencia de muestreo
fc = 1000  # Frecuencia de la portadora (Hz)
Ac = 1     # Amplitud de la portadora
duration = 1  # Duración para pulso rectangular (s)

# Opciones de señal mensaje
option = st.sidebar.radio(
    "Seleccione la señal mensaje:",
    ("Pulso rectangular", "Subir archivo de audio (5s)")
)

# Generar señal mensaje
if option == "Pulso rectangular":
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    m = np.zeros_like(t)
    m[int(0.25*len(t)):int(0.75*len(t))] = 1  # Pulso rectangular centrado
    st.write("**Pulso rectangular:** Duración de 1 segundo")
else:
    uploaded_file = st.sidebar.file_uploader("Suba archivo WAV (5s)", type=["wav"])
if uploaded_file is not None:
    fs, m = wavfile.read(uploaded_file)
    if len(m.shape) > 1:
        m = m[:, 0]  # Solo un canal
    t = np.arange(len(m)) / fs
    m = m / np.max(np.abs(m))  # Normalizar
    st.write(f"**Audio cargado:** {uploaded_file.name}")

    # 👇 Nuevo: reproductor de audio
    st.audio(uploaded_file, format='audio/wav')

else:
    st.warning("⚠️ Cargue un archivo WAV de máximo 5 segundos.")
    st.stop()


# Mostrar señal original
fig, ax = plt.subplots()
ax.plot(t, m)
ax.set_title("Señal mensaje m(t)")
ax.set_xlabel("Tiempo [s]")
ax.set_ylabel("Amplitud")

# NUEVO: límites y rejilla
ax.set_xlim([0, duration])
ax.set_ylim([-0.2, 1.2])
ax.grid(True)

st.pyplot(fig)

# Modulación SSB-AM
analytic_signal = hilbert(m)
ssb = np.real(m * np.cos(2 * np.pi * fc * t) - np.imag(analytic_signal) * np.sin(2 * np.pi * fc * t))

# Espectro de la señal original
M_f = np.abs(fft(m))
freqs = fftfreq(len(m), 1/fs)

# Espectro de la señal modulada
S_f = np.abs(fft(ssb))

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(freqs[:len(freqs)//2], M_f[:len(M_f)//2])
    ax1.set_title("Espectro de la señal mensaje")
    ax1.set_xlabel("Frecuencia [Hz]")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(freqs[:len(freqs)//2], S_f[:len(S_f)//2])
    ax2.set_title("Espectro de la señal SSB-AM")
    ax2.set_xlabel("Frecuencia [Hz]")
    st.pyplot(fig2)

# Demodulación coherente
demod = ssb * np.cos(2 * np.pi * fc * t) * 2  # Multiplicación coherente

# Filtro pasa-bajos
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    norm_cutoff = cutoff / nyq
    b, a = butter(order, norm_cutoff, btype='low')
    y = lfilter(b, a, data)
    return y

demod_filtered = butter_lowpass_filter(demod, cutoff=1500, fs=fs, order=5)

# Graficar señal demodulada
fig3, ax3 = plt.subplots()
ax3.plot(t, demod_filtered)
ax3.set_title("Señal demodulada")
ax3.set_xlabel("Tiempo [s]")
st.pyplot(fig3)

st.success("✅ Modulación y demodulación SSB-AM completadas.")
