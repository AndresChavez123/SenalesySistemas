
# ================================
# 📦 Importación de librerías
# ================================
import streamlit as st  # Librería para construir aplicaciones web interactivas
import numpy as np      # Librería para operaciones numéricas
import matplotlib.pyplot as plt  # Para gráficas estáticas
import control as ctrl   # Análisis y diseño de sistemas de control
import plotly.graph_objects as go  # Gráficos interactivos
from scipy import signal  # Procesamiento de señales y funciones de sistemas

# ================================
# ⚙️ Configuración de la aplicación
# ================================
st.set_page_config(page_title="Simulación MRA - Streamlit", layout="wide")
st.title("🔧 Simulador Interactivo de Sistemas Masa-Resorte-Amortiguador (MRA)")

# ================================
# 🎛️ Panel lateral para parámetros del sistema
# ================================
st.sidebar.header("⚙️ Parámetros del sistema")

# Selección del tipo de respuesta del sistema
tipo = st.sidebar.selectbox("Tipo de respuesta:", 
                            ["Subamortiguada", "Sobreamortiguada", "Amortiguamiento crítico", "Inestable"])

# Ajuste del factor de amortiguamiento ζ según el tipo seleccionado
if tipo == "Subamortiguada":
    zeta = st.sidebar.slider("Factor de amortiguamiento (ζ)", 0.01, 0.99, 0.5)
elif tipo == "Sobreamortiguada":
    zeta = st.sidebar.slider("Factor de amortiguamiento (ζ)", 1.01, 5.0, 2.0)
elif tipo == "Amortiguamiento crítico":
    zeta = 1.0
    st.sidebar.write("ζ = 1 (amortiguamiento crítico)")
else:  # Inestable
    zeta = st.sidebar.slider("Factor de amortiguamiento (ζ)", -5.0, -0.01, -0.5)

# Frecuencia natural del sistema (rad/s)
wn = st.sidebar.slider("Frecuencia natural (ωₙ)", 0.1, 20.0, 5.0)

# ================================
# 🔁 Función de transferencia del sistema MRA
# ================================
# Se define el sistema de segundo orden clásico: G(s) = wn^2 / (s^2 + 2ζwns + wn^2)
num = [wn**2]
den = [1, 2*zeta*wn, wn**2]
sistema = ctrl.TransferFunction(num, den)

# ================================
# 📐 Cálculo de parámetros temporales
# ================================
# Calcula tiempos de subida, pico, sobreimpulso, establecimiento, etc.
info = ctrl.step_info(sistema)

# ================================
# 🔁 Cálculo de componentes equivalentes
# ================================
# Se asume masa m = 1 para simplificar cálculos
m = 1
k = wn**2 * m       # Constante del resorte
c = 2 * zeta * wn * m  # Coeficiente del amortiguador

# Analogía eléctrica RLC serie
L = m
R = c
C = 1 / k

# ================================
# 📈 Visualización: Respuesta al escalón
# ================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Respuesta al Escalón")
    t, y = ctrl.step_response(sistema)  # Simulación de la respuesta al escalón
    fig, ax = plt.subplots()
    ax.plot(t, y)
    ax.set_title("Respuesta al Escalón")
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Salida")
    st.pyplot(fig)  # Muestra la figura en Streamlit

# ================================
# 🧮 Visualización: Parámetros temporales
# ================================
with col2:
    st.subheader("🎯 Parámetros Temporales")
    st.write(f"**Tiempo de subida:** {info['RiseTime']:.3f} s")
    st.write(f"**Tiempo de establecimiento:** {info['SettlingTime']:.3f} s")
    st.write(f"**Sobreimpulso:** {info['Overshoot']:.2f} %")
    st.write(f"**Tiempo del sobreimpulso:** {info['PeakTime']:.3f} s")
    st.write(f"**Valor pico:** {info['Peak']:.3f}")

# ================================
# 📊 Visualización: Diagrama de Bode
# ================================
st.subheader("📊 Diagrama de Bode")

# Cálculo del Bode usando scipy (porque control.bode no es compatible con Plotly fácilmente)
w = np.logspace(-1, 2, 500)  # Frecuencia logarítmica
w, mag, phase = signal.bode(signal.TransferFunction(num, den), w=w)

# Gráfico interactivo con Plotly
fig_bode = go.Figure()
fig_bode.add_trace(go.Scatter(x=w, y=mag, mode='lines', name='Magnitud (dB)'))
fig_bode.add_trace(go.Scatter(x=w, y=phase, mode='lines', name='Fase (°)'))
fig_bode.update_layout(
    title="Diagrama de Bode", 
    xaxis_title='Frecuencia [rad/s]', 
    yaxis_title='Magnitud / Fase', 
    height=400
)
st.plotly_chart(fig_bode, use_container_width=True)

# ================================
# 🌀 Visualización: Polos y ceros
# ================================
st.subheader("🌀 Diagrama de Polos y Ceros")
plt.figure()
ctrl.pzmap(sistema)  # Diagrama de polos y ceros del sistema
st.pyplot(plt)       # Muestra en Streamlit

# ================================
# 📦 Visualización: Componentes físicos y eléctricos equivalentes
# ================================
st.subheader("📦 Estimación de Componentes Equivalentes")

# Mostramos en notación LaTeX los componentes estimados
st.latex(f"\\text{{Masa }}\\ m = {m:.2f}")
st.latex(f"\\text{{Amortiguador }}\\ c = {c:.2f}")
st.latex(f"\\text{{Resorte }}\\ k = {k:.2f}")
st.latex(f"\\text{{Inductor }}\\ L = {L:.2f}")
st.latex(f"\\text{{Resistencia }}\\ R = {R:.2f}")
st.latex(f"\\text{{Capacitor }}\\ C = {C:.4f}")
