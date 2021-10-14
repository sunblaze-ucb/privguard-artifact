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
sys.path.append(os.environ.get('PRIVGUARD') + '/src/parser')
sys.path.append(os.environ.get('PRIVGUARD') + "/src/stub_libraries")

from importlib.util import spec_from_file_location, module_from_spec
import json
from shutil import copyfile
import argparse

from attribute import Satisfied
from policy_tree import Policy

import stub_pandas
import stub_numpy
import stub_lightgbm

def analyze(module, data_folder):
    records = module.run(data_folder, lightgbm=stub_lightgbm, numpy=stub_numpy, pandas=stub_pandas)
    residual_policy = records.policy.policy
    return residual_policy

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--script', help='Path to the program', default='./examples/program/trans_pred_example.py')# default='./examples/program/ehr_example.py')
    parser.add_argument('--data_folder', help='Path to the data', default='./examples/data/trans_pred_example/')#default='./examples/data/ehr_example/')
    return parser.parse_args()

if __name__ == '__main__':

    args = parse()

    spec = spec_from_file_location("default_module", args.script)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    residual_policy = analyze(module, args.data_folder)
    print(residual_policy)
