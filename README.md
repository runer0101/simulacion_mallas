# Simulador de Circuitos Eléctricos en Mallas

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

<!-- Inserta aquí una captura de pantalla o un GIF de tu aplicación en funcionamiento -->

## Sinopsis

Este proyecto es una aplicación web interactiva diseñada para la **simulación y optimización de sistemas de distribución de energía en instalaciones residenciales**. Utiliza el método de análisis de mallas para calcular las corrientes en un circuito de tres lazos, representativo de una vivienda con diferentes zonas (por ejemplo, cocina, sala, dormitorios).

La herramienta no solo realiza los cálculos, sino que también sirve como un recurso educativo, mostrando el desglose matemático completo del problema, desde la aplicación de la Ley de Kirchhoff de Voltajes hasta la resolución del sistema de ecuaciones matricial.

El repositorio del proyecto se encuentra en GitHub: [https://github.com/runer0101/simulacion_mallas.git](https://github.com/runer0101/simulacion_mallas.git)

## Características Principales

*   **Simulación Interactiva:** Permite a los usuarios introducir valores personalizados para resistencias y fuentes de voltaje para ver los resultados en tiempo real.
*   **Generación Dinámica de Diagramas:** El esquema del circuito se actualiza visualmente con los valores introducidos, gracias a la generación de imágenes con Matplotlib en el backend.
*   **Validación de Entradas:** El formulario valida los datos en el lado del cliente y del servidor para asegurar que los parámetros sean físicamente realistas y evitar errores.
*   **Desglose Matemático Detallado:** Muestra paso a paso la formulación de las ecuaciones de malla, la construcción de la matriz y la solución final, utilizando MathJax para una representación clara de las fórmulas.
*   **Interpretación de Resultados:** Proporciona un análisis textual de las corrientes calculadas, indicando la dirección y la magnitud de la carga en cada malla.
*   **API RESTful:** Incluye endpoints para realizar cálculos de forma programática y para cargar datos de ejemplo.
*   **Interfaz de Usuario Moderna y Responsiva:** La interfaz está diseñada para ser intuitiva y accesible en diferentes dispositivos, desde ordenadores de escritorio hasta móviles.

## Tecnologías Utilizadas

*   **Backend:**
    *   **Python 3**
    *   **Flask:** Micro-framework para el servidor web y la API.
    *   **NumPy:** Para los cálculos matriciales y la resolución del sistema de ecuaciones lineales.
    *   **Matplotlib:** Para la generación dinámica de los diagramas del circuito.
*   **Frontend:**
    *   **HTML5**
    *   **CSS3:** Para el diseño y la maquetación responsiva.
    *   **JavaScript (ES6):** Para la interactividad del cliente, validación de formularios y llamadas a la API (Fetch).
    *   **Jinja2:** Motor de plantillas para renderizar el contenido dinámico en el HTML.
    *   **MathJax:** Para renderizar ecuaciones matemáticas en formato LaTeX.

## Estructura del Proyecto

```
simulacion_mallas/
├── app.py                  # Lógica principal de la aplicación Flask, rutas y cálculos.
├── static/
│   ├── styles.css          # Hoja de estilos principal.
│   └── main.js             # Scripts del lado del cliente (validación, API, etc.).
├── templates/
│   └── index.html          # Plantilla principal de la aplicación (HTML con Jinja2).
└── README.md               # Este archivo.
```

## Instalación y Ejecución Local

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

**Prerrequisitos:**
*   Python 3.8 o superior
*   `pip` y `venv`

**1. Clonar el Repositorio**
```bash
git clone https://github.com/runer0101/simulacion_mallas.git
cd simulacion_mallas
```

**2. Crear y Activar un Entorno Virtual**
*   En Windows:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
*   En macOS/Linux:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

**3. Instalar las Dependencias**

*(Nota: Se recomienda crear un archivo `requirements.txt` con las librerías necesarias. Puedes generarlo con `pip freeze > requirements.txt` después de instalar las librerías manualmente).*
```bash
pip install Flask numpy matplotlib
```
Si clonas un repositorio que ya incluye un archivo `requirements.txt`, simplemente ejecuta:
```bash
pip install -r requirements.txt
```

**4. Ejecutar la Aplicación**
```bash
python app.py
```
La aplicación estará disponible en `http://127.0.0.1:5000` en tu navegador web.

## Cómo Usar

1.  Abre la aplicación en tu navegador.
2.  Introduce los valores de las resistencias (R1 a R6) y los voltajes (V1 a V3) en el formulario.
3.  Haz clic en el botón **"Calcular"**.
4.  Los resultados de las corrientes (I1, I2, I3) aparecerán debajo del formulario, junto con una interpretación.
5.  Más abajo en la página, encontrarás el desglose matemático completo con los valores que introdujiste.
6.  Puedes usar el botón **"Cargar ejemplo"** para rellenar el formulario con un conjunto de datos predefinido.

## Autor

*   **runer0101**