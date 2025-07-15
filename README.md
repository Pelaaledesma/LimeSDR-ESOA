# LimeSDR-ESOA

# LimeSDR – Aplicación en Python

**Curso de Comunicantes – Escuela de Oficiales de la Armada Argentina**

Este repositorio contiene un programa en Python desarrollado para ser utilizado junto a la plataforma **LimeSDR**, como parte de los contenidos del curso de Comunicantes. El objetivo es introducir a los cursantes en el uso práctico de radio definida por software (SDR) mediante la captura, transmisión y análisis de señales.

---

## 📡 ¿Qué es LimeSDR?

**LimeSDR** es un transceptor SDR flexible y de código abierto, capaz de operar desde 100 kHz hasta 3.8 GHz. Se puede utilizar para experimentar con tecnologías como FM, AM, LTE, GSM, ADS-B, y más.

---

## 🧠 Objetivo del Proyecto

- Aplicar conocimientos de comunicaciones y señales en un entorno real.
- Interactuar directamente con hardware SDR desde Python.
- Comprender la cadena de transmisión y recepción de señales digitales.
- Fomentar el desarrollo de soluciones personalizadas en comunicaciones militares.

---

## 🛠️ Requisitos

- **Hardware**: LimeSDR-USB o LimeSDR-Mini
- **Sistema operativo**: Windows 10/11 (64-bit)
- **Software**:
  - [Python 3.9](https://www.python.org/downloads/release/python-390/)
  - [Pothos SDR Suite](https://downloads.myriadrf.org/builds/PothosSDR/)
  - Paquetes Python:
    - `numpy`
    - `scipy`
    - `matplotlib`
    - `SoapySDR`

---

## 📦 Instalación

1. Instalar [PothosSDR](https://downloads.myriadrf.org/builds/PothosSDR/)
2. Agregar `C:\Program Files\PothosSDR\bin` al PATH del sistema.
3. Instalar Python 3.9 y los módulos necesarios:
   ```bash
   pip install numpy scipy matplotlib SoapySDR
   ```
