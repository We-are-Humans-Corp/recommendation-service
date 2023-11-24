# controller.py
import logging
from colorama import init, Fore
from flask import Flask, request, jsonify
from recommendation_service import RecommendationService
from data_access import DataAccess
from app_configuration import AppConfig

# Initialize Colorama for colored console output
init()
class ColoredConsoleHandler(logging.StreamHandler):
    COLORS = {
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.DEBUG: Fore.WHITE,
        logging.INFO: Fore.WHITE,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        formatter = logging.Formatter(f'{color}[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s{Fore.RESET}', datefmt='%Y-%m-%d %H:%M:%S %z')
        return formatter.format(record)

# Customizing logging to use the colored console handler
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.handlers[0] = ColoredConsoleHandler()

app = Flask(__name__)
config = AppConfig()

csv_repo = DataAccess(config.csv_path)
rec_service = RecommendationService(csv_repo)


class RecommendationController:
    @staticmethod
    @app.route('/v1/recommend', methods=['POST'])
    def recommend():
        try:

            data = request.json

            user_id = data.get('user_id')
            user_col = data.get('user_column_name')
            item_col = data.get('item_column_name')
            rating_col = data.get('rating_column_name')
            response_size = data.get('response_size')
            algo = data.get('algo', 'KNN')  # Default to KNN if not provided

            logging.getLogger(RecommendationController.__name__).info(f"User ID: '{user_id}', Algorithm: '{algo}'")

            if algo not in ['KNN', 'SVD']:
                raise ValueError("Invalid algorithm choice. Must be 'KNN' or 'SVD'.")

            # Corrected call to get_recommendations with proper number of arguments
            top_recommendations = rec_service.get_recommendations(user_id, user_col, item_col, rating_col, response_size, algo)
            return jsonify(top_recommendations.to_dict(orient='records'))
        except Exception as e:
            logging.getLogger(RecommendationController.__name__).error("Error in /v1/recommend: %s", e)
            return jsonify({"error_type": type(e).__name__, "error_message": str(e)}), 503


class HealthController:
    @staticmethod
    @app.route('/health', methods=['GET'])
    def health_check():
        logging.getLogger(HealthController.__name__).info("Health check invoked")
        #logging.getLogger(HealthController.__name__).debug("Health check invoked")
        #logging.getLogger(HealthController.__name__).warning("Health check invoked")
        #logging.getLogger(HealthController.__name__).error("Health check invoked")
        return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=config.http_port)
