{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOuwG6aiqVBMW49czDK1H5d",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/AndresChavez123/SenalesySistemas/blob/main/potencia_streamlit.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 385
        },
        "id": "YZW3Qr0T6HnT",
        "outputId": "e2ef75d2-1e3b-4b4c-8e90-a31c08a42795"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'streamlit'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-1-3598943733>\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mnumpy\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mnp\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mmatplotlib\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpyplot\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mplt\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mtitle\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"Simulación de Potencia en Circuitos Eléctricos AC\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "import streamlit as st\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "st.title(\"Simulación de Potencia en Circuitos Eléctricos AC\")\n",
        "\n",
        "# Entradas de usuario\n",
        "V = st.slider(\"Tensión (V)\", 0, 250, 120)\n",
        "I = st.slider(\"Corriente (A)\", 0, 20, 5)\n",
        "phi_deg = st.slider(\"Ángulo de fase φ (grados)\", 0, 90, 30)\n",
        "phi = np.radians(phi_deg)\n",
        "\n",
        "# Cálculos de potencia\n",
        "P = V * I * np.cos(phi)\n",
        "Q = V * I * np.sin(phi)\n",
        "S = V * I\n",
        "fp = np.cos(phi)\n",
        "\n",
        "# Mostrar resultados\n",
        "st.metric(\"Potencia Activa (P) [W]\", f\"{P:.2f}\")\n",
        "st.metric(\"Potencia Reactiva (Q) [VAR]\", f\"{Q:.2f}\")\n",
        "st.metric(\"Potencia Aparente (S) [VA]\", f\"{S:.2f}\")\n",
        "st.metric(\"Factor de Potencia (cos φ)\", f\"{fp:.2f}\")\n",
        "\n",
        "# Triángulo de potencias\n",
        "fig, ax = plt.subplots()\n",
        "ax.arrow(0, 0, P, 0, head_width=5, head_length=5, fc='green', ec='green')\n",
        "ax.arrow(0, 0, 0, Q, head_width=5, head_length=5, fc='red', ec='red')\n",
        "ax.arrow(0, 0, P, Q, head_width=5, head_length=5, fc='blue', ec='blue')\n",
        "ax.set_xlim(0, max(P, S)+20)\n",
        "ax.set_ylim(0, max(Q, S)+20)\n",
        "ax.set_xlabel(\"Potencia Activa (W)\")\n",
        "ax.set_ylabel(\"Potencia Reactiva (VAR)\")\n",
        "ax.grid(True)\n",
        "st.pyplot(fig)\n"
      ]
    }
  ]
}