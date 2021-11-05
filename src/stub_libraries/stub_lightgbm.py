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

""" Function summaries for the lightgbm library. """

import stub_numpy as np
import stub_pandas as pd
import math
from blackbox import Blackbox
from stub_numpy import ndarray

class Dataset(Blackbox):
    
    def __init__(self, data, label=None, reference=None, weight=None, group=None, init_score=None, silent=False, feature_name='auto', categorical_feature='auto', params=None, free_raw_data=True):
        self.data = data
        self.label = label
        self.policy = data.policy

    def num_features(self):

        return len(self.data.schema)

class LGBMClassifier:

    def __init__(self, boosting_type='gbdt', num_leaves=31, max_depth=-1, learning_rate=0.1, n_estimators=100, subsample_for_bin=200000, objective=None, class_weight=None, min_split_gain=0.0, min_child_weight=0.001, min_child_samples=20, subsample=1.0, subsample_freq=0, colsample_bytree=1.0, reg_alpha=0.0, reg_lambda=0.0, random_state=None, n_jobs=-1, silent=True, importance_type='split', **kwargs):
        self.data = None
        self.label = None

    def fit(self, X, y, sample_weight=None, init_score=None, eval_set=None, eval_names=None, eval_sample_weight=None, eval_class_weight=None, eval_init_score=None, eval_metric=None, early_stopping_rounds=None, verbose=True, feature_name='auto', categorical_feature='auto', callbacks=None):

        self.data = X
        self.label = y
        return Blackbox((X.policy.join(y.policy)).runPrivacy('Aggregation'))

    def predict_proba(self, X, raw_score=False, num_iteration=None, pred_leaf=False, pred_contrib=False, **kwargs):

        result = pd.concat([pd.merge(self.data, self.label), pd.merge(X, self.label)]) 
        return Blackbox(result)

    def __str__(self):
        return 'LGBMClassifier'

    __repr__ = __str__

class Booster(Blackbox):
    def __init__(self, params=None, train_set=None, model_file=None, model_str=None, silent='warn'):
        self.policy = train_set.policy
        self.best_iteration = 0

    def predict(self, data, start_iteration=0, num_iteration=None, raw_score=False, pred_leaf=False, pred_contrib=False, data_has_header=False, is_reshape=True, **kwargs):
        return ndarray(self.policy.join(data.policy))

def train(params, train_set, num_boost_round=100, valid_sets=None, valid_names=None, fobj=None, feval=None, init_model=None, feature_name='auto', categorical_feature='auto', early_stopping_rounds=None, evals_result=None, verbose_eval='warn', learning_rates=None, keep_training_booster=False, callbacks=None):
    return Booster(params=params, train_set=train_set)
