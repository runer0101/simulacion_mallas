from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def calcular_corrientes(R1, R2, R3, R4, R5, R6, V1, V2, V3):
    """
    Calcula las corrientes de malla usando el método matricial.
    
    El sistema de ecuaciones para 3 mallas es:
    (R1+R4+R6)I1 - R4*I2 - R6*I3 = V1
    -R4*I1 + (R2+R4+R5)I2 - R5*I3 = V2  
    -R6*I1 - R5*I2 + (R3+R5+R6)I3 = V3
    """
    # Matriz de coeficientes basada en el método de mallas
    A = np.array([
        [R1 + R4 + R6, -R4, -R6],
        [-R4, R2 + R4 + R5, -R5],
        [-R6, -R5, R3 + R5 + R6]
    ])
    
    # Vector de voltajes
    B = np.array([V1, V2, V3])
    
    # Resolver el sistema de ecuaciones lineales
    try:
        I = np.linalg.solve(A, B)
        return I[0], I[1], I[2], A, B
    except np.linalg.LinAlgError:
        raise ValueError("El sistema no tiene solución única")

@app.route('/', methods=['GET', 'POST'])
def home():
    # Valores por defecto realistas para una instalación residencial
    default_vals = {
        'R1': 0.5,   # Resistencia del ramal de sala (Ω)
        'R2': 0.7,   # Resistencia del ramal de cocina (Ω)  
        'R3': 0.6,   # Resistencia del ramal de dormitorios (Ω)
        'R4': 20,    # Resistencia entre sala y cocina (Ω)
        'R5': 15,    # Resistencia entre cocina y dormitorios (Ω)
        'R6': 25,    # Resistencia entre dormitorios y sala (Ω)
        'V1': 120,   # Voltaje de alimentación sala (V)
        'V2': 220,   # Voltaje de alimentación cocina (V)
        'V3': 120    # Voltaje de alimentación dormitorios (V)
    }
    
    vals = default_vals.copy()
    error = None
    I1 = I2 = I3 = A = B = None
    
    if request.method == 'POST':
        try:
            # Obtener valores del formulario
            for key in vals:
                form_value = request.form.get(key)
                if form_value:
                    vals[key] = float(form_value)
                    
            # Validar que los valores sean positivos
            for key, value in vals.items():
                if value <= 0:
                    raise ValueError(f"El valor de {key} debe ser positivo")
                    
        except ValueError as e:
            if "could not convert" in str(e):
                error = 'Por favor, ingresa valores numéricos válidos.'
            else:
                error = str(e)
        except Exception:
            error = 'Error en los datos ingresados. Verifica los valores.'

    # Calcular corrientes si no hay errores
    if not error:
        try:
            R1, R2, R3, R4, R5, R6 = vals['R1'], vals['R2'], vals['R3'], vals['R4'], vals['R5'], vals['R6']
            V1, V2, V3 = vals['V1'], vals['V2'], vals['V3']
            
            I1, I2, I3, A, B = calcular_corrientes(R1, R2, R3, R4, R5, R6, V1, V2, V3)
            
        except ValueError as e:
            error = str(e)
        except Exception:
            error = 'El sistema no tiene solución única. Verifica los valores ingresados.'

    return render_template('index.html', 
                         vals=vals, 
                         error=error,
                         I1=I1, I2=I2, I3=I3,
                         A=A, B=B)

if __name__ == '__main__':
    app.run(debug=True)
