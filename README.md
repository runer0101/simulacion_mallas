# Simulador de Mallas Eléctricas Residenciales

Aplicación web que calcula corrientes eléctricas en circuitos residenciales usando análisis de mallas de Kirchhoff.

## ¿Qué hace?

Esta herramienta analiza circuitos eléctricos de viviendas divididos en tres zonas:
- **Malla 1:** Sala/Comedor  
- **Malla 2:** Cocina/Lavandería
- **Malla 3:** Dormitorios

Calcula automáticamente las corrientes que circulan por cada zona y determina si las cargas son normales o críticas.

## Instalación

\`\`\`bash
git clone https://github.com/runer0101/simulacion_mallas.git
cd simulacion_mallas
pip install flask numpy matplotlib
python app.py o py app.py
\`\`\`

Abrir navegador en: \`http://localhost:5000\`

## Cómo usar

### Interfaz Web
1. Ingresar valores de **resistencias** (R1 a R6) en Ohms
2. Ingresar **voltajes** (V1 a V3) en Volts  
3. Hacer clic en **\"Calcular\"**
4. Ver resultados con interpretación automática

### Ejemplo rápido
Hacer clic en **\"Cargar ejemplo\"** para valores predefinidos:
- R1=2Ω, R2=4Ω, R3=3Ω, R4=6Ω, R5=5Ω, R6=2Ω
- V1=12V, V2=0V, V3=0V
- **Resultado:** I1=2.296A, I2=1.406A, I3=1.262A

## API REST

### Calcular corrientes
\`\`\`bash
POST /api/calculate
Content-Type: application/json

{
  \"R1\": 2.0, \"R2\": 4.0, \"R3\": 3.0,
  \"R4\": 6.0, \"R5\": 5.0, \"R6\": 2.0,
  \"V1\": 12.0, \"V2\": 0.0, \"V3\": 0.0
}
\`\`\`

### Obtener valores de ejemplo
\`\`\`bash
GET /api/example
\`\`\`

### Generar diagrama del circuito
\`\`\`bash
GET /circuito.png?R1=2.0&R2=4.0&R3=3.0&R4=6.0&R5=5.0&R6=2.0&V1=12.0&V2=0.0&V3=0.0
\`\`\`

## Cómo funciona

Resuelve el sistema de ecuaciones de Kirchhoff:
\`\`\`
(R1+R4+R6)×I1 - R4×I2 - R6×I3 = V1
-R4×I1 + (R2+R4+R5)×I2 - R5×I3 = V2
-R6×I1 - R5×I2 + (R3+R5+R6)×I3 = V3
\`\`\`

Usando álgebra lineal: **I = A⁻¹ × B**

## Validaciones

- **Resistencias:** 0.01Ω a 1000Ω
- **Voltajes:** 1V a 500V  
- **Corrientes:** Alerta si supera 1000A
- **Sistema:** Verifica que tenga solución única

## Características técnicas

- **Clase MeshAnalyzer:** Análisis profesional con validación robusta
- **Logging completo:** Registro de cálculos y errores
- **Validación de parámetros:** Rangos seguros para uso residencial
- **Interpretación automática:** Clasificación de cargas (baja/normal/alta/crítica)
- **Manejo de errores:** Captura de sistemas singulares y valores inválidos
- **API REST:** Integración con otras aplicaciones
- **Visualización:** Diagrama dinámico del circuito con matplotlib
- **Interface académica:** Resolución matemática paso a paso con MathJax

## Archivos del proyecto

\`\`\`
simulacion_mallas/
├── app.py                 # Aplicación principal (completa)
├── app_clean.py          # Versión simplificada  
├── templates/
│   └── index.html        # Interfaz web académica con resolución paso a paso
├── static/               # Archivos CSS/JS (si existen)
├── README.md             # Este archivo
└── requirements.txt      # Dependencias
\`\`\`

## Tecnologías

- **Python 3.7+** con Flask para servidor web
- **NumPy** para cálculos matriciales y álgebra lineal
- **Matplotlib** para generación de diagramas del circuito
- **HTML/CSS/JavaScript** para interfaz de usuario
- **MathJax** para renderizado de ecuaciones matemáticas
- **Logging** para monitoreo y debugging
- **Type hints** para mejor documentación del código

## Interpretación de resultados

### Magnitud de corriente:
- **< 0.001A:** Corriente despreciable
- **< 1A:** Carga baja
- **1-10A:** Carga normal  
- **10-50A:** Carga alta
- **> 50A:** ⚠️ Carga crítica

### Sentido de corriente:
- **Positiva:** Sentido horario
- **Negativa:** Sentido antihorario

## Validaciones de seguridad

La aplicación incluye validaciones exhaustivas:
- Verificación de rangos de resistencias y voltajes
- Detección de sistemas singulares (sin solución única)
- Alertas para corrientes peligrosamente altas
- Manejo robusto de errores con logging
- Validación de tipos de datos y valores NaN/infinitos

## Casos de uso

1. **Análisis de instalaciones residenciales** reales
2. **Educación en ingeniería eléctrica** - problemas de ejemplo
3. **Verificación de diseños** eléctricos antes de implementación
4. **Integración con software** de diseño via API REST
5. **Simulación de cargas** en diferentes zonas de la vivienda
6. **Enseñanza académica** con resolución matemática detallada

## Licencia

MIT License - Uso libre para proyectos educativos y comerciales." > README.md

# Crear archivo .gitignore
echo "# Python
__pycache__/
*.py[cod]
*\$py.class
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
ENV/

# Flask
instance/
.webassets-cache

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Virtual environment
venv/
env/

# Temporary files
*.tmp
*.temp" > .gitignore

# Crear requirements.txt
echo "Flask==2.3.3
numpy==1.24.3
matplotlib==3.7.2" > requirements.txt

# Inicializar Git y hacer commit
git init
git add .
git commit -m "🎉 Initial commit: Simulador de mallas eléctricas residenciales

Características implementadas:
- Análisis completo de 3 mallas eléctricas residenciales
- Interfaz web académica con resolución matemática paso a paso
- API REST completa para integración
- Validación robusta de parámetros eléctricos
- Visualización dinámica de circuitos con matplotlib
- Clase MeshAnalyzer para análisis profesional
- Logging completo y manejo de errores
- Renderizado de ecuaciones con MathJax
- Interpretación automática de resultados
- Documentación técnica completa

Zonas analizadas:
- Malla 1: Sala/Comedor
- Malla 2: Cocina/Lavandería  
- Malla 3: Dormitorios

Métodos implementados:
- Análisis de mallas de Kirchhoff
- Resolución matricial con NumPy
- Validación de sistemas no singulares
- Cálculo de corrientes reales en componentes
- Análisis de potencia disipada

Tecnologías:
- Python Flask + NumPy + Matplotlib
- HTML5 + CSS3 + JavaScript + MathJax
- API REST con validación completa
- Logging y Type hints para código profesional"

# Agregar remote origin (reemplaza TU_USUARIO con tu usuario de GitHub)
echo "Para conectar con GitHub, ejecuta:"
echo "git remote add origin https://github.com/TU_USUARIO/simulacion_mallas.git"
echo "git branch -M main" 
echo "git push -u origin main"
