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

""" Function summaries for the numpy library. """

import os
import sys
sys.path.append(os.path.join(os.environ.get('PRIVGUARD'), "src/parser"))

import numpy as np
import stub_pandas as pd
import math
from blackbox import Blackbox
from policy_tree import Policy
from utils import UniversalIndex
from tabular import Tabular

int8 = np.int8
int64 = np.int64
nan = np.nan
ptp = np.ptp
float = np.float
newaxis = np.newaxis

class ndarray(Blackbox):

    def __getattr__(self, attr):
        if attr == 'shape':
            return UniversalIndex()

    def __format__(self, _):
        return str(self)

    def __str__(self):
        return f'ndarray({self.policy})'

    def __getitem__(self, key):
        return self

    def __setitem__(self, key, newvalue):
        return ndarray(policy=self.policy.join(newvalue.policy))

    def copy(self):
        return ndarray(policy=self.policy.copy())

def arange(shape, *args, **kwargs):
    return ndarray()

def array(obj, *args, **kwargs):
    if isinstance(obj, Tabular):
        return ndarray(policy=obj.policy)
    else:
        raise NotImplementedError

def sum(a, **kwargs):
    newPolicy = Policy()
    for x in a:
        newPolicy = newPolicy.join(x.policy)
    return Blackbox(newPolicy)

def vstack(arr, *args, **kwargs):
    policy = arr[0].policy
    for i in range(1, len(arr)):
        policy = policy.join(arr[i].policy)
    return ndarray(policy)

def concatenate(arr, *args, **kwargs):
    policy = arr[0].policy
    for i in range(1, len(arr)):
        policy = policy.join(arr[i].policy)
    return ndarray(policy)

def ones(shape, *args, **kwargs):
    return ndarray()

def zeros(shape, *args, **kwargs):
    return ndarray()

def tanh(x, **kwargs):
    return Blackbox(x.policy)

def log1p(x, **kwargs):
    return Blackbox(x.policy)

def exp(x, **kwargs):
    return Blackbox(x.policy)

def expm1(x, **kwargs):
    return Blackbox(x.policy)

def log(x, **kwargs): 
    return Blackbox(x.policy)

def corrcoef(x, y, **kwargs):
    return Blackbox(x.policy.join(y.policy))
