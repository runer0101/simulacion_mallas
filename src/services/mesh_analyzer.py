from typing import Dict, Optional, Tuple
import logging

import numpy as np

logger = logging.getLogger(__name__)


class MeshAnalyzer:
    """Clase para el análisis de circuitos de mallas residenciales."""

    RESISTANCE_RANGE = (0.01, 1000.0)
    VOLTAGE_RANGE = (0.0, 500.0)

    @staticmethod
    def validate_parameters(params: Dict[str, float]) -> None:
        for key, value in params.items():
            if not isinstance(value, (int, float)) or np.isnan(value) or np.isinf(value):
                raise ValueError(f"{key}: Debe ser un número válido")

            if key.startswith('R'):
                if value <= 0:
                    raise ValueError(f"{key}: Debe ser un valor positivo")
                min_val, max_val = MeshAnalyzer.RESISTANCE_RANGE
                if not (min_val <= value <= max_val):
                    raise ValueError(f"{key}: Resistencia debe estar entre {min_val}Ω y {max_val}Ω")
            elif key.startswith('V'):
                min_val, max_val = MeshAnalyzer.VOLTAGE_RANGE
                if not (min_val <= value <= max_val):
                    raise ValueError(f"{key}: Voltaje debe estar entre {min_val}V y {max_val}V")

    @staticmethod
    def calcular_corrientes(
        R1: float,
        R2: float,
        R3: float,
        R4: float,
        R5: float,
        R6: float,
        V1: float,
        V2: float,
        V3: float,
    ) -> Tuple[float, float, float, np.ndarray, np.ndarray]:
        params = {
            'R1': R1,
            'R2': R2,
            'R3': R3,
            'R4': R4,
            'R5': R5,
            'R6': R6,
            'V1': V1,
            'V2': V2,
            'V3': V3,
        }
        MeshAnalyzer.validate_parameters(params)

        A = np.array(
            [
                [R1 + R4 + R6, -R4, -R6],
                [-R4, R2 + R4 + R5, -R5],
                [-R6, -R5, R3 + R5 + R6],
            ],
            dtype=np.float64,
        )
        B = np.array([V1, V2, V3], dtype=np.float64)

        det_A = np.linalg.det(A)
        if abs(det_A) < 1e-10:
            raise ValueError("Sistema singular: Las resistencias crean un circuito indeterminado")

        try:
            I = np.linalg.solve(A, B)
            max_current = max(abs(i) for i in I)
            if max_current > 1000:
                logger.warning(f"Corriente muy alta detectada: {max_current:.2f}A")
            return float(I[0]), float(I[1]), float(I[2]), A, B
        except np.linalg.LinAlgError as exc:
            raise ValueError(f"Error al resolver el sistema: {str(exc)}")
        except Exception as exc:
            raise ValueError(f"Error inesperado en el cálculo: {str(exc)}")

    @staticmethod
    def interpretar_corrientes(I1: float, I2: float, I3: float) -> Dict[str, str]:
        interpretaciones: Dict[str, str] = {}

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
    return {
        'R1': 0.5,
        'R2': 0.7,
        'R3': 0.6,
        'R4': 20,
        'R5': 15,
        'R6': 25,
        'V1': 120,
        'V2': 220,
        'V3': 120,
    }


def get_example_values() -> Dict[str, float]:
    return {
        'R1': 2.0,
        'R2': 4.0,
        'R3': 3.0,
        'R4': 6.0,
        'R5': 5.0,
        'R6': 2.0,
        'V1': 12.0,
        'V2': 0.0,
        'V3': 0.0,
    }


def parse_form_data(form_data: Dict, default_vals: Dict[str, float]) -> Tuple[Dict[str, float], Optional[str]]:
    vals = default_vals.copy()

    try:
        for key in vals.keys():
            form_value = form_data.get(key, '').strip()
            if form_value:
                form_value = form_value.replace(',', '.')
                vals[key] = float(form_value)

        MeshAnalyzer.validate_parameters(vals)
        return vals, None
    except ValueError as exc:
        return vals, str(exc)
    except Exception as exc:
        logger.error(f"Error inesperado al procesar formulario: {exc}")
        return vals, "Error al procesar los datos. Verifica el formato de los números."
