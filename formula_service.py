import datetime
import sys
import math
import requests

from collections import defaultdict

from app_configuration import AppConfig


class FormulaServiceError(Exception):
    """Custom exception for formula service errors."""


class FormulaService:

    def __init__(self):
        # Initialize AppConfig once when an instance of FormulaService is created
        self.app_config = AppConfig()
        self.a_formula_data_url = self.app_config.a_formula_data_url
        self.r_formula_data_url = self.app_config.r_formula_data_url
        self.post_rating_formula_data_url = self.app_config.post_rating_formula_data_url
        self.karma_formula_data_url = self.app_config.karma_formula_data_url
        self.karma_level_formula_data_url = self.app_config.karma_level_formula_data_url


    class FloatValidator:
        @staticmethod
        def is_valid_float(number):
            if number is None:
                return False
            if not isinstance(number, float):
                return False
            return abs(number) <= sys.float_info.max

    class AData:
        def __init__(self):
            self.final_formula_result = None
            self.user_id = None
            self.unique_impression_sum_iterations = None
            self.unique_impression_sum_result = None
            self.unique_view_sum_iterations = None
            self.unique_view_sum_result = None
            self.unique_full_view_sum_iterations = None
            self.unique_full_view_sum_result = None
            self.impression_sum_iterations = None
            self.impression_sum_result = None
            self.view_sum_iterations = None
            self.view_sum_result = None
            self.full_view_sum_iterations = None
            self.full_view_sum_result = None
            self.j_number = None
            self.c4 = None
            self.c5 = None
            self.c6 = None
            self.c7 = None
            self.c8 = None
            self.c9 = None
            self.k_j = None
            self.Ka_t0 = None
            self.f_t_tj_result = None
            self.I_j = None
            self.V_j = None
            self.F_j = None
            self.I_small_j = None
            self.V_small_j = None
            self.F_small_j = None

        def calculate_event_sum_result(self, times_to_sum, event_value, constant):
            result = 0.0
            for i in range(times_to_sum):
                iteration_result = constant * self.k_j * event_value * self.f_t_tj_result
                result += iteration_result
            return result

        def calculate_formula(self):
            self.unique_impression_sum_result = self.calculate_event_sum_result(self.unique_impression_sum_iterations,
                                                                                self.I_j,
                                                                                self.c4)

            self.unique_view_sum_result = self.calculate_event_sum_result(self.unique_view_sum_iterations,
                                                                          self.V_j,
                                                                          self.c5)

            self.unique_full_view_sum_result = self.calculate_event_sum_result(self.unique_full_view_sum_iterations,
                                                                               self.F_j,
                                                                               self.c6)

            self.impression_sum_result = self.calculate_event_sum_result(self.impression_sum_iterations,
                                                                         self.I_small_j,
                                                                         self.c7)

            self.view_sum_result = self.calculate_event_sum_result(self.view_sum_iterations,
                                                                   self.V_small_j,
                                                                   self.c8)

            self.full_view_sum_result = self.calculate_event_sum_result(self.full_view_sum_iterations,
                                                                        self.F_small_j,
                                                                        self.c9)

            formula_final_result = sum([
                self.unique_impression_sum_result,
                self.unique_view_sum_result,
                self.unique_full_view_sum_result,
                self.impression_sum_result,
                self.view_sum_result,
                self.full_view_sum_result
            ])

            if not FormulaService.FloatValidator.is_valid_float(formula_final_result):
                raise ValueError("A(t) formula resulted in an invalid float result")

            self.final_formula_result = formula_final_result
            return self

    class RData:
        def __init__(self):
            self.final_formula_result = None
            self.user_id = None
            self.c10 = None
            self.c11 = None
            self.c12 = None
            self.c13 = None
            self.c14 = None
            self.r_j = None
            self.l_j = None
            self.m_j = None
            self.s_j = None
            self.p_j = None
            self.k_j = None
            self.g_t_tj_result = None
            self.y_t_tj_result = None
            self.reply_function_sum_result = None
            self.reply_function_iterations_num = None
            self.like_function_sum_result = None
            self.like_function_iterations_num = None
            self.master_class_function_sum_result = None
            self.master_class_iterations_num = None
            self.comment_function_sum_result = None
            self.comment_function_iterations_num = None
            self.payment_function_sum_result = None
            self.payment_function_iterations_num = None

        def calculate_event_sum_result(self, times_to_sum, event_value, constant, decreasing_function_result):
            result = 0.0
            for i in range(times_to_sum):
                iteration_result = constant * self.k_j * event_value * decreasing_function_result
                result += iteration_result
            return result

        def calculate_formula(self):
            self.reply_function_sum_result = self.calculate_event_sum_result(self.reply_function_iterations_num,
                                                                             self.r_j,
                                                                             self.c10,
                                                                             self.g_t_tj_result)

            self.like_function_sum_result = self.calculate_event_sum_result(self.like_function_iterations_num,
                                                                            self.l_j,
                                                                            self.c11,
                                                                            self.g_t_tj_result)

            self.master_class_function_sum_result = self.calculate_event_sum_result(self.master_class_iterations_num,
                                                                                    self.m_j,
                                                                                    self.c12,
                                                                                    self.y_t_tj_result)

            self.comment_function_sum_result = self.calculate_event_sum_result(self.comment_function_iterations_num,
                                                                               self.s_j,
                                                                               self.c13,
                                                                               self.y_t_tj_result)

            self.payment_function_sum_result = self.calculate_event_sum_result(self.payment_function_iterations_num,
                                                                               self.p_j,
                                                                               self.c14,
                                                                               self.y_t_tj_result)

            formula_final_result = sum([
                self.reply_function_sum_result,
                self.like_function_sum_result,
                self.master_class_function_sum_result,
                self.comment_function_sum_result,
                self.payment_function_sum_result
            ])

            if not FormulaService.FloatValidator.is_valid_float(formula_final_result):
                raise ValueError("R(t) formula resulted in an invalid float result")

            self.final_formula_result = formula_final_result
            return self


    class PostRatingData:
        def __init__(self):
            self.final_formula_result = None
            self.user_id = None
            self.c1 = None
            self.c2 = None
            self.c3 = None
            self.k_j = None
            self.Ka_t0 = None
            self.A_t_result = None
            self.R_t_result = None

        def calculate_formula(self):
            self.final_formula_result = self.c1 * self.k_j * self.Ka_t0 * (self.c2 * self.A_t_result + self.c3 * self.R_t_result)
            return self

    class KarmaFormulaData:
        def __init__(self):
            self.final_formula_result = None
            self.user_id = None
            self.c15 = None
            self.p_a = None
            self.n_sub = None
            self.t_r = None  # datetime object
            self.h_t_tr_result = None
            self.z_n_result = None
            self.c_reg = None
            self.alpha = None
            self.post_rating_function_result = None
            self.post_rating_sum_iterations = None

        def calculate_post_rating_sum(self):
            result = 0.0
            for _ in range(self.post_rating_sum_iterations):
                result += self.post_rating_function_result
            return result

        def calculate_formula(self):
            final_formula_result = self.c15 * self.p_a * self.z_n_result * self.h_t_tr_result * self.calculate_post_rating_sum() + self.c_reg + self.alpha
            decreased_karma_result = self.decrease_karma_result(final_formula_result)
            self.final_formula_result = decreased_karma_result
            return self

        def decrease_karma_result(self, value):
            # Implement any decreasing operations here
            return value


    class KarmaLevelData:
        def __init__(self):
            self.final_formula_result = None
            self.user_id = None
            self.c16 = None
            self.K_t = None

        def calculate_karma_level_formula(self):
            if self.K_t is None or self.K_t <= 0:
                raise ValueError("K_t cannot be null or less than 0")

            if self.c16 is None or self.c16 <= 0:
                raise ValueError("c16 cannot be null or less than 0")

            # Calculate the natural logarithm of K(t) and multiply by the constant c16
            result = abs(self.c16 * math.log(self.K_t))
            self.final_formula_result = float(result)
            return self

    def build_and_calculate_a_data(self, user_id):

        url_template = self.a_formula_data_url

        safe_format = defaultdict(str, user_id=user_id)
        url = url_template.format_map(safe_format)
        response = requests.get(url)
        if response.status_code != 200:
            raise FormulaServiceError("Failed to fetch A(t) formula data from server")

        data = response.json()

        a_data = self.AData()
        a_data.user_id = user_id
        a_data.F_j = data["F_j"]
        a_data.F_small_j = data["F_small_j"]
        a_data.I_j = data["I_j"]
        a_data.I_small_j = data["I_small_j"]
        a_data.Ka_t0 = data["Ka_t0"]
        a_data.V_j = data["V_j"]
        a_data.V_small_j = data["V_small_j"]
        a_data.c4 = data["c4"]
        a_data.c5 = data["c5"]
        a_data.c6 = data["c6"]
        a_data.c7 = data["c7"]
        a_data.c8 = data["c8"]
        a_data.c9 = data["c9"]
        a_data.f_t_tj_result = data["f_t_tj_result"]
        a_data.k_j = data["k_j"]
        a_data.impression_sum_iterations = data["impression_sum_iterations"]
        a_data.full_view_sum_iterations = data["full_view_sum_iterations"]
        a_data.unique_full_view_sum_iterations = data["unique_full_view_sum_iterations"]
        a_data.unique_impression_sum_iterations = data["unique_impression_sum_iterations"]
        a_data.unique_view_sum_iterations = data["unique_view_sum_iterations"]
        a_data.view_sum_iterations = data["view_sum_iterations"]

        # Calculate formula
        result = a_data.calculate_formula()
        return result

    def build_and_calculate_r_data(self, user_id):

        url_template = self.r_formula_data_url

        safe_format = defaultdict(str, user_id=user_id)
        url = url_template.format_map(safe_format)
        response = requests.get(url)
        if response.status_code != 200:
            raise FormulaServiceError("Failed to fetch R(t) data from server")

        data = response.json()

        r_data = self.RData()
        r_data.user_id = user_id
        r_data.c10 = data["c10"]
        r_data.c11 = data["c11"]
        r_data.c12 = data["c12"]
        r_data.c13 = data["c13"]
        r_data.c14 = data["c14"]
        r_data.r_j = data["r_j"]
        r_data.l_j = data["l_j"]
        r_data.m_j = data["m_j"]
        r_data.s_j = data["s_j"]
        r_data.p_j = data["p_j"]
        r_data.k_j = data["k_j"]
        r_data.like_function_iterations_num = data["like_function_iterations_num"]
        r_data.reply_function_iterations_num = data["reply_function_iterations_num"]
        r_data.master_class_iterations_num = data["master_class_iterations_num"]
        r_data.comment_function_iterations_num = data["comment_function_iterations_num"]
        r_data.payment_function_iterations_num = data["payment_function_iterations_num"]
        r_data.g_t_tj_result = data["g_t_tj_result"]
        r_data.y_t_tj_result = data["y_t_tj_result"]

        # Calculate formula
        result = r_data.calculate_formula()
        return result

    def build_init_data_for_post_rating_formula(self, user_id):
        post_rating_external_data = self.request_post_rating_data_external(user_id)
        # Additional calculations
        a_data = self.build_and_calculate_a_data(user_id)
        post_rating_external_data.A_t_result = a_data.final_formula_result

        r_data = self.build_and_calculate_r_data(user_id)
        post_rating_external_data.R_t_result = r_data.final_formula_result
        return post_rating_external_data

    def request_post_rating_data_external(self, user_id):
        url_template = self.post_rating_formula_data_url

        safe_format = defaultdict(str, user_id=user_id)
        url = url_template.format_map(safe_format)
        response = requests.get(url)
        if response.status_code != 200:
            raise FormulaServiceError("Failed to fetch PostRating formula data from server")

        data = response.json()

        post_rating_external_data = self.PostRatingData()
        post_rating_external_data.user_id = user_id
        post_rating_external_data.c1 = data["c1"]
        post_rating_external_data.c2 = data["c2"]
        post_rating_external_data.c3 = data["c3"]
        post_rating_external_data.k_j = data["k_j"]
        post_rating_external_data.Ka_t0 = data["Ka_t0"]

        return post_rating_external_data

    def request_karma_formula_data_external(self, user_id):
        url_template = self.karma_formula_data_url

        safe_format = defaultdict(str, user_id=user_id)
        url = url_template.format_map(safe_format)
        response = requests.get(url)
        if response.status_code != 200:
            raise FormulaServiceError("Failed to fetch Karma formula data from server")

        data = response.json()

        karma_formula_data = self.KarmaFormulaData()
        karma_formula_data.user_id = user_id
        karma_formula_data.c15 = data["c15"]
        karma_formula_data.p_a = data["p_a"]
        karma_formula_data.n_sub = data["n_sub"]
        karma_formula_data.c_reg = data["c_reg"]
        karma_formula_data.alpha = data["alpha"]
        karma_formula_data.post_rating_sum_iterations = data["post_rating_sum_iterations"]
        karma_formula_data.h_t_tr_result = data["h_t_tr_result"]
        karma_formula_data.z_n_result = data["z_n_result"]

        return karma_formula_data

    def request_karma_level_data_external(self, user_id):
        url_template = self.karma_level_formula_data_url

        safe_format = defaultdict(str, user_id=user_id)
        url = url_template.format_map(safe_format)
        response = requests.get(url)
        if response.status_code != 200:
            raise FormulaServiceError("Failed to fetch Karma Level formula data from server")

        data = response.json()

        karma_level_data = self.KarmaLevelData()
        karma_level_data.user_id = user_id
        karma_level_data.c16 = data["c16"]

        return karma_level_data

    class CalculationResult:
        def __init__(self, karma_value, karma_lvl_value):
            self.karma_value = karma_value
            self.karma_lvl_value = karma_lvl_value

    def calculate_for_user(self, user_id):
        post_rating_data = self.build_init_data_for_post_rating_formula(user_id)
        calculated_post_rating_data = post_rating_data.calculate_formula()

        initiated_karma_formula = self.request_karma_formula_data_external(user_id)
        initiated_karma_formula.post_rating_function_result = calculated_post_rating_data.final_formula_result

        calculated_karma_formula_data = initiated_karma_formula.calculate_formula()

        karma_level_data = self.request_karma_level_data_external(user_id)
        karma_level_data.K_t = calculated_karma_formula_data.final_formula_result

        calculated_karma_level_data = karma_level_data.calculate_karma_level_formula()

        return self.CalculationResult(karma_value=calculated_karma_formula_data.final_formula_result,
                                      karma_lvl_value=calculated_karma_level_data.final_formula_result)


# formula_service = FormulaService()
# calculation_result = formula_service.calculate_for_user(1)
# print("Karma Rating: ", calculation_result.karma_value)
# print("KarmaLevel Rating: ", calculation_result.karma_lvl_value)
#
# todo:
#                 1*) Расчет A(t) R(t) S(t) K(t) и L(t) формулы и остальных
#                 1.1*) предусмотреть метод понижения значения кармы оставить пустым
#                 2) Запрос данных отдельно по каждой формуле клиентом
#                 4) обновление данных запросом к адаптеру
#                 6) тесты
#                 7) работа с датафреймом
#                 7.1) запрос данных не из ксв а из базы
#                 7.2) ручка по добавлению инфы в датасет
#                 8) документация на сервис кармы и датасет