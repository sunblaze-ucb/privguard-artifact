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

""" Black-box values whose policies can not be further satisfied. """

import os
import sys
sys.path.append(os.environ.get('PRIVGUARD') + "/src/parser")

import stub_pandas as pd
from functools import partial, reduce
from policy_tree import Policy, DNF


class Blackbox:

    def __init__(self, policy=Policy(DNF([])), *args, **kwargs):

        self.policy = policy
        #self._add_data(list(args) + list(kwargs.values()))

    def _add_data(self, data_list):

        policy = self.policy
        for data in data_list:
            if data in [pd.DataFrame]:
                policy = self.policy.join(data.policy)
        self.policy = policy
        return policy

    def method_missing(self, _name, *args, **kwargs):

        print(f'Blackbox method missing: {_name}')
        self._add_data(list(args) + list(kwargs.values()))
        return self

    def __getattr__(self, _name):
        if _name == 'parentDF':
            raise RuntimeError('Black box has no parent dataframe')
        return partial(self.method_missing, _name)

    def __getitem__(self, key):
        return self

    def __pow__(self, other):
        self._add_data([other])
        return self

    def __truediv__(self, other):
        self._add_data([other])
        return self

    def __rtruediv__(self, other):
        self._add_data([other])
        return self

    def __mul__(self, other):
        self._add_data([other])
        return self

    def __rmul__(self, other):
        self._add_data([other])
        return self

    def __add__(self, other):
        self._add_data([other])
        return self

    def __radd__(self, other):
        self._add_data([other])
        return self

    def __gt__(self, other):
        self._add_data([other])
        return self

    def __lt__(self, other):
        self._add_data([other])
        return self

