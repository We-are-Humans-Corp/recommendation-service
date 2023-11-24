# app_configuration.py
import os
import yaml

class AppConfig:
    def __init__(self):
        self.config = {}
        self.load_config()

    def load_config(self):
        config_path = os.environ.get('CONFIG_PATH', 'application.yml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    @property
    def postgres_url(self):
        return self.config['service-configuration']['data-layer']['postgres']['url']

    @property
    def postgres_schema(self):
        return self.config['service-configuration']['data-layer']['postgres']['schema']

    @property
    def postgres_table(self):
        return self.config['service-configuration']['data-layer']['postgres']['table']

    @property
    def csv_path(self):
        return self.config['service-configuration']['data-layer']['csv']['path_to_file']

    @property
    def http_port(self):
        return self.config['service-configuration']['http']['port']

    @property
    def a_formula_data_url(self):
        return self.config['service-configuration']['data-layer']['adapter']['a-formula-data-url']

    @property
    def r_formula_data_url(self):
        return self.config['service-configuration']['data-layer']['adapter']['r-formula-data-url']

    @property
    def post_rating_formula_data_url(self):
        return self.config['service-configuration']['data-layer']['adapter']['post-rating-formula-data-url']

    @property
    def karma_formula_data_url(self):
        return self.config['service-configuration']['data-layer']['adapter']['karma-formula-data-url']

    @property
    def karma_level_formula_data_url(self):
        return self.config['service-configuration']['data-layer']['adapter']['karma-level-formula-data-url']

    @property
    def trainset_cache_time(self):
        return self.config['service-configuration']['cache']['trainset']

    @property
    def engine_pool_size(self):
        return self.config['service-configuration']['data-layer']['postgres']['sql-engine']['pool-size']


    @property
    def engine_pool_timeout_in_s(self):
        return self.config['service-configuration']['data-layer']['postgres']['sql-engine']['pool-timeout-in-s']

    @property
    def engine_pool_recycle_in_s(self):
        return self.config['service-configuration']['data-layer']['postgres']['sql-engine']['pool-recycle-in-s']



