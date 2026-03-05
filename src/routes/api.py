import logging

from flask import Blueprint, jsonify, request

from src.config import REQUIRED_PARAMS
from src.services.mesh_analyzer import MeshAnalyzer, get_example_values
from src.validators.inputs import validate_api_payload

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/calculate", methods=["POST"])
def api_calculate():
    try:
        data = request.get_json()
        params, error = validate_api_payload(data)
        if error:
            return jsonify({"error": error}), 400

        R1, R2, R3, R4, R5, R6 = (params[key] for key in REQUIRED_PARAMS[:6])
        V1, V2, V3 = (params[key] for key in REQUIRED_PARAMS[6:])

        I1, I2, I3, A, B = MeshAnalyzer.calcular_corrientes(R1, R2, R3, R4, R5, R6, V1, V2, V3)
        interpretaciones = MeshAnalyzer.interpretar_corrientes(I1, I2, I3)

        return jsonify(
            {
                "success": True,
                "currents": {"I1": I1, "I2": I2, "I3": I3},
                "matrix_A": A.tolist(),
                "vector_B": B.tolist(),
                "interpretations": interpretaciones,
            }
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        logger.error(f"Error en API: {exc}")
        return jsonify({"error": "Error interno del servidor"}), 500


@api_bp.route("/example", methods=["GET"])
def api_example():
    return jsonify(get_example_values())
