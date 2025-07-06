
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import control

# ────────────────────────────────────────────────────────
# Configuración general
# ────────────────────────────────────────────────────────
st.set_page_config(page_title="Simulación MRS / RLC", layout="wide")
st.title("Panel interactivo: Masa‑Resorte‑Amortiguador ⇄ Circuito RLC")

# ────────────────────────────────────────────────────────
# Barra lateral: selección de tipo de respuesta y parámetros
# ────────────────────────────────────────────────────────
st.sidebar.header("Parámetros del sistema")

resp_map = {
    "Subamortiguada (0 < ζ < 1)": 0.3,
    "Sobreamortiguada (ζ > 1)":     1.5,
    "Críticamente amortiguada (ζ = 1)": 1.0,
    "Inestable (ζ < 0)":           -0.2,
}
resp_type = st.sidebar.selectbox("Tipo de respuesta", list(resp_map.keys()))
default_zeta = resp_map[resp_type]
zeta = st.sidebar.slider("ζ (factor de amortiguamiento)", -0.5, 2.5, default_zeta, step=0.05)
wn   = st.sidebar.slider("ωₙ (rad/s)", 1.0, 50.0, 5.0)

# ────────────────────────────────────────────────────────
# Función de transferencia (lazo abierto)
# ────────────────────────────────────────────────────────
num = [1.0]
den = [1.0, 2*zeta*wn, wn**2]
G   = control.TransferFunction(num, den)

st.subheader("Función de transferencia (lazo abierto)")
st.latex(r"H(s)=\dfrac{1}{s^{2}+2\zeta\omega_n s+\omega_n^{2}}")
st.write(f"Denominador numérico: {den}")

# ────────────────────────────────────────────────────────
# Respuestas temporales
# ────────────────────────────────────────────────────────
T_end = 10/wn         # horizonte hasta ~5 períodos
T     = np.linspace(0, T_end, 1000)
t_step, y_step     = control.step_response(G, T)
t_imp , y_imp      = control.impulse_response(G, T)

# ────────────────────────────────────────────────────────
# Bode (mag, phase, ω)
# ────────────────────────────────────────────────────────
mag, phase, omega  = control.bode(G, dB=True, Plot=False)
mag   = np.squeeze(mag)
phase = np.squeeze(phase)

# ────────────────────────────────────────────────────────
# Polos y ceros
# ────────────────────────────────────────────────────────
poles = control.pole(G)
zeros = control.zero(G)

# ────────────────────────────────────────────────────────
# Gráficas
# ────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Respuesta al escalón")
    fig1, ax1 = plt.subplots()
    ax1.plot(t_step, y_step)
    ax1.set_xlabel("t [s]");  ax1.set_ylabel("Salida")
    ax1.grid(True)
    st.pyplot(fig1)

with col2:
    st.subheader("Respuesta al impulso")
    fig2, ax2 = plt.subplots()
    ax2.plot(t_imp, y_imp)
    ax2.set_xlabel("t [s]");  ax2.set_ylabel("Salida")
    ax2.grid(True)
    st.pyplot(fig2)

st.subheader("Diagrama de Bode")
fig3, (axm, axp) = plt.subplots(2, 1, figsize=(6,6))
axm.semilogx(omega, 20*np.log10(mag)); axm.set_ylabel("Magnitud [dB]"); axm.grid(True, which="both")
axp.semilogx(omega, np.degrees(phase)); axp.set_xlabel("ω [rad/s]"); axp.set_ylabel("Fase [°]"); axp.grid(True, which="both")
st.pyplot(fig3)

st.subheader("Polos y ceros")
fig4, ax4 = plt.subplots()
ax4.scatter(np.real(poles), np.imag(poles), marker="x", color="red", label="Polos")
if zeros.size:
    ax4.scatter(np.real(zeros), np.imag(zeros), marker="o", facecolors="none", edgecolors="blue", label="Ceros")
ax4.axhline(0, color="black"); ax4.axvline(0, color="black")
ax4.set_xlabel("Re{s}"); ax4.set_ylabel("Im{s}")
ax4.grid(True);  ax4.legend()
st.pyplot(fig4)

# ────────────────────────────────────────────────────────
# Parámetros temporales (step_info)
# ────────────────────────────────────────────────────────
try:
    info = control.step_info(G)
    st.subheader("Parámetros temporales")
    st.write({k: round(v, 4) for k, v in info.items()})
except Exception as e:
    st.warning(f"No se pudo calcular step_info: {e}")

# ────────────────────────────────────────────────────────
# Equivalencia mecánico ⟷ eléctrico
# ────────────────────────────────────────────────────────
m = 1.0
c = 2*zeta*wn*m
k = wn**2*m
C = 1.0
L = m / C
R = np.inf if c==0 else 2*L / c

st.subheader("Equivalencia componentes MRS ↔ RLC")
st.markdown(f"""
**Mecánico**  
- m = {m:.2f} kg  
- c = {c:.2f} N s/m  
- k = {k:.2f} N/m  

**Eléctrico equivalente**  
- R = {'∞' if R==np.inf else f'{R:.2f} Ω'}  
- L = {L:.2f} H  
- C = {C:.2f} F
""")
