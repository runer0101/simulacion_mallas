from flask import Flask, render_template_string, request
import numpy as np

app = Flask(__name__)

def calcular_corrientes(R1, R2, R3, R4, R5, R6, V1, V2, V3):
    A = np.array([
        [R1 + R3 + R4, -R1, -R3],
        [-R1, R1 + R2 + R5, -R2],
        [-R3, -R2, R2 + R3 + R6]
    ])
    B = np.array([V1, V2, V3])
    I = np.linalg.solve(A, B)
    return I[0], I[1], I[2], A, B

@app.route('/', methods=['GET', 'POST'])
def home():
    default_vals = {
        'R1': 0.5, 'R2': 0.7, 'R3': 0.6, 'R4': 20, 'R5': 15, 'R6': 25,
        'V1': 120, 'V2': 220, 'V3': 120
    }
    vals = default_vals.copy()
    error = None
    if request.method == 'POST':
        try:
            for key in vals:
                vals[key] = float(request.form.get(key, vals[key]))
        except Exception:
            error = 'Por favor, ingresa valores numéricos válidos.'

    R1, R2, R3, R4, R5, R6 = vals['R1'], vals['R2'], vals['R3'], vals['R4'], vals['R5'], vals['R6']
    V1, V2, V3 = vals['V1'], vals['V2'], vals['V3']
    try:
        I1, I2, I3, A, B = calcular_corrientes(R1, R2, R3, R4, R5, R6, V1, V2, V3)
    except Exception:
        I1 = I2 = I3 = None
        error = 'El sistema no tiene solución única (verifica los valores ingresados).'

    latex_mallas = r'''
    \begin{cases}
    (R_1+R_3+R_4)I_1 - R_1 I_2 - R_3 I_3 = V_1 \\
    -R_1 I_1 + (R_1+R_2+R_5)I_2 - R_2 I_3 = V_2 \\
    -R_3 I_1 - R_2 I_2 + (R_2+R_3+R_6)I_3 = V_3
    \end{cases}
    '''
    latex_matriz = r'''
    A = \begin{bmatrix} R_1+R_3+R_4 & -R_1 & -R_3 \\ -R_1 & R_1+R_2+R_5 & -R_2 \\ -R_3 & -R_2 & R_2+R_3+R_6 \end{bmatrix}, \\
    B = \begin{bmatrix} V_1 \\ V_2 \\ V_3 \end{bmatrix}
    '''
    latex_sistema = r'''
    \begin{bmatrix} %.2f & %.2f & %.2f \\ %.2f & %.2f & %.2f \\ %.2f & %.2f & %.2f \end{bmatrix} \begin{bmatrix} I_1 \\ I_2 \\ I_3 \end{bmatrix} = \begin{bmatrix} %.2f \\ %.2f \\ %.2f \end{bmatrix}
    ''' % (A[0,0], A[0,1], A[0,2], A[1,0], A[1,1], A[1,2], A[2,0], A[2,1], A[2,2], B[0], B[1], B[2]) if I1 is not None else ''

    html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Optimización de sistemas de distribución de energía en instalaciones residenciales</title>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(120deg, #e0e7ff 0%, #f8fafc 100%); margin: 0; padding: 0; }}
            header {{ background: #1e293b; color: #fff; padding: 30px 0 15px 0; text-align: center; box-shadow: 0 2px 8px rgba(30,41,59,0.08); }}
            header h1 {{ margin: 0; font-size: 2.5em; letter-spacing: 1px; }}
            header p {{ margin: 10px 0 0 0; font-size: 1.2em; color: #cbd5e1; }}
            main {{ background: #fff; max-width: 950px; margin: 40px auto 30px auto; border-radius: 12px; box-shadow: 0 4px 24px rgba(30,41,59,0.10); padding: 32px 36px 28px 36px; }}
            section {{ margin-bottom: 28px; }}
            .section-title {{ color: #1e293b; font-size: 1.3em; margin-top: 0; margin-bottom: 10px; border-left: 4px solid #6366f1; padding-left: 10px; }}
            .explanation {{ background: #f1f5f9; border-left: 4px solid #6366f1; padding: 16px 18px; border-radius: 6px; margin-bottom: 18px; color: #334155; }}
            .desc-section {{ background: #f1f5f9; border-left: 4px solid #f59e42; padding: 16px 18px; border-radius: 6px; margin-bottom: 18px; color: #b45309; }}
            .results {{ background: #f8fafc; border-radius: 8px; padding: 18px 20px; margin: 18px 0; font-size: 1.15em; color: #1e293b; border: 1px solid #e0e7ef; }}
            .circuit-diagram {{ display: flex; justify-content: center; margin: 24px 0 10px 0; }}
            .footer {{ text-align: center; color: #64748b; font-size: 1em; margin-bottom: 18px; }}
            @media (max-width: 950px) {{ main {{ padding: 18px 6vw; }} }}
            .math-block {{ background: #f3f4f6; border-radius: 6px; padding: 10px 18px; margin: 10px 0 18px 0; font-size: 1.1em; overflow-x: auto; }}
            .form-section {{ background: #f8fafc; border: 1px solid #e0e7ef; border-radius: 8px; padding: 18px 20px; margin-bottom: 24px; }}
            .form-row {{ display: flex; flex-wrap: wrap; gap: 18px; margin-bottom: 12px; }}
            .form-row label {{ min-width: 60px; font-weight: 500; color: #334155; }}
            .form-row input {{ width: 80px; padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 1em; }}
            .form-actions {{ margin-top: 10px; }}
            .form-actions button {{ background: #6366f1; color: #fff; border: none; border-radius: 4px; padding: 8px 18px; font-size: 1em; cursor: pointer; }}
            .form-actions button:hover {{ background: #4f46e5; }}
            .error-msg {{ color: #dc2626; font-weight: 500; margin-bottom: 10px; }}
            .calc-explanation {{ color: #334155; font-size: 1.05em; margin-bottom: 10px; }}
            .arrow-anim {{ animation: moveArrow 1.2s linear infinite alternate; }}
            @keyframes moveArrow {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(-18px); }} }}
        </style>
    </head>
    <body>
        <header>
            <h1>Optimización de sistemas de distribución de energía en instalaciones residenciales</h1>
            <p>Ejemplo de análisis de mallas en una vivienda con tres zonas principales</p>
        </header>
        <main>
            <section>
                <h2 class="section-title">Introducción</h2>
                <div class="explanation">
                    El <b>análisis de circuitos eléctricos en mallas</b> es fundamental para el diseño eficiente de sistemas de distribución de energía en viviendas. Utilizando el método de mallas, es posible calcular las corrientes que circulan por cada lazo del circuito, optimizando así el consumo y la seguridad eléctrica en instalaciones residenciales.<br><br>
                    <b>Este ejemplo representa una vivienda con tres zonas principales:</b> <br>
                    <ul>
                        <li><b>Malla 1:</b> Sala y comedor</li>
                        <li><b>Malla 2:</b> Cocina y lavandería</li>
                        <li><b>Malla 3:</b> Dormitorios</li>
                    </ul>
                    Cada zona tiene su propio ramal, pero comparten parte del cableado y están alimentadas por diferentes circuitos derivados desde el tablero principal. Las resistencias representan tanto el cableado como la carga de los electrodomésticos y luminarias.
                </div>
            </section>
            <section>
                <h2 class="section-title">Circuito de tres mallas residencial</h2>
                <div class="circuit-diagram">
                    <svg width="700" height="600" viewBox="0 0 700 600">
                        <!-- Vértices del triángulo -->
                        <circle cx="150" cy="150" r="12" fill="#64748b" /> <!-- Nodo A -->
                        <circle cx="550" cy="150" r="12" fill="#64748b" /> <!-- Nodo B -->
                        <circle cx="350" cy="500" r="12" fill="#64748b" /> <!-- Nodo C -->
                        <!-- Etiquetas de nodos -->
                        <text x="120" y="140" font-size="26" fill="#64748b" font-weight="bold">A</text>
                        <text x="570" y="140" font-size="26" fill="#64748b" font-weight="bold">B</text>
                        <text x="370" y="540" font-size="26" fill="#64748b" font-weight="bold">C</text>
                        <!-- Lados del triángulo (resistencias compartidas) -->
                        <!-- R1: A-B -->
                        <rect x="210" y="140" width="280" height="14" fill="#64748b" transform="rotate(0 350 150)" />
                        <text x="320" y="135" font-size="18" fill="#64748b">R1={vals['R1']}Ω</text>
                        <!-- R2: B-C -->
                        <rect x="430" y="220" width="180" height="14" fill="#64748b" transform="rotate(120 550 150)" />
                        <text x="520" y="320" font-size="18" fill="#64748b">R2={vals['R2']}Ω</text>
                        <!-- R3: C-A -->
                        <rect x="110" y="220" width="180" height="14" fill="#64748b" transform="rotate(240 150 150)" />
                        <text x="160" y="320" font-size="18" fill="#64748b">R3={vals['R3']}Ω</text>
                        <!-- R4 y V1: desde A hacia afuera -->
                        <rect x="140" y="70" width="20" height="60" fill="#6366f1" />
                        <text x="110" y="60" font-size="20" fill="#6366f1">R4={vals['R4']}Ω</text>
                        <circle cx="150" cy="40" r="18" fill="#facc15" stroke="#eab308" stroke-width="2" />
                        <text x="100" y="35" font-size="20" fill="#b45309">V1={vals['V1']}V</text>
                        <line x1="150" y1="150" x2="150" y2="70" stroke="#334155" stroke-width="5" />
                        <line x1="150" y1="70" x2="150" y2="40" stroke="#334155" stroke-width="5" stroke-dasharray="8,6" />
                        <!-- R5 y V2: desde B hacia afuera -->
                        <rect x="540" y="70" width="20" height="60" fill="#0ea5e9" />
                        <text x="560" y="60" font-size="20" fill="#0ea5e9">R5={vals['R5']}Ω</text>
                        <circle cx="550" cy="40" r="18" fill="#facc15" stroke="#eab308" stroke-width="2" />
                        <text x="570" y="35" font-size="20" fill="#b45309">V2={vals['V2']}V</text>
                        <line x1="550" y1="150" x2="550" y2="70" stroke="#334155" stroke-width="5" />
                        <line x1="550" y1="70" x2="550" y2="40" stroke="#334155" stroke-width="5" stroke-dasharray="8,6" />
                        <!-- R6 y V3: desde C hacia afuera -->
                        <rect x="340" y="520" width="20" height="60" fill="#f59e42" />
                        <text x="370" y="610" font-size="20" fill="#f59e42">R6={vals['R6']}Ω</text>
                        <circle cx="350" cy="600" r="18" fill="#facc15" stroke="#eab308" stroke-width="2" />
                        <text x="370" y="630" font-size="20" fill="#b45309">V3={vals['V3']}V</text>
                        <line x1="350" y1="500" x2="350" y2="520" stroke="#334155" stroke-width="5" />
                        <line x1="350" y1="520" x2="350" y2="600" stroke="#334155" stroke-width="5" stroke-dasharray="8,6" />
                        <!-- Lados del triángulo (conexiones) -->
                        <line x1="150" y1="150" x2="550" y2="150" stroke="#334155" stroke-width="5" /> <!-- A-B -->
                        <line x1="550" y1="150" x2="350" y2="500" stroke="#334155" stroke-width="5" /> <!-- B-C -->
                        <line x1="350" y1="500" x2="150" y2="150" stroke="#334155" stroke-width="5" /> <!-- C-A -->
                    </svg>
                </div>
            </section>
            <section class="desc-section">
                <b>Descripción:</b> El circuito mostrado representa tres mallas conectadas mediante resistencias (<b>R1</b> a <b>R6</b>) y alimentadas por tres fuentes de voltaje (<b>V1</b>, <b>V2</b> y <b>V3</b>). El objetivo es calcular las corrientes <b>I₁</b>, <b>I₂</b> e <b>I₃</b> que circulan por cada malla, lo cual es esencial para dimensionar correctamente los conductores y dispositivos de protección en una instalación residencial.
            </section>
            <section class="form-section">
                <h2 class="section-title">Calculadora de mallas residenciales</h2>
                <div class="calc-explanation">
                    Ingresa los valores de las resistencias y voltajes de cada zona de la vivienda. Al pulsar "Calcular", obtendrás las corrientes de malla para cada lazo del circuito. Esto te permite analizar y optimizar la distribución de energía en instalaciones residenciales reales.
                </div>
                <form method="post">
                    <div class="form-row">
                        <label for="R1">R1 (Ω):</label><input type="number" step="any" name="R1" value="{vals['R1']}">
                        <label for="R2">R2 (Ω):</label><input type="number" step="any" name="R2" value="{vals['R2']}">
                        <label for="R3">R3 (Ω):</label><input type="number" step="any" name="R3" value="{vals['R3']}">
                    </div>
                    <div class="form-row">
                        <label for="R4">R4 (Ω):</label><input type="number" step="any" name="R4" value="{vals['R4']}">
                        <label for="R5">R5 (Ω):</label><input type="number" step="any" name="R5" value="{vals['R5']}">
                        <label for="R6">R6 (Ω):</label><input type="number" step="any" name="R6" value="{vals['R6']}">
                    </div>
                    <div class="form-row">
                        <label for="V1">V1 (V):</label><input type="number" step="any" name="V1" value="{vals['V1']}">
                        <label for="V2">V2 (V):</label><input type="number" step="any" name="V2" value="{vals['V2']}">
                        <label for="V3">V3 (V):</label><input type="number" step="any" name="V3" value="{vals['V3']}">
                    </div>
                    <div class="form-actions">
                        <button type="submit">Calcular</button>
                    </div>
                    {'<div class="error-msg">'+error+'</div>' if error else ''}
                </form>
            </section>
            <section>
                <h2 class="section-title">Resultados de la simulación</h2>
                <div class="results">
                    {f'<b>Corriente en la malla 1 (Sala/Comedor, I₁):</b> {I1:.2f} A<br>' if I1 is not None else ''}
                    {f'<b>Corriente en la malla 2 (Cocina/Lavandería, I₂):</b> {I2:.2f} A<br>' if I2 is not None else ''}
                    {f'<b>Corriente en la malla 3 (Dormitorios, I₃):</b> {I3:.2f} A' if I3 is not None else ''}
                </div>
                <div class="explanation">
                    <b>Interpretación:</b> Estos valores permiten analizar el comportamiento del circuito y tomar decisiones para optimizar la distribución de energía, reducir pérdidas y mejorar la seguridad eléctrica en el hogar.
                </div>
            </section>
            <section>
                <h2 class="section-title">¿Cómo se calculan las corrientes de malla?</h2>
                <div class="explanation">
                    <ol>
                        <li><b>Identificación de las mallas:</b><br>
                            Observa el circuito y define cada lazo independiente (malla). Asigna una corriente a cada malla (por ejemplo, I₁, I₂, I₃), normalmente en sentido horario.
                        </li>
                        <li><b>Aplicación de la Ley de Kirchhoff de Voltajes (LKV):</b><br>
                            Para cada malla, recorre el lazo sumando las caídas y subidas de voltaje (resistencias y fuentes). La suma algebraica de voltajes en cada malla debe ser igual a cero.<br>
                            <i>Ejemplo:</i> Para la malla 1, suma las caídas de tensión en R1, R3, R4 y las fuentes V1, considerando el sentido de la corriente.
                        </li>
                        <li><b>Planteamiento del sistema de ecuaciones:</b><br>
                            Escribe una ecuación para cada malla. Si dos mallas comparten una resistencia, la caída de tensión en esa resistencia depende de la diferencia de corrientes.<br>
                            <div class="math-block">$$ {latex_mallas} $$</div>
                        </li>
                        <li><b>Expresión matricial:</b><br>
                            El sistema se puede escribir en forma de matrices, lo que facilita su resolución con métodos algebraicos o computacionales.<br>
                            <div class="math-block">$$ {latex_matriz} $$</div>
                        </li>
                        <li><b>Reemplazo de valores numéricos:</b><br>
                            Sustituye los valores de resistencias y voltajes en la matriz y el vector de términos independientes.<br>
                            <div class="math-block">$$ {latex_sistema} $$</div>
                        </li>
                        <li><b>Resolución del sistema:</b><br>
                            Resuelve el sistema de ecuaciones lineales (por ejemplo, usando la regla de Cramer, matrices inversas o herramientas como Python y NumPy) para encontrar las corrientes de cada malla.<br>
                            <b>Consejo:</b> Si el sistema no tiene solución única, revisa que no haya errores en el planteamiento o valores inconsistentes.
                        </li>
                        <li><b>Interpretación de resultados:</b><br>
                            Analiza el sentido y magnitud de las corrientes. Un valor negativo indica que la corriente real va en sentido opuesto al supuesto.
                        </li>
                    </ol>
                    <b>Resumen:</b> El método de mallas es una técnica sistemática y poderosa para analizar circuitos complejos, permitiendo optimizar el diseño y la seguridad de instalaciones eléctricas residenciales.
                </div>
            </section>
            <section>
                <h2 class="section-title">Importancia del análisis de mallas</h2>
                <div class="explanation">
                    El método de mallas facilita el diseño eficiente de sistemas eléctricos residenciales, permitiendo:
                    <ul>
                        <li>Optimizar el uso de materiales y energía.</li>
                        <li>Prevenir sobrecargas y fallos eléctricos.</li>
                        <li>Garantizar la seguridad de los habitantes.</li>
                        <li>Reducir costos de instalación y operación.</li>
                    </ul>
                </div>
            </section>
        </main>
        <footer class="footer">
            &copy; 2024 - Simulación de Circuitos en Mallas | Proyecto académico<br>
            Tema: Optimización de sistemas de distribución de energía en instalaciones residenciales
        </footer>
    </body>
    </html>
    '''
    return render_template_string(html, vals=vals)

if __name__ == '__main__':
    app.run(debug=True)