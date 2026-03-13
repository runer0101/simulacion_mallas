import logging
import os

from src.app_factory import create_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    logger.info("Iniciando servidor de simulación de mallas residenciales...")
    logger.info(f"Puerto: {port}, Debug: {debug_mode}")

    app.run(host="0.0.0.0", port=port, debug=debug_mode)
