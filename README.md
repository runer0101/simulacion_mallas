# Simulador de Circuitos Eléctricos en Mallas

---

## Sinopsis

Una aplicación web interactiva para el análisis y la simulación de circuitos eléctricos, diseñada específicamente para la optimización de sistemas de distribución de energía en instalaciones residenciales.

El repositorio del proyecto se encuentra en GitHub: [https://github.com/runer0101/simulacion_mallas.git](https://github.com/runer0101/simulacion_mallas.git)

## Características Principales

- **Simulación Interactiva:** Permite a los usuarios introducir valores personalizados para resistencias y fuentes de voltaje para ver los resultados en tiempo real.
- **Generación Dinámica de Diagramas:** El esquema del circuito se actualiza visualmente con los valores introducidos, gracias a la generación de imágenes con Matplotlib.
- **Validación de Entradas:** El formulario valida los datos en el lado del cliente (JavaScript) y del servidor (Python) para asegurar que los parámetros sean físicamente realistas.
- **Desglose Matemático Detallado:** Muestra paso a paso la formulación de las ecuaciones de malla, la construcción de la matriz y la solución final, utilizando MathJax para una representación clara de las fórmulas.
- **Interpretación de Resultados:** Proporciona un análisis textual de las corrientes calculadas, indicando la dirección y la magnitud de la carga en cada malla.
- **Interfaz de Usuario Moderna y Responsiva:** La interfaz está diseñada para ser intuitiva y accesible en diferentes dispositivos (escritorio, tablet, móvil).

## Tecnologías Utilizadas

- **Backend:**
    - **Python 3**
    - **Flask:** Micro-framework para el servidor web.
    - **NumPy:** Para los cálculos matriciales y la resolución del sistema de ecuaciones.
    - **Matplotlib:** Para la generación dinámica de los diagramas del circuito.
- **Frontend:**
    - **HTML5**
    - **CSS3:** (Flexbox, CSS Grid) para el diseño y la maquetación responsiva.
    - **JavaScript (ES6):** Para la interactividad del cliente, validación de formularios y llamadas a la API.
    - **Jinja2:** Motor de plantillas para renderizar el contenido dinámico.
    - **MathJax:** Para renderizar ecuaciones matemáticas en formato LaTeX.

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
- Python 3.8 o superior
- `pip` y `venv`

**1. Clonar el Repositorio**
```bash
git clone https://github.com/runer0101/simulacion_mallas.git
cd simulacion_mallas
```

**2. Crear y Activar un Entorno Virtual**
- En Windows:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
- En macOS/Linux:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

**3. Instalar las Dependencias**

```bash
pip install -r requirements.txt
```

Si no tienes el archivo `requirements.txt`, instala manualmente:
```bash
pip install Flask numpy matplotlib
```

**4. Ejecutar la Aplicación**
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Uso de la Aplicación

### Interfaz Web
1. **Ingresar parámetros del circuito:**
   - Resistencias (R1-R6) en Ohms
   - Voltajes (V1-V3) en Volts
2. **Hacer clic en "Calcular"** para obtener las corrientes I1, I2, I3
3. **Ver resultados** con interpretación automática y diagrama actualizado
4. **Usar "Cargar ejemplo"** para valores predefinidos del problema típico

### Valores de Ejemplo

**Problema Académico:**
```
R1=2Ω, R2=4Ω, R3=3Ω, R4=6Ω, R5=5Ω, R6=2Ω
V1=12V, V2=0V, V3=0V
Resultado: I1=2.296A, I2=1.406A, I3=1.262A
```

### API REST

**Calcular corrientes:**
```bash
POST /api/calculate
Content-Type: application/json

{
  "R1": 2.0, "R2": 4.0, "R3": 3.0,
  "R4": 6.0, "R5": 5.0, "R6": 2.0,
  "V1": 12.0, "V2": 0.0, "V3": 0.0
}
```

**Obtener valores de ejemplo:**
```bash
GET /api/example
```

**Generar diagrama del circuito:**
```bash
GET /circuito.png?R1=2.0&R2=4.0&R3=3.0&R4=6.0&R5=5.0&R6=2.0&V1=12.0&V2=0.0&V3=0.0
```

## Método de Análisis

La aplicación utiliza el **método de análisis de mallas** basado en las leyes de Kirchhoff:

### Sistema de Ecuaciones
```
(R1+R4+R6)×I1 - R4×I2 - R6×I3 = V1
-R4×I1 + (R2+R4+R5)×I2 - R5×I3 = V2  
-R6×I1 - R5×I2 + (R3+R5+R6)×I3 = V3
```

### Resolución Matricial
- **Matriz A**: Coeficientes de resistencias según topología del circuito
- **Vector B**: Voltajes independientes de cada malla
- **Solución**: I = A⁻¹ × B usando álgebra lineal (NumPy)

## Validaciones

- **Rangos de parámetros:** Resistencias (0.01-1000Ω), Voltajes (1-500V)
- **Validación de matrices:** Verificación de sistemas no singulares
- **Límites de corriente:** Alertas para corrientes superiores a 1000A
- **Manejo de errores:** Captura y logging de excepciones

## Interpretación de Resultados

### Magnitud de corriente:
- **< 1A:** Carga baja
- **1-10A:** Carga normal  
- **10-50A:** Carga alta
- **> 50A:** Carga crítica

### Sentido de corriente:
- **Positiva:** Sentido horario
- **Negativa:** Sentido antihorario

## Despliegue

### Opciones de Hosting

**Heroku:**
```bash
# Crear Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create simulacion-mallas-runer
git push heroku main
```

**Railway/Render:**
- Conecta tu repositorio GitHub
- Deploy automático
- SSL gratuito incluido

## Casos de Uso

1. **Análisis de instalaciones residenciales** reales
2. **Educación en ingeniería eléctrica** - problemas de ejemplo
3. **Verificación de diseños** eléctricos antes de implementación
4. **Integración con software** de diseño via API REST
5. **Simulación de cargas** en diferentes zonas de la vivienda

## Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork del proyecto
2. Crear rama feature: `git checkout -b feature/nueva-caracteristica`
3. Commit cambios: `git commit -m 'Descripción del cambio'`
4. Push a la rama: `git push origin feature/nueva-caracteristica`
5. Abrir Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

**Desarrollado por:** runer0101  
**Versión:** 1.2.0  
**Última actualización:** Julio 2025  
**Python:** 3.8+ requerido