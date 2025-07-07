
# ================================
# 📦 Importación de librerías necesarias
# ================================
import streamlit as st  # Para crear la interfaz web
import numpy as np      # Para operaciones numéricas y manejo de señales
import matplotlib.pyplot as plt  # Para graficar en formato estático
from scipy.signal import hilbert, butter, lfilter  # Para modulación SSB y filtrado
from scipy.fft import fft, fftfreq  # Para análisis espectral
from scipy.io import wavfile  # Para leer archivos de audio WAV

# ================================
# ⚙️ Configuración de la aplicación Streamlit
# ================================
st.set_page_config(page_title="SSB-AM Dashboard", layout="wide")
st.title("📡 Dashboard de Modulación y Demodulación SSB-AM")

# ================================
# 🎚️ Parámetros básicos de la señal
# ================================
fs = 8000       # Frecuencia de muestreo por defecto (Hz)
fc = 1000       # Frecuencia de la portadora (Hz)
Ac = 1          # Amplitud de la portadora
duration = 1    # Duración de la señal en segundos (solo para pulso)

# ================================
# 🎵 Opción para seleccionar señal mensaje
# ================================
option = st.sidebar.radio(
    "Seleccione la señal mensaje:",
    ("Pulso rectangular", "Subir archivo de audio (5s)")
)

# ================================
# 🔊 Generación o carga de la señal mensaje
# ================================
if option == "Pulso rectangular":
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)  # Vector de tiempo
    m = np.zeros_like(t)  # Inicializa en cero
    m[int(0.25*len(t)):int(0.75*len(t))] = 1  # Pulso rectangular centrado
    st.write("**Pulso rectangular:** Duración de 1 segundo")

else:
    uploaded_file = st.sidebar.file_uploader("Suba archivo WAV (5s)", type=["wav"])

# Si se carga un archivo, se procesa aquí
if uploaded_file is not None:
    fs, m = wavfile.read(uploaded_file)  # Leer el archivo WAV
    if len(m.shape) > 1:
        m = m[:, 0]  # Convertir a mono si es estéreo
    t = np.arange(len(m)) / fs  # Vector de tiempo
    m = m / np.max(np.abs(m))  # Normalizar la señal entre -1 y 1
    st.write(f"**Audio cargado:** {uploaded_file.name}")

    # 🎧 Reproductor de audio en la app
    st.audio(uploaded_file, format='audio/wav')

else:
    # Si no se carga nada, mostrar advertencia y detener ejecución
    st.warning("⚠️ Cargue un archivo WAV de máximo 5 segundos.")
    st.stop()

# ================================
# 🖼️ Mostrar la señal mensaje en el dominio del tiempo
# ================================
fig, ax = plt.subplots()
ax.plot(t, m)
ax.set_title("Señal mensaje m(t)")
ax.set_xlabel("Tiempo [s]")
ax.set_ylabel("Amplitud")
ax.set_xlim([0, duration])  # Limita el eje x a 1 segundo
ax.set_ylim([-0.2, 1.2])    # Para mejorar la visualización del pulso
ax.grid(True)
st.pyplot(fig)

# ================================
# 📡 Modulación SSB-AM usando la señal analítica de Hilbert
# ================================
# La señal analítica permite eliminar una de las bandas laterales
analytic_signal = hilbert(m)  # Devuelve una señal compleja: parte real + j·parte imaginaria
ssb = np.real(
    m * np.cos(2 * np.pi * fc * t) - 
    np.imag(analytic_signal) * np.sin(2 * np.pi * fc * t)
)

# ================================
# 🔍 Espectro de la señal mensaje
# ================================
M_f = np.abs(fft(m))  # Magnitud del espectro de m(t)
freqs = fftfreq(len(m), 1/fs)  # Vector de frecuencias correspondiente

# 🔍 Espectro de la señal modulada
S_f = np.abs(fft(ssb))

# ================================
# 📊 Mostrar espectros en dos columnas
# ================================
col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(freqs[:len(freqs)//2], M_f[:len(M_f)//2])  # Solo la mitad positiva del espectro
    ax1.set_title("Espectro de la señal mensaje")
    ax1.set_xlabel("Frecuencia [Hz]")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(freqs[:len(freqs)//2], S_f[:len(S_f)//2])
    ax2.set_title("Espectro de la señal SSB-AM")
    ax2.set_xlabel("Frecuencia [Hz]")
    st.pyplot(fig2)

# ================================
# 🔄 Demodulación coherente
# ================================
# Multiplicamos por la misma portadora y por 2 para compensar el escalamiento
demod = ssb * np.cos(2 * np.pi * fc * t) * 2

# ================================
# 🔻 Filtro pasa bajos para eliminar componentes de alta frecuencia
# ================================
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs  # Frecuencia de Nyquist
    norm_cutoff = cutoff / nyq  # Frecuencia normalizada
    b, a = butter(order, norm_cutoff, btype='low')  # Coeficientes del filtro
    y = lfilter(b, a, data)  # Aplicar el filtro
    return y

demod_filtered = butter_lowpass_filter(demod, cutoff=1500, fs=fs, order=5)

# ================================
# 📈 Graficar señal demodulada
# ================================
fig3, ax3 = plt.subplots()
ax3.plot(t, demod_filtered)
ax3.set_title("Señal demodulada")
ax3.set_xlabel("Tiempo [s]")
st.pyplot(fig3)

# ================================
# ✅ Mensaje de éxito final
# ================================
st.success("✅ Modulación y demodulación SSB-AM completadas.")

