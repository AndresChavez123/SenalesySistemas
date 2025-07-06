
# Simulador Interactivo de Sistemas Masa-Resorte-Amortiguador (MRA)

Este proyecto es una aplicación interactiva creada con **Streamlit** para simular el comportamiento de un sistema masa-resorte-amortiguador (MRA), muy común en sistemas mecánicos y eléctricos.

## 🚀 Funcionalidades

- Visualización de la **respuesta al escalón** del sistema MRA
- Cálculo de **parámetros temporales**: tiempo de subida, sobreimpulso, tiempo de establecimiento, etc.
- Visualización del **diagrama de Bode** (magnitud y fase)
- **Diagrama de polos y ceros**
- Estimación de **componentes mecánicos y su equivalencia eléctrica** (masa, resorte, amortiguador → RLC)
- Control total del **tipo de respuesta**:
  - Subamortiguada
  - Sobreamortiguada
  - Amortiguamiento crítico
  - Inestable

## 🧪 Requisitos

Asegúrate de tener Python instalado y crea tu entorno virtual. Luego instala las dependencias:

```bash
pip install -r requirements.txt
```

## ▶️ Cómo ejecutar la aplicación

```bash
streamlit run mra_dashboard.py
```

También puedes desplegar esta app directamente en [Streamlit Cloud](https://streamlit.io/cloud) subiendo los archivos `mra_dashboard.py` y `requirements.txt` a tu repositorio.

## 📦 Estructura del proyecto

```
.
├── mra_dashboard.py     # Código principal de la app Streamlit
├── requirements.txt     # Lista de dependencias
└── README.md            # Este archivo
```

## ✏️ Autor

Proyecto desarrollado para fines académicos en el área de **Sistemas y Señales**.

