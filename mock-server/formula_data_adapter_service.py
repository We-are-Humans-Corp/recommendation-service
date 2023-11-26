from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

class KarmaFormulaData:
    def __init__(self, user_id):
        self.final_formula_result = None
        self.user_id = user_id
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

# Endpoint: GET /v1/formula-data/karma-formula/:userId
@app.route('/v1/formula-data/karma-formula/<userId>', methods=['GET'])
def karma_formula(userId):
    karma_formula_data = KarmaFormulaData(user_id=userId)

    karma_formula_data.c15 = 1.0
    karma_formula_data.p_a = 1.0
    karma_formula_data.n_sub = 1.0
    #karma_formula_data.t_r = int(datetime.datetime.now().timestamp())
    karma_formula_data.c_reg = 1.0
    karma_formula_data.alpha = 1.0

    karma_formula_data.post_rating_sum_iterations = 2
    karma_formula_data.h_t_tr_result = 1.0
    karma_formula_data.z_n_result = 1.0

    response = {attr: getattr(karma_formula_data, attr) for attr in vars(karma_formula_data)}

    return jsonify(response)

# Endpoint 2: GET /v1/formula-data/a-formula/:userId
class AData:
    def __init__(self, user_id):
        self.final_formula_result = None
        self.user_id = user_id
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

# Endpoint: GET /v1/formula-data/a-formula/:userId
@app.route('/v1/formula-data/a-formula/<userId>', methods=['GET'])
def a_formula(userId):
    a_data = AData(user_id=userId)

    a_data.impression_sum_iterations = 2
    a_data.view_sum_iterations = 2
    a_data.unique_impression_sum_iterations = 2
    a_data.full_view_sum_iterations = 2
    a_data.unique_full_view_sum_iterations = 2
    a_data.unique_view_sum_iterations = 2

    a_data.c4 = 1.0
    a_data.c5 = 1.0
    a_data.c6 = 1.0
    a_data.c7 = 1.0
    a_data.c8 = 1.0
    a_data.c9 = 1.0
    a_data.k_j = 1.0
    a_data.Ka_t0 = 1.0

    a_data.f_t_tj_result = 1.0

    a_data.I_j = 1.0
    a_data.V_j = 1.0
    a_data.F_j = 1.0
    a_data.I_small_j = 1.0
    a_data.V_small_j = 1.0
    a_data.F_small_j = 1.0

    response = {attr: getattr(a_data, attr) for attr in vars(a_data)}
    return jsonify(response)

class RData:
    def __init__(self, user_id):
        self.final_formula_result = None
        self.user_id = user_id
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

# Endpoint: GET /v1/formula-data/r-formula/:userId
@app.route('/v1/formula-data/r-formula/<userId>', methods=['GET'])
def r_data(userId):
    r_data = RData(user_id=userId)

    r_data.c10 = 1.0
    r_data.c11 = 1.0
    r_data.c12 = 1.0
    r_data.c13 = 1.0
    r_data.c14 = 1.0

    r_data.r_j = 1.0
    r_data.l_j = 1.0
    r_data.m_j = 1.0
    r_data.s_j = 1.0
    r_data.p_j = 1.0

    r_data.k_j = 1.0

    r_data.like_function_iterations_num = 2
    r_data.reply_function_iterations_num = 2
    r_data.master_class_iterations_num = 2
    r_data.comment_function_iterations_num = 2
    r_data.payment_function_iterations_num = 2

    r_data.g_t_tj_result = 1.0
    r_data.y_t_tj_result = 1.0

    response = {attr: getattr(r_data, attr) for attr in vars(r_data)}
    return jsonify(response)

class KarmaLevelData:
    def __init__(self, user_id):
        self.final_formula_result = None
        self.user_id = user_id
        self.c16 = None
        self.K_t = None

# Endpoint: GET /v1/formula-data/karma-level/:userId
@app.route('/v1/formula-data/karma-level/<userId>', methods=['GET'])
def karma_level(userId):
    karma_level_data = KarmaLevelData(user_id=userId)
    karma_level_data.c16 = 1.0

    # Convert the object to a dictionary for JSON response
    response = {attr: getattr(karma_level_data, attr) for attr in vars(karma_level_data)}
    return jsonify(response)

class PostRatingData:
    def __init__(self, user_id):
        self.final_formula_result = None
        self.user_id = user_id
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.k_j = None
        self.Ka_t0 = None
        self.A_t_result = None
        self.R_t_result = None

# Endpoint: GET /v1/formula-data/post-rating/:userId
@app.route('/v1/formula-data/post-rating/<userId>', methods=['GET'])
def post_rating(userId):
    post_rating_external_data = PostRatingData(user_id=userId)

    post_rating_external_data.c1 = 1.0
    post_rating_external_data.c2 = 1.0
    post_rating_external_data.c3 = 1.0
    post_rating_external_data.k_j = 1.0
    post_rating_external_data.Ka_t0 = 1.0

    response = {attr: getattr(post_rating_external_data, attr) for attr in vars(post_rating_external_data)}
    return jsonify(response)


# Define the class for parsing incoming JSON data
class CalculationResult:
    def __init__(self, karma_value, karma_lvl_value, user_id):
        self.karma_value = karma_value
        self.karma_lvl_value = karma_lvl_value
        self.user_id = user_id

    def __repr__(self):
        return f"CalculationResult(karma_value={self.karma_value}, karma_lvl_value={self.karma_lvl_value})"


@app.route('/v1/update-info', methods=['POST'])
def update_info():
    data = request.get_json()
    # Create an instance of CalculationResult
    calculation_result = CalculationResult(**data)
    print(f"CalculationResult(karma_value={calculation_result.karma_value}, karma_lvl_value={calculation_result.karma_lvl_value}, user_id={calculation_result.user_id})")

    return jsonify({"message": "Data received successfully"}), 200

if __name__ == '__main__':
    app.run(port=5002)
