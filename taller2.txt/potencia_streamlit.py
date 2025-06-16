
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Simulación de Potencia en Circuitos Eléctricos AC")

# Entradas de usuario
V = st.slider("Tensión (V)", 0, 250, 120)
I = st.slider("Corriente (A)", 0, 20, 5)
phi_deg = st.slider("Ángulo de fase φ (grados)", 0, 90, 30)
phi = np.radians(phi_deg)

# Cálculos de potencia
P = V * I * np.cos(phi)
Q = V * I * np.sin(phi)
S = V * I
fp = np.cos(phi)

# Mostrar resultados
st.metric("Potencia Activa (P) [W]", f"{P:.2f}")
st.metric("Potencia Reactiva (Q) [VAR]", f"{Q:.2f}")
st.metric("Potencia Aparente (S) [VA]", f"{S:.2f}")
st.metric("Factor de Potencia (cos φ)", f"{fp:.2f}")

# Triángulo de potencias
fig, ax = plt.subplots()
ax.arrow(0, 0, P, 0, head_width=5, head_length=5, fc='green', ec='green')
ax.arrow(0, 0, 0, Q, head_width=5, head_length=5, fc='red', ec='red')
ax.arrow(0, 0, P, Q, head_width=5, head_length=5, fc='blue', ec='blue')
ax.set_xlim(0, max(P, S)+20)
ax.set_ylim(0, max(Q, S)+20)
ax.set_xlabel("Potencia Activa (W)")
ax.set_ylabel("Potencia Reactiva (VAR)")
ax.grid(True)
st.pyplot(fig)
