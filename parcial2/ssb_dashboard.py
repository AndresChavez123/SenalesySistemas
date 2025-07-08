
# ================================
# 📦 Importación de librerías necesarias
# ================================
import streamlit as st  # Para crear la interfaz web
import numpy as np      # Para operaciones numéricas
import matplotlib.pyplot as plt  # Para graficar
from scipy.signal import hilbert, butter, lfilter  # Para modulación y filtrado
from scipy.fft import fft, fftfreq  # Análisis espectral
from scipy.io import wavfile  # Lectura de archivos de audio WAV

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
        st.audio(uploaded_file, format='audio/wav')  # Reproductor de audio

    else:
        st.warning("⚠️ Cargue un archivo WAV de máximo 5 segundos.")
        st.stop()  # Detiene ejecución si no hay archivo

# ================================
# 📈 Mostrar la señal mensaje en el tiempo
# ================================
fig, ax = plt.subplots()
ax.plot(t, m)
ax.set_title("Señal mensaje m(t)")
ax.set_xlabel("Tiempo [s]")
ax.set_ylabel("Amplitud")
ax.set_xlim([0, duration])
ax.set_ylim([-0.2, 1.2])
ax.grid(True)
st.pyplot(fig)

# ================================
# 📡 Modulación SSB-AM usando señal analítica
# ================================
analytic_signal = hilbert(m)  # Crea la señal analítica (compleja)
ssb = np.real(
    m * np.cos(2 * np.pi * fc * t) -
    np.imag(analytic_signal) * np.sin(2 * np.pi * fc * t)
)

# ================================
# 🔍 Cálculo del espectro de la señal mensaje y modulada
# ================================
M_f = np.abs(fft(m))
S_f = np.abs(fft(ssb))
freqs = fftfreq(len(m), 1/fs)

# ================================
# 📊 Mostrar espectros en dos columnas
# ================================
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
# 🧩 Demodulación coherente (multiplicación por coseno)
# ================================
demod = ssb * np.cos(2 * np.pi * fc * t) * 2  # Multiplicación coherente

# ================================
# 🔻 Filtro pasa bajos para recuperar la señal mensaje
# ================================
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs  # Frecuencia de Nyquist
    norm_cutoff = cutoff / nyq
    b, a = butter(order, norm_cutoff, btype='low')  # Diseño del filtro
    y = lfilter(b, a, data)  # Aplicación del filtro
    return y

# Aplicar el filtro
demod_filtered = butter_lowpass_filter(demod, cutoff=1500, fs=fs, order=5)

# ================================
# 📈 Mostrar la señal demodulada
# ================================
fig3, ax3 = plt.subplots()
ax3.plot(t, demod_filtered)
ax3.set_title("Señal demodulada")
ax3.set_xlabel("Tiempo [s]")
ax3.set_ylabel("Amplitud")
st.pyplot(fig3)

# ================================
# ✅ Mensaje final
# ================================
st.success("✅ Modulación y demodulación SSB-AM completadas.")

