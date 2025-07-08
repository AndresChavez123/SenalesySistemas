# ================================
# 📦 Importación de librerías necesarias
# ================================
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, butter, lfilter, tf2zpk, freqz
from scipy.fft import fft, fftfreq
from scipy.io import wavfile

# ================================
# ⚙️ Configuración general de la app
# ================================
st.set_page_config(page_title="SSB-AM Dashboard", layout="wide")
st.title("📡 Dashboard de Modulación y Demodulación SSB-AM")

# ================================
# ⚙️ Parámetros del sistema
# ================================
fs = 8000       # Frecuencia de muestreo por defecto (Hz)
fc = 1000       # Frecuencia de la portadora (Hz)
Ac = 1          # Amplitud de la portadora
duration = 1    # Duración de la señal (s), usada para el pulso

# ================================
# 🎵 Selección del tipo de señal mensaje
# ================================
option = st.sidebar.radio(
    "Seleccione la señal mensaje:",
    ("Pulso rectangular", "Subir archivo de audio (5s)")
)

uploaded_file = None  # Inicializamos para evitar errores

# ================================
# 🟢 Opción 1: Pulso rectangular
# ================================
if option == "Pulso rectangular":
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    m = np.zeros_like(t)
    m[int(0.25*len(t)):int(0.75*len(t))] = 1  # Pulso centrado
    st.write("**Pulso rectangular:** Duración de 1 segundo")

# ================================
# 🔵 Opción 2: Archivo de audio WAV
# ================================
else:
    uploaded_file = st.sidebar.file_uploader("Suba archivo WAV (5s)", type=["wav"])

    if uploaded_file is not None:
        fs, m = wavfile.read(uploaded_file)
        if len(m.shape) > 1:
            m = m[:, 0]  # Convertir a mono si es estéreo
        t = np.arange(len(m)) / fs
        m = m / np.max(np.abs(m))  # Normalizar la señal
        st.write(f"**Audio cargado:** {uploaded_file.name}")
        st.audio(uploaded_file, format='audio/wav')
    else:
        st.warning("⚠️ Cargue un archivo WAV de máximo 5 segundos.")
        st.stop()

# ================================
# 📈 Mostrar la señal mensaje en el tiempo
# ================================
fig, ax = plt.subplots()
ax.plot(t, m)
ax.set_title("Señal mensaje m(t)")
ax.set_xlabel("Tiempo [s]")
ax.set_ylabel("Amplitud")
ax.grid(True)
st.pyplot(fig)

# ================================
# 📡 Modulación SSB-AM usando señal analítica
# ================================
analytic_signal = hilbert(m)
ssb = np.real(
    m * np.cos(2 * np.pi * fc * t) -
    np.imag(analytic_signal) * np.sin(2 * np.pi * fc * t)
)

# ================================
# 🔍 Cálculo del espectro de la señal mensaje y SSB
# ================================
M_f = np.abs(fft(m))
S_f = np.abs(fft(ssb))
freqs = fftfreq(len(m), 1/fs)

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(freqs[:len(freqs)//2], M_f[:len(M_f)//2])
    ax1.set_title("Espectro de la señal mensaje")
    ax1.set_xlabel("Frecuencia [Hz]")
    ax1.set_ylabel("Magnitud")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(freqs[:len(freqs)//2], S_f[:len(S_f)//2])
    ax2.set_title("Espectro de la señal SSB-AM")
    ax2.set_xlabel("Frecuencia [Hz]")
    ax2.set_ylabel("Magnitud")
    st.pyplot(fig2)

# ================================
# 🧩 Demodulación coherente
# ================================
demod = ssb * np.cos(2 * np.pi * fc * t) * 2

# ================================
# 🔻 Filtro pasa bajos Butterworth
# ================================
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    norm_cutoff = cutoff / nyq
    b, a = butter(order, norm_cutoff, btype='low')
    y = lfilter(b, a, data)
    return y, b, a

cutoff = 1500  # Frecuencia de corte del LPF
demod_filtered, b, a = butter_lowpass_filter(demod, cutoff=cutoff, fs=fs, order=5)

# ================================
# 📈 Señal demodulada en el tiempo
# ================================
fig3, ax3 = plt.subplots()
ax3.plot(t, demod_filtered)
ax3.set_title("Señal demodulada (recuperada)")
ax3.set_xlabel("Tiempo [s]")
ax3.set_ylabel("Amplitud")
st.pyplot(fig3)

# ================================
# 📉 Espectro de la señal demodulada
# ================================
Demod_f = np.abs(fft(demod_filtered))
fig5, ax5 = plt.subplots()
ax5.plot(freqs[:len(freqs)//2], Demod_f[:len(Demod_f)//2])
ax5.set_title("Espectro de la señal demodulada")
ax5.set_xlabel("Frecuencia [Hz]")
ax5.set_ylabel("Magnitud")
st.pyplot(fig5)

# ================================
# 🔘 Plano de polos y ceros del filtro
# ================================
z, p, k = tf2zpk(b, a)
fig6, ax6 = plt.subplots()
ax6.plot(np.real(z), np.imag(z), 'go', label='Ceros')
ax6.plot(np.real(p), np.imag(p), 'rx', label='Polos')
ax6.set_title("Plano de Polos y Ceros del filtro IIR")
ax6.set_xlabel("Re")
ax6.set_ylabel("Im")
ax6.grid(True)
ax6.legend()
st.pyplot(fig6)

# ================================
# 📈 Diagrama de Bode
# ================================
w, h = freqz(b, a, worN=8000)
frequencies = w * fs / (2 * np.pi)
fig_bode, ax_bode = plt.subplots()
ax_bode.plot(frequencies, 20 * np.log10(abs(h)))
ax_bode.set_title("Diagrama de Bode del filtro IIR")
ax_bode.set_xlabel("Frecuencia [Hz]")
ax_bode.set_ylabel("Ganancia [dB]")
ax_bode.grid()
st.pyplot(fig_bode)

# ================================
# ✅ Mensaje final
# ================================
st.success("✅ Modulación y demodulación SSB-AM completadas con visualización de filtros.")
