
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import control as ctrl
import plotly.graph_objects as go

st.set_page_config(page_title="Simulación MRA - Streamlit", layout="wide")

st.title("🔧 Simulador Interactivo de Sistemas Masa-Resorte-Amortiguador (MRA)")

# Parámetros ajustables por el usuario
st.sidebar.header("⚙️ Parámetros del sistema")

tipo = st.sidebar.selectbox("Tipo de respuesta:", ["Subamortiguada", "Sobreamortiguada", "Amortiguamiento crítico", "Inestable"])

if tipo == "Subamortiguada":
    zeta = st.sidebar.slider("Factor de amortiguamiento (ζ)", 0.01, 0.99, 0.5)
elif tipo == "Sobreamortiguada":
    zeta = st.sidebar.slider("Factor de amortiguamiento (ζ)", 1.01, 5.0, 2.0)
elif tipo == "Amortiguamiento crítico":
    zeta = 1.0
    st.sidebar.write("ζ = 1 (amortiguamiento crítico)")
else:
    zeta = st.sidebar.slider("Factor de amortiguamiento (ζ)", -5.0, -0.01, -0.5)

wn = st.sidebar.slider("Frecuencia natural (ωₙ)", 0.1, 20.0, 5.0)

# Función de transferencia
num = [wn**2]
den = [1, 2*zeta*wn, wn**2]
sistema = ctrl.TransferFunction(num, den)

# Cálculo de parámetros temporales
info = ctrl.step_info(sistema)

# Estimación de componentes mecánicos y eléctricos
m = 1
k = wn**2 * m
c = 2 * zeta * wn * m
L = m
R = c
C = 1 / k

# Visualizaciones
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Respuesta al Escalón")
    t, y = ctrl.step_response(sistema)
    fig, ax = plt.subplots()
    ax.plot(t, y)
    ax.set_title("Respuesta al Escalón")
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Salida")
    st.pyplot(fig)

with col2:
    st.subheader("🎯 Parámetros Temporales")
    st.write(f"**Tiempo de subida:** {info['RiseTime']:.3f} s")
    st.write(f"**Tiempo de establecimiento:** {info['SettlingTime']:.3f} s")
    st.write(f"**Sobreimpulso:** {info['Overshoot']:.2f} %")
    st.write(f"**Tiempo del sobreimpulso:** {info['PeakTime']:.3f} s")
    st.write(f"**Valor pico:** {info['Peak']:.3f}")

st.subheader("📊 Diagrama de Bode")
mag, phase, omega = ctrl.bode(sistema, dB=True, Plot=False)
fig_bode = go.Figure()
fig_bode.add_trace(go.Scatter(x=omega, y=20*np.log10(mag), mode='lines', name='Magnitud (dB)'))
fig_bode.add_trace(go.Scatter(x=omega, y=np.degrees(phase), mode='lines', name='Fase (°)'))
fig_bode.update_layout(xaxis_title='Frecuencia [rad/s]', yaxis_title='Magnitud / Fase', height=400)
st.plotly_chart(fig_bode, use_container_width=True)

st.subheader("🌀 Diagrama de Polos y Ceros")
fig_pz, ax_pz = plt.subplots()
ctrl.pzmap(sistema, Plot=True, ax=ax_pz)
st.pyplot(fig_pz)

st.subheader("📦 Estimación de Componentes Equivalentes")
st.latex(f"\text{{Masa }} m = {m:.2f}")
st.latex(f"\text{{Amortiguador }} c = {c:.2f}")
st.latex(f"\text{{Resorte }} k = {k:.2f}")
st.latex(f"\text{{Inductor }} L = {L:.2f}")
st.latex(f"\text{{Resistencia }} R = {R:.2f}")
st.latex(f"\text{{Capacitor }} C = {C:.4f}")
