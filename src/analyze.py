# MIT License

# Copyright (c) 2021 sunblaze-ucb

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" PrivAnalyzer. """

import os
import sys
sys.path.append(os.path.join(os.environ.get('PRIVGUARD'), 'src/parser'))
sys.path.append(os.path.join(os.environ.get('PRIVGUARD'), "src/stub_libraries"))

from importlib.util import spec_from_file_location, module_from_spec
import json
from shutil import copyfile
import argparse

from attribute import Satisfied
from policy_tree import Policy

import stub_pandas
import stub_numpy
import stub_numpy.random as stub_random
import stub_lightgbm
import stub_xgboost
import stub_statsmodels.tsa.arima.model as stub_arima
import stub_sklearn.cross_validation as stub_cross_validation
import stub_sklearn.metrics as stub_metrics
import stub_sklearn.model_selection as stub_model_selection

program_map = {
    0: "./examples/program/ehr_example.py",
    # 1: "./examples/program/1_fraud_detection.py",
    # 2: "./examples/program/2_fraud_detection.py",
    # 3: "./examples/program/3_merchant_recommendation.py",
    4: "./examples/program/4_customer_satisfaction_prediction.py",
    5: "./examples/program/5_customer_transaction_prediction.py",
    6: "./examples/program/6_customer_transaction_prediction.py",
    # 7: "./examples/program/7_bank_customer_classification.py",
    # 8: "./examples/program/8_bank_customer_segmentation.py",
    # 9: "./examples/program/9_credit_risk_analysis.py",
    # 10: "./examples/program/10_customer_churn_prediction.py",
    # 11: "./examples/program/11_heart_disease_causal_inference.py",
    # 12: "./examples/program/12_classify_forest_categories.py",
    # 13: "./examples/program/13_simple_lstm.py",
    # 14: "./examples/program/14_solve_titanic.py",
    # 15: "./examples/program/15_earthquake_prediction.py",
    # 16: "./examples/program/16_display_advertising.py",
    # 17: "./examples/program/17_fraud_detection.py",
    # 18: "./examples/program/18_restaurant_revenue_prediction.py",
    # 19: "./examples/program/19_nfl_analytics.py",
    # 20: "./examples/program/20_ncaa_prediction.py",
    # 21: "./examples/program/21_home_value_prediction.py",
    # 22: "./examples/program/22_malware_prediction.py",
    23: "./examples/program/23_web_traffic_forecasting.py",
}

data_map = {
    0: "./examples/data/ehr_example/",
    # 1: "./examples/data/fraud_detection_1/",
    # 2: "./examples/data/fraud_detection_1/",
    # 3: "./examples/data/merchant_recommendation/",
    4: "./examples/data/customer_satisfaction_prediction/",
    5: "./examples/data/customer_transaction_prediction/",
    6: "./examples/data/customer_transaction_prediction/",
    # 7: "./examples/data/bank_customer_classification/",
    # 8: "./examples/data/bank_customer_segmentation/",
    # 9: "./examples/data/credit_risk_analysis/",
    # 10: "./examples/data/customer_churn_prediction/",
    # 11: "./examples/data/heart_disease_causal_inference/",
    # 12: "./examples/data/classify_forest_categories/",
    # 13: "./examples/data/simple_lstm/",
    # 14: "./examples/data/solve_titanic/",
    # 15: "./examples/data/earthquake_prediction/",
    # 16: "./examples/data/display_advertising/",
    # 17: "./examples/data/fraud_detection_2/",
    # 18: "./examples/data/restaurant_revenue_prediction/",
    # 19: "./examples/data/nfl_analytics/",
    # 20: "./examples/data/ncaa_prediction/",
    # 21: "./examples/data/home_value_prediction/",
    # 22: "./examples/data/malware_prediction/",
    23: "./examples/data/web_traffic_forecasting/",
}

lib_map = {
    0: {'numpy':stub_numpy, 'pandas':stub_pandas},
    4: {'cross_validation': stub_cross_validation, 'metrics': stub_metrics, 'numpy': stub_numpy, 'pandas': stub_pandas, 'xgboost': stub_xgboost},
    5: {'lgb':stub_lightgbm, 'metrics': stub_metrics, 'model_selection':stub_model_selection, 'numpy':stub_numpy, 'pandas':stub_pandas, 'random':stub_random},
    6: {'numpy':stub_numpy, 'pandas':stub_pandas},
    23: {'numpy':stub_numpy, 'pandas':stub_pandas, 'arima': stub_arima},
}

def analyze(module, data_folder, lib_list):
    return module.run(data_folder, lightgbm=stub_lightgbm, **lib_list)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--example_id', help='The example program ID', type=int, default=6)
    args = parser.parse_args()
    return program_map[args.example_id], data_map[args.example_id], lib_map[args.example_id]

if __name__ == '__main__':

    script, data_folder, lib_list = parse()

    spec = spec_from_file_location("default_module", script)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    result = analyze(module, data_folder, lib_list)
    print("\nResidual policy of the output:\n" + str(result))
