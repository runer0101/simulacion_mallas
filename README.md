# Simulación de Mallas Residenciales

Una aplicación web interactiva para el análisis de circuitos eléctricos en mallas, optimizada para instalaciones residenciales.

## Características

### Funcionalidades Principales
- **Calculadora de mallas** con interfaz intuitiva
- **Visualización SVG animada** del circuito eléctrico
- **Resolución matemática paso a paso** con MathJax
- **Validación en tiempo real** de los datos de entrada
- **Diseño completamente responsivo** para todos los dispositivos

### Tecnologías Utilizadas
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Matemáticas**: NumPy para cálculos matriciales
- **Visualización**: SVG animado + MathJax para ecuaciones
- **Estilos**: CSS Grid + Flexbox + Unidades responsivas

## Estructura del Proyecto

```
simulacion_mallas/
├── app.py                    # Aplicación Flask principal
├── simulacion_mallas.py      # Script de cálculo independiente
├── run_app.bat              # Script de ejecución (Windows)
├── run_app.sh               # Script de ejecución (Linux/Mac)
├── static/
│   ├── styles.css           # Estilos CSS responsivos
│   └── main.js              # JavaScript interactivo
└── templates/
    └── index.html           # Template HTML principal
```

## Cómo Ejecutar

### Opción 1: Script automático (Windows)
```bash
run_app.bat
```

### Opción 2: Script automático (Linux/Mac)
```bash
chmod +x run_app.sh
./run_app.sh
```

### Opción 3: Comando directo
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Diseño Responsivo

El proyecto utiliza un sistema de unidades completamente responsivo:

- **vw/vh**: Para tamaños de fuente y espaciados
- **%**: Para márgenes y dimensiones
- **CSS Grid/Flexbox**: Para layouts adaptativos
- **Media queries**: Para diferentes breakpoints

### Breakpoints
- **Desktop**: > 1200px
- **Tablet**: 768px - 1200px  
- **Mobile**: < 768px

## Funcionalidades Matemáticas

### Método de Mallas
El sistema resuelve circuitos de 3 mallas usando:

```
(R1+R4+R6)I1 - R4*I2 - R6*I3 = V1
-R4*I1 + (R2+R4+R5)I2 - R5*I3 = V2  
-R6*I1 - R5*I2 + (R3+R5+R6)I3 = V3
```

### Características
- **Matriz de coeficientes** automática
- **Resolución con NumPy** (eliminación gaussiana)
- **Validación de sistemas** singulares
- **Interpretación de resultados** (sentido de corriente)

## Características de UI/UX

### Validación en Tiempo Real
- Campos numéricos válidos
- Valores positivos
- Rangos realistas (R: 0.1-1000Ω, V: 1-500V)
- Mensajes de error descriptivos

### Animaciones
- Electrones moviéndose por el circuito
- Efectos de brillo en las bombillas
- Transiciones suaves en hover
- Animaciones de aparición de resultados

### Interactividad
- Hover en resultados resalta elementos del SVG
- Copia de resultados al portapapeles
- Exportación a CSV
- Tooltips informativos

## Personalización

### Valores por Defecto
```python
default_vals = {
    'R1': 0.5,   # Resistencia sala (Ω)
    'R2': 0.7,   # Resistencia cocina (Ω)  
    'R3': 0.6,   # Resistencia dormitorios (Ω)
    'R4': 20,    # Conexión sala-cocina (Ω)
    'R5': 15,    # Conexión cocina-dormitorios (Ω)
    'R6': 25,    # Conexión dormitorios-sala (Ω)
    'V1': 120,   # Voltaje sala (V)
    'V2': 220,   # Voltaje cocina (V)
    'V3': 120    # Voltaje dormitorios (V)
}
```

### Colores del Tema
- **Primario**: `#0ea5e9` (Sky Blue)
- **Secundario**: `#38bdf8` (Light Blue)
- **Acentos**: `#6366f1` (Indigo), `#e11d48` (Rose)
- **Fondo**: Gradiente `#38bdf8` → `#fff`

## Casos de Uso

### Residencial
- Análisis de cargas por zona
- Dimensionamiento de conductores
- Cálculo de caídas de tensión
- Optimización energética

### Educativo
- Enseñanza del método de mallas
- Visualización de conceptos eléctricos
- Práctica con sistemas matriciales
- Comprensión de la Ley de Kirchhoff

## Mejoras Implementadas

### v2.0 (Actual)
- Arquitectura Flask refactorizada
- Sistema de templates organizado
- CSS completamente responsivo
- JavaScript interactivo avanzado
- Validación en tiempo real
- Animaciones SVG mejoradas
- Soporte completo MathJax
- Exportación de datos

### v1.0 (Original)
- Cálculo básico de mallas
- Interfaz web simple
- SVG estático del circuito

## Solución de Problemas

### Error: "El sistema no tiene solución única"
- Verificar que los valores de resistencia sean positivos
- Asegurar que el circuito no sea singular
- Revisar las conexiones del circuito

### Error: "Valores numéricos inválidos"
- Usar punto decimal (.) no coma (,)
- Verificar que todos los campos estén llenos
- Asegurar valores dentro de rangos válidos

## Soporte

Para reportar problemas o sugerir mejoras:
- **Autor**: runer0101
- **Proyecto**: Optimización de sistemas de distribución de energía
- **Tema**: Simulación de circuitos en mallas residenciales

## Licencia

Proyecto académico - 2024
Tema: Optimización de sistemas de distribución de energía en instalaciones residenciales
