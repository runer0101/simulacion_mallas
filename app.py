from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
from typing import Tuple, Dict, Union, Optional
import logging
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import io

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class MeshAnalyzer:
    """Clase para el análisis de circuitos de mallas residenciales."""
    
    # Rangos válidos para validación
    RESISTANCE_RANGE = (0.01, 1000.0)  # Ohms
    VOLTAGE_RANGE = (1.0, 500.0)       # Volts
    
    @staticmethod
    def validate_parameters(params: Dict[str, float]) -> None:
        """
        Valida que todos los parámetros estén en rangos aceptables.
        
        Args:
            params: Diccionario con los valores de resistencias y voltajes
            
        Raises:
            ValueError: Si algún parámetro está fuera de rango
        """
        for key, value in params.items():
            if not isinstance(value, (int, float)) or np.isnan(value) or np.isinf(value):
                raise ValueError(f"{key}: Debe ser un número válido")
            
            if value <= 0:
                raise ValueError(f"{key}: Debe ser un valor positivo")
            
            if key.startswith('R'):
                min_val, max_val = MeshAnalyzer.RESISTANCE_RANGE
                if not (min_val <= value <= max_val):
                    raise ValueError(f"{key}: Resistencia debe estar entre {min_val}Ω y {max_val}Ω")
            
            elif key.startswith('V'):
                min_val, max_val = MeshAnalyzer.VOLTAGE_RANGE
                if not (min_val <= value <= max_val):
                    raise ValueError(f"{key}: Voltaje debe estar entre {min_val}V y {max_val}V")
    
    @staticmethod
    def calcular_corrientes(R1: float, R2: float, R3: float, R4: float, R5: float, R6: float,
                          V1: float, V2: float, V3: float) -> Tuple[float, float, float, np.ndarray, np.ndarray]:
        """
        Calcula las corrientes de malla usando el método matricial de Kirchhoff.
        
        Método de análisis nodal para circuito triangular residencial:
        - Malla 1: Sala/Comedor (I1)
        - Malla 2: Cocina/Lavandería (I2)  
        - Malla 3: Dormitorios (I3)
        
        Sistema de ecuaciones:
        (R1+R4+R6)×I1 - R4×I2 - R6×I3 = V1
        -R4×I1 + (R2+R4+R5)×I2 - R5×I3 = V2  
        -R6×I1 - R5×I2 + (R3+R5+R6)×I3 = V3
        
        Args:
            R1-R6: Resistencias del circuito (Ohms)
            V1-V3: Voltajes de alimentación (Volts)
            
        Returns:
            Tuple con: (I1, I2, I3, matriz_A, vector_B)
            
        Raises:
            ValueError: Si el sistema no tiene solución única o parámetros inválidos
        """
        # Validar parámetros de entrada
        params = {'R1': R1, 'R2': R2, 'R3': R3, 'R4': R4, 'R5': R5, 'R6': R6,
                 'V1': V1, 'V2': V2, 'V3': V3}
        MeshAnalyzer.validate_parameters(params)
        
        # Construir matriz de coeficientes (método de mallas)
        A = np.array([
            [R1 + R4 + R6, -R4, -R6],           # Ecuación malla 1
            [-R4, R2 + R4 + R5, -R5],           # Ecuación malla 2
            [-R6, -R5, R3 + R5 + R6]            # Ecuación malla 3
        ], dtype=np.float64)
        
        # Vector de voltajes independientes
        B = np.array([V1, V2, V3], dtype=np.float64)
        
        # Verificar que la matriz no sea singular
        det_A = np.linalg.det(A)
        if abs(det_A) < 1e-10:
            raise ValueError("Sistema singular: Las resistencias crean un circuito indeterminado")
        
        # Resolver sistema de ecuaciones lineales
        try:
            I = np.linalg.solve(A, B)
            
            # Verificar que las corrientes sean físicamente razonables
            max_current = max(abs(i) for i in I)
            if max_current > 1000:  # Más de 1000A es irrealista para uso residencial
                logger.warning(f"Corriente muy alta detectada: {max_current:.2f}A")
            
            return float(I[0]), float(I[1]), float(I[2]), A, B
            
        except np.linalg.LinAlgError as e:
            raise ValueError(f"Error al resolver el sistema: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error inesperado en el cálculo: {str(e)}")
    
    @staticmethod
    def interpretar_corrientes(I1: float, I2: float, I3: float) -> Dict[str, str]:
        """
        Interpreta el sentido y magnitud de las corrientes calculadas.
        
        Args:
            I1, I2, I3: Corrientes de malla calculadas
            
        Returns:
            Diccionario con interpretaciones textuales
        """
        interpretaciones = {}
        
        corrientes = {'I1': I1, 'I2': I2, 'I3': I3}
        zonas = {'I1': 'Sala/Comedor', 'I2': 'Cocina/Lavandería', 'I3': 'Dormitorios'}
        
        for nombre, corriente in corrientes.items():
            magnitud = abs(corriente)
            sentido = "horario" if corriente > 0 else "antihorario"
            zona = zonas[nombre]
            
            if magnitud < 0.001:
                interpretaciones[nombre] = f"{zona}: Corriente despreciable (~0A)"
            elif magnitud < 1:
                interpretaciones[nombre] = f"{zona}: {magnitud:.3f}A ({sentido}) - Carga baja"
            elif magnitud < 10:
                interpretaciones[nombre] = f"{zona}: {magnitud:.2f}A ({sentido}) - Carga normal"
            elif magnitud < 50:
                interpretaciones[nombre] = f"{zona}: {magnitud:.1f}A ({sentido}) - Carga alta"
            else:
                interpretaciones[nombre] = f"{zona}: {magnitud:.1f}A ({sentido}) - ⚠️ CARGA CRÍTICA"
        
        return interpretaciones

def get_default_values() -> Dict[str, float]:
    """
    Retorna valores por defecto realistas para una instalación residencial.
    
    Returns:
        Diccionario con valores típicos de resistencias y voltajes
    """
    return {
        'R1': 0.5,   # Resistencia del ramal de sala (Ω) - Cable 12 AWG
        'R2': 0.7,   # Resistencia del ramal de cocina (Ω) - Cable 12 AWG  
        'R3': 0.6,   # Resistencia del ramal de dormitorios (Ω) - Cable 12 AWG
        'R4': 20,    # Resistencia entre sala y cocina (Ω) - Cargas compartidas
        'R5': 15,    # Resistencia entre cocina y dormitorios (Ω) - Cargas compartidas
        'R6': 25,    # Resistencia entre dormitorios y sala (Ω) - Cargas compartidas
        'V1': 120,   # Voltaje de alimentación sala (V) - Monofásico estándar
        'V2': 220,   # Voltaje de alimentación cocina (V) - Bifásico para electrodomésticos
        'V3': 120    # Voltaje de alimentación dormitorios (V) - Monofásico estándar
    }

def get_example_values() -> Dict[str, float]:
    """
    Retorna los valores de ejemplo del problema mostrado en la imagen.
    """
    return {
        'R1': 2.0,   # Cocina
        'R2': 4.0,   # entre Cocina y Sala
        'R3': 3.0,   # Sala
        'R4': 6.0,   # entre Sala y Dormitorios
        'R5': 5.0,   # Dormitorios
        'R6': 2.0,   # a tierra desde Dormitorio
        'V1': 12.0,  # Fuente de voltaje
        'V2': 0.0,   # No hay V2 en el ejemplo
        'V3': 0.0    # No hay V3 en el ejemplo
    }

def parse_form_data(form_data: Dict, default_vals: Dict[str, float]) -> Tuple[Dict[str, float], Optional[str]]:
    """
    Procesa y valida los datos del formulario.
    
    Args:
        form_data: Datos del formulario Flask
        default_vals: Valores por defecto a usar
        
    Returns:
        Tuple con (valores_procesados, mensaje_error)
    """
    vals = default_vals.copy()
    
    try:
        # Procesar cada campo del formulario
        for key in vals.keys():
            form_value = form_data.get(key, '').strip()
            if form_value:
                # Reemplazar coma por punto para formato decimal
                form_value = form_value.replace(',', '.')
                vals[key] = float(form_value)
        
        # Validar usando la clase MeshAnalyzer
        MeshAnalyzer.validate_parameters(vals)
        return vals, None
        
    except ValueError as e:
        return vals, str(e)
    except Exception as e:
        logger.error(f"Error inesperado al procesar formulario: {e}")
        return vals, "Error al procesar los datos. Verifica el formato de los números."

def dibujar_circuito(vals):
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('#222')
    ax.set_facecolor('#222')
    ax.axis('off')
    # Líneas horizontales superiores e inferiores
    ax.plot([0.5, 6.5], [3, 3], color='white', lw=3)  # superior
    ax.plot([0.5, 6.5], [1, 1], color='white', lw=3)  # inferior
    # Líneas verticales
    ax.plot([0.5, 0.5], [1, 3], color='white', lw=3)
    ax.plot([2.5, 2.5], [1, 3], color='white', lw=3)
    ax.plot([4.5, 4.5], [1, 3], color='white', lw=3)
    ax.plot([6.5, 6.5], [1, 3], color='white', lw=3)
    # Resistencias (como texto)
    ax.text(1.5, 3.15, f"R₁={vals['R1']}Ω", color='orange', fontsize=13, ha='center', va='bottom', fontweight='bold')
    ax.text(3.5, 3.15, f"R₃={vals['R3']}Ω", color='orange', fontsize=13, ha='center', va='bottom', fontweight='bold')
    ax.text(5.5, 3.15, f"R₅={vals['R5']}Ω", color='orange', fontsize=13, ha='center', va='bottom', fontweight='bold')
    ax.text(0.7, 2, f"R₂={vals['R2']}Ω", color='orange', fontsize=13, ha='left', va='center', fontweight='bold', rotation=90)
    ax.text(2.7, 2, f"R₄={vals['R4']}Ω", color='orange', fontsize=13, ha='left', va='center', fontweight='bold', rotation=90)
    ax.text(4.7, 2, f"R₆={vals['R6']}Ω", color='orange', fontsize=13, ha='left', va='center', fontweight='bold', rotation=90)
    # Fuente de voltaje (círculo y texto)
    fuente_x, fuente_y = 0.5, 2.6
    circle = Circle((fuente_x, fuente_y), 0.18, fill=False, edgecolor='cyan', lw=2)
    ax.add_patch(circle)
    ax.text(fuente_x-0.15, fuente_y+0.15, '+', color='cyan', fontsize=14, ha='center', va='center')
    ax.text(fuente_x-0.15, fuente_y-0.15, '-', color='cyan', fontsize=14, ha='center', va='center')
    ax.text(fuente_x-0.4, fuente_y, f"V₁={vals['V1']}V", color='cyan', fontsize=13, ha='right', va='center', fontweight='bold')
    # Flechas de corriente
    def flecha_corriente(x1, y1, x2, y2, label):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(facecolor='lime', edgecolor='lime', arrowstyle='->', lw=2))
        ax.text((x1+x2)/2, y1-0.18, label, color='lime', fontsize=15, ha='center', va='top', fontweight='bold')
    flecha_corriente(1, 0.9, 2, 0.9, 'I₁')
    flecha_corriente(3, 0.9, 4, 0.9, 'I₂')
    flecha_corriente(5, 0.9, 6, 0.9, 'I₃')
    # Etiquetas de malla
    ax.text(1.5, 0.6, 'Malla 1\n(Cocina)', color='white', fontsize=13, ha='center', va='center')
    ax.text(3.5, 0.6, 'Malla 2\n(Sala)', color='white', fontsize=13, ha='center', va='center')
    ax.text(5.5, 0.6, 'Malla 3\n(Dormitorios)', color='white', fontsize=13, ha='center', va='center')
    ax.set_xlim(0, 7)
    ax.set_ylim(0.3, 3.5)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Ruta principal de la aplicación.
    
    GET: Muestra el formulario con valores por defecto
    POST: Procesa el cálculo y muestra resultados
    """
    default_vals = get_default_values()
    vals = default_vals.copy()
    error = None
    I1 = I2 = I3 = A = B = interpretaciones = None
    
    if request.method == 'POST':
        # Procesar datos del formulario
        vals, error = parse_form_data(request.form, default_vals)
        
        # Si no hay errores en el formulario, calcular corrientes
        if not error:
            try:
                # Extraer parámetros
                R1, R2, R3, R4, R5, R6 = vals['R1'], vals['R2'], vals['R3'], vals['R4'], vals['R5'], vals['R6']
                V1, V2, V3 = vals['V1'], vals['V2'], vals['V3']

                # Calcular corrientes de malla
                I1, I2, I3, A, B = MeshAnalyzer.calcular_corrientes(R1, R2, R3, R4, R5, R6, V1, V2, V3)
                
                # Interpretar resultados
                interpretaciones = MeshAnalyzer.interpretar_corrientes(I1, I2, I3)
                
                logger.info(f"Cálculo exitoso: I1={I1:.3f}A, I2={I2:.3f}A, I3={I3:.3f}A")
                
            except ValueError as e:
                error = str(e)
                logger.warning(f"Error de validación: {error}")
            except Exception as e:
                error = "Error inesperado durante el cálculo. Verifica los valores ingresados."
                logger.error(f"Error inesperado: {e}")

    # Preparar datos para el template
    template_data = {
        'vals': vals,
        'error': error,
        'I1': I1, 'I2': I2, 'I3': I3,
        'A': A, 'B': B,
        'interpretaciones': interpretaciones,
        'default_vals': default_vals
    }
    
    return render_template('index.html', **template_data)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """
    API endpoint para cálculos programáticos.
    
    Acepta JSON con parámetros R1-R6, V1-V3
    Retorna JSON con resultados o errores
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos JSON'}), 400
        
        # Validar que estén todos los parámetros requeridos
        required_params = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'V1', 'V2', 'V3']
        missing_params = [p for p in required_params if p not in data]
        if missing_params:
            return jsonify({'error': f'Parámetros faltantes: {missing_params}'}), 400
        
        # Extraer y calcular
        R1, R2, R3, R4, R5, R6 = data['R1'], data['R2'], data['R3'], data['R4'], data['R5'], data['R6']
        V1, V2, V3 = data['V1'], data['V2'], data['V3']
        
        I1, I2, I3, A, B = MeshAnalyzer.calcular_corrientes(R1, R2, R3, R4, R5, R6, V1, V2, V3)
        interpretaciones = MeshAnalyzer.interpretar_corrientes(I1, I2, I3)
        
        return jsonify({
            'success': True,
            'currents': {'I1': I1, 'I2': I2, 'I3': I3},
            'matrix_A': A.tolist(),
            'vector_B': B.tolist(),
            'interpretations': interpretaciones
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error en API: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/example', methods=['GET'])
def api_example():
    """
    Devuelve los valores de ejemplo del problema como JSON.
    """
    return jsonify(get_example_values())

@app.route('/circuito.png')
def circuito_png():
    # Obtener valores de la query string o usar por defecto
    vals = get_default_values()
    for key in vals.keys():
        val = request.args.get(key)
        if val is not None:
            try:
                vals[key] = float(val.replace(',', '.'))
            except Exception:
                pass  # Si hay error, deja el valor por defecto
    buf = dibujar_circuito(vals)
    return send_file(buf, mimetype='image/png')

@app.errorhandler(404)
def not_found(error):
    """Manejo de páginas no encontradas."""
    template_data = {
        'vals': get_default_values(),
        'error': "Página no encontrada (Error 404)",
        'I1': None, 'I2': None, 'I3': None,
        'A': None, 'B': None,
        'interpretaciones': None,
        'default_vals': get_default_values()
    }
    return render_template('index.html', **template_data), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos del servidor."""
    logger.error(f"Error interno: {error}")
    template_data = {
        'vals': get_default_values(),
        'error': "Error interno del servidor (Error 500). Revisa la consola para más detalles.",
        'I1': None, 'I2': None, 'I3': None,
        'A': None, 'B': None,
        'interpretaciones': None,
        'default_vals': get_default_values()
    }
    return render_template('index.html', **template_data), 500

if __name__ == '__main__':
    logger.info("Iniciando servidor de simulación de mallas residenciales...")
    app.run(debug=True)
