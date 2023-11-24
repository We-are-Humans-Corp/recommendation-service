import logging
from surprise import KNNBasic, SVD
from data_access import DataAccess
import numpy as np
import pandas as pd
import time

from app_configuration import AppConfig

from formula_service import FormulaService


class RecommendationServiceError(Exception):
    """Custom exception for recommendation service errors."""


class RecommendationService:

    config = AppConfig()

    CACHE_EXPIRY_TIME = config.trainset_cache_time
    trainset_cache = None
    last_cache_update = 0

    def __init__(self, data_access: DataAccess):
        if data_access is None:
            raise RecommendationServiceError("Data access object cannot be null")
        self.data_access = data_access
        self.algorithm = None
        self.formula_service = FormulaService()

    def train_model(self, user_col: str, item_col: str, rating_col: str, algo='KNN'):
        current_time = time.time()
        try:
            if not user_col:
                raise RecommendationServiceError("User column name cannot be null or empty")
            if not item_col:
                raise RecommendationServiceError("Item column name cannot be null or empty")
            if not rating_col:
                raise RecommendationServiceError("Rating column name cannot be null or empty")

            # Check if cache is expired
            if RecommendationService.trainset_cache is None or (
                    current_time - RecommendationService.last_cache_update) > RecommendationService.CACHE_EXPIRY_TIME:
                data = self.data_access.load_data_from_db(user_col, item_col, rating_col)
                RecommendationService.trainset_cache = data.build_full_trainset()
                RecommendationService.last_cache_update = current_time

            trainset = RecommendationService.trainset_cache

            # Choose the algorithm based on algo parameter
            if algo == 'KNN':
                self.algorithm = KNNBasic()
            elif algo == 'SVD':
                self.algorithm = SVD()
            else:
                raise RecommendationServiceError("Invalid algorithm choice")

            self.algorithm.fit(trainset)

        except RecommendationServiceError as e:
            logging.getLogger(RecommendationService.__name__).error(f"Error in recommendation service: {e}")
            raise RecommendationServiceError(e)

        except Exception as e:
            logging.getLogger(RecommendationService.__name__).error(f"Error in train_model: {e}")
            raise RecommendationServiceError(e)

    # todo изменить сигнатуру принимать дто
    def get_recommendations(self, user_id: int, user_col: str, item_col: str, rating_col: str, n=5, algo='KNN'):
        try:

            if user_id is None:
                raise RecommendationServiceError("User ID cannot be null")
            if not user_col:
                raise RecommendationServiceError("User column name cannot be null or empty")
            if not item_col:
                raise RecommendationServiceError("Item column name cannot be null or empty")
            if not rating_col:
                raise RecommendationServiceError("Rating column name cannot be null or empty")
            if n is None or n <= 0:
                raise RecommendationServiceError("Number of recommendations 'n' must be a positive integer")

            calculation_result = self.formula_service.calculate_for_user(user_id)

            logging.getLogger(RecommendationService.__name__).info(f"Karma lvl for user {user_id}: {calculation_result.karma_lvl_value}")

            self.train_model(user_col, item_col, rating_col, algo)
            predictions = self._predict_ratings(user_id, user_col, item_col, rating_col)

            pred_ratings = pd.DataFrame([(pred.uid, pred.iid, pred.est * calculation_result.karma_lvl_value) for pred in predictions],
                                        columns=[user_col, item_col, rating_col]).sort_values(rating_col, ascending=False)  # order control:  ascending=False

            recommendations = pred_ratings.head(n)

            return recommendations

        except RecommendationServiceError as e:
            logging.getLogger(RecommendationService.__name__).error(f"Error in get_recommendations: {e}")
            raise RecommendationServiceError(e)

        except Exception as e:
            logging.getLogger(RecommendationService.__name__).error(f"Unexpected error in get_recommendations: {e}")
            raise RecommendationServiceError(e)

    def _predict_ratings(self, user_id, user_col, item_col, rating_col):
        try:
            data_frame = self.data_access.get_postgres_data_frame(user_col, item_col, rating_col)
            unique_ids = data_frame[item_col].unique()
            items_rated_by_user = data_frame[data_frame[user_col] == user_id][item_col].unique()
            items_to_predict = np.setdiff1d(unique_ids, items_rated_by_user)

            predictions = [self.algorithm.predict(user_id, item_id) for item_id in items_to_predict]
            return predictions

        except Exception as e:
            logging.getLogger(RecommendationService.__name__).error(f"Error in _predict_ratings: {e}")
            raise RecommendationServiceError(e)




