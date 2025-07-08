# ================================
# 📦 Importación de librerías
# ================================
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import plotly.graph_objects as go
from scipy import signal

# ================================
# ⚙️ Configuración de la aplicación
# ================================
st.set_page_config(page_title="Simulación MRA - Streamlit", layout="wide")
st.title("🔧 Simulador Interactivo de Sistemas Masa-Resorte-Amortiguador (MRA)")

# ================================
# 🎛️ Panel lateral para parámetros
# ================================
st.sidebar.header("⚙️ Parámetros del sistema")

# Selección del tipo de respuesta
tipo = st.sidebar.selectbox("Tipo de respuesta:",
                            ["Subamortiguada", "Sobreamortiguada", "Amortiguamiento crítico", "Inestable"])

# Parámetros según tipo
if tipo == "Subamortiguada":
    zeta = st.sidebar.slider("Factor de amortiguamiento (ζ)", 0.01, 0.99, 0.5)
elif tipo == "Sobreamortiguada":
    zeta = st.sidebar.slider("Factor de amortiguamiento (ζ)", 1.01, 5.0, 2.0)
elif tipo == "Amortiguamiento crítico":
    zeta = 1.0
    st.sidebar.write("ζ = 1 (amortiguamiento crítico)")
else:
    zeta = st.sidebar.slider("Factor de amortiguamiento (ζ)", -5.0, -0.01, -0.5)

# Frecuencia natural
wn = st.sidebar.slider("Frecuencia natural (ωₙ)", 0.1, 20.0, 5.0)

# Selección de lazo abierto o cerrado
lazo = st.sidebar.selectbox("Configuración del sistema:", ["Lazo Abierto", "Lazo Cerrado"])

# ================================
# 🔁 Función de transferencia
# ================================
num = [wn**2]
den = [1, 2*zeta*wn, wn**2]
sistema = ctrl.TransferFunction(num, den)

if lazo == "Lazo Cerrado":
    sistema = ctrl.feedback(sistema, 1)

# ================================
# 📐 Cálculo de parámetros temporales
# ================================
info = ctrl.step_info(sistema)

# ================================
# 🔁 Cálculo de componentes equivalentes
# ================================
m = 1
k = wn**2 * m
c = 2 * zeta * wn * m
L = m
R = c
C = 1 / k

# ================================
# 📈 Respuesta al Escalón
# ================================
st.subheader("📈 Respuesta al Escalón")
t_step, y_step = ctrl.step_response(sistema)
fig_step, ax_step = plt.subplots()
ax_step.plot(t_step, y_step)
ax_step.set_title("Respuesta al Escalón")
ax_step.set_xlabel("Tiempo [s]")
ax_step.set_ylabel("Salida")
st.pyplot(fig_step)

# ================================
# ⚡ Respuesta al Impulso
# ================================
st.subheader("⚡ Respuesta al Impulso")
t_imp, y_imp = ctrl.impulse_response(sistema)
fig_imp, ax_imp = plt.subplots()
ax_imp.plot(t_imp, y_imp)
ax_imp.set_title("Respuesta al Impulso")
ax_imp.set_xlabel("Tiempo [s]")
ax_imp.set_ylabel("Salida")
st.pyplot(fig_imp)

# ================================
# 🟢 Respuesta a la Rampa
# ================================
st.subheader("📈 Respuesta a la Rampa")
t_rampa = np.linspace(0, 10, 500)
u_rampa = t_rampa
t_out, y_rampa, _ = ctrl.forced_response(sistema, T=t_rampa, U=u_rampa)
fig_rampa, ax_rampa = plt.subplots()
ax_rampa.plot(t_out, y_rampa)
ax_rampa.set_title("Respuesta a la Rampa")
ax_rampa.set_xlabel("Tiempo [s]")
ax_rampa.set_ylabel("Salida")
st.pyplot(fig_rampa)

# ================================
# 🎯 Parámetros Temporales
# ================================
st.subheader("🎯 Parámetros Temporales")
st.write(f"**Tiempo de subida:** {info['RiseTime']:.3f} s")
st.write(f"**Tiempo de establecimiento:** {info['SettlingTime']:.3f} s")
st.write(f"**Sobreimpulso:** {info['Overshoot']:.2f} %")
st.write(f"**Tiempo del sobreimpulso:** {info['PeakTime']:.3f} s")
st.write(f"**Valor pico:** {info['Peak']:.3f}")

# ================================
# 📊 Diagrama de Bode
# ================================
st.subheader("📊 Diagrama de Bode")
w = np.logspace(-1, 2, 500)
w, mag, phase = signal.bode(signal.TransferFunction(num, den), w=w)
fig_bode = go.Figure()
fig_bode.add_trace(go.Scatter(x=w, y=mag, mode='lines', name='Magnitud (dB)'))
fig_bode.add_trace(go.Scatter(x=w, y=phase, mode='lines', name='Fase (°)'))
fig_bode.update_layout(title="Diagrama de Bode",
                       xaxis_title='Frecuencia [rad/s]',
                       yaxis_title='Magnitud / Fase',
                       height=400)
st.plotly_chart(fig_bode, use_container_width=True)

# ================================
# 🌀 Diagrama de Polos y Ceros
# ================================
st.subheader("🌀 Diagrama de Polos y Ceros")
fig_pz, ax_pz = plt.subplots()
ctrl.pzmap(sistema, ax=ax_pz, grid=True)
st.pyplot(fig_pz)

# ================================
# 📦 Componentes físicos y eléctricos
# ================================
st.subheader("📦 Estimación de Componentes Equivalentes")
st.latex(f"\\text{{Masa }}\\ m = {m:.2f}")
st.latex(f"\\text{{Amortiguador }}\\ c = {c:.2f}")
st.latex(f"\\text{{Resorte }}\\ k = {k:.2f}")
st.latex(f"\\text{{Inductor }}\\ L = {L:.2f}")
st.latex(f"\\text{{Resistencia }}\\ R = {R:.2f}")
st.latex(f"\\text{{Capacitor }}\\ C = {C:.4f}")
