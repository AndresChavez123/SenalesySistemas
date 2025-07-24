
# 📡 Proyecto Final – Señales y Sistemas 2025

### **"Análisis y Simulación Interactiva de Señales Digitales Modernas (WiFi / 5G)"**

Este repositorio contiene un conjunto de **dashboards interactivos construidos con Streamlit en Google Colab**, orientados a la **visualización, simulación y comprensión de conceptos clave de procesamiento de señales** y sistemas de comunicación digital.

---

## 🎯 Objetivo del Proyecto

Ofrecer una plataforma educativa modular para que los estudiantes puedan experimentar de forma visual e interactiva con los fundamentos de señales y sistemas. Cada módulo aborda un tema fundamental desde la teoría hasta su aplicación práctica en contextos como la modulación QAM y la transmisión OFDM.

---

## 📦 Estructura del Proyecto

Este proyecto está dividido en **bloques o pestañas**, cada uno alojado en un archivo `.py` ejecutado de forma independiente desde Google Colab mediante `streamlit_jupyter`.

Cada archivo genera una app Streamlit que se ejecuta **dentro de Colab** y se accede mediante un túnel `cloudflared`.

---

## 📁 Módulos incluidos

### 1. 📝 `📝_Proy_Fin.py` – Página principal del Dashboard

- Presentación del proyecto
- Propósito general y créditos
- Navegación sugerida
- Inspirado en WiFi/5G y el curso de Señales

---

### 2. 📊 `📊_Dominio_Frecuencia.py`

- Construcción de señales seno/coseno
- Análisis espectral con FFT
- Visualización en el dominio del tiempo y la frecuencia
- Ideal para comenzar el recorrido teórico

---
### 4. 💠 `💠_Modulacion_QAM.py`

- Generación de bits aleatorios
- Modulación 16-QAM / 64-QAM
- Diagrama de constelación
- Simulación de canal con ruido (AWGN)

---

### 5. 🌐 `🌐_Sistema_Completo.py`

- Transmisor completo: bits → I/Q → canal
- Canal ruidoso: AWGN
- Receptor: demodulación coherente
- Comparación de señales transmitidas vs recibidas

---

### 6. 🔊 `🔊_Audio_Filtrado.py` (opcional)

- Análisis de señales reales (audio `.wav`)
- Aplicación de filtros digitales paso-bajo
- Visualización de espectros
- Ideal para ver el efecto del filtrado en datos reales

---

## 🚀 Instrucciones de Ejecución en Google Colab

1. **Abrir cada archivo en Colab** (como notebook)
2. Ejecutar los siguientes bloques al principio:

```python
!pip install streamlit streamlit_jupyter control soundfile yt-dlp -q
```

3. Luego, en cada bloque de código principal, guardar el contenido del módulo:

```python
%%writefile 📝_Proy_Fin.py
# (Pega aquí el contenido del módulo principal)
```

4. Ejecuta el túnel Streamlit con:

```python
!wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
!chmod +x cloudflared-linux-amd64
!mv cloudflared-linux-amd64 /usr/local/bin/cloudflared

!streamlit run 📝_Proy_Fin.py &>/content/logs.txt &
!cloudflared tunnel --url http://localhost:8501 > /content/cloudflared.log 2>&1 &

import time, re
time.sleep(5)
with open('/content/cloudflared.log') as f:
    for line in f:
        if 'https://' in line:
            url = re.search(r'https?://\S+', line).group(0)
            print(f'🔗 Enlace de tu app: {url}')
            break
```

---

## 🧩 Librerías utilizadas

| Librería         | Uso principal |
|------------------|----------------|
| `streamlit`      | Interfaces gráficas |
| `streamlit_jupyter` | Integración con Google Colab |
| `control`        | Análisis de sistemas dinámicos |
| `soundfile`      | Lectura de archivos de audio |
| `yt-dlp`         | Descarga de videos o audios de YouTube |
| `numpy`, `matplotlib`, `scipy` | Procesamiento y visualización numérica |

---

## 🏫 Créditos Académicos

- **Curso:** Señales y Sistemas – 2025  
- **Profesor:** Dr. Andrés Marino Álvarez Meza  
- **Universidad:** Nacional de Colombia – Sede Manizales  
- **Autores del Dashboard:** Estudiantes de Ingeniería Eléctrica / Electrónica  

---

## 💡 Inspiración

Este trabajo busca integrar herramientas modernas como Streamlit y Google Colab en la enseñanza de ingeniería, demostrando cómo los principios matemáticos permiten comprender y simular tecnologías avanzadas como **WiFi, LTE y 5G**.

---

## ✅ Recomendaciones Finales

- Ejecuta un módulo por bloque
- Asegúrate de tener los permisos para instalar dependencias
- Copia el enlace generado por Cloudflare para abrir tu app
- Explora los conceptos paso a paso desde la pestaña inicial

---

### 🎓 ¡A experimentar, simular y aprender!
