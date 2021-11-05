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

""" Function summaries for the pandas library. """

import os
import sys
sys.path.append(os.path.join(os.environ.get('PRIVGUARD'), "src/parser"))

from tabular import Tabular
from blackbox import Blackbox
from utils import UniversalIndex
from stub_numpy import ndarray
from policy_tree import DNF, Policy
from attribute import Satisfied, Unsatisfiable
from abstract_domain import ClosedIntervalL
from typed_value import IntegerV, StringV, ExtendV

def read_csv(filename, schema=[], usecols=None, **kwargs):

    """ read DataFrame from a csv file. Policy is specified at the end of this file. """
    
    data_folder = filename[:filename.rfind("/")+1]
    with open(data_folder + 'policy.txt', 'r') as f:
        policy = Policy(f.read().rstrip())
        print(f'Policy of input data {filename}:\n' + str(policy))
    with open(data_folder + 'meta.txt', 'r') as f:
        complete_schema = f.readline().strip().replace('"', '').split(',')
        rows = int(f.readline())
        # print('Data Schema: ' + str(schema))

    if not schema and usecols == None:
        return DataFrame(complete_schema, policy, shape=[len(schema), rows])
    elif schema:
        return DataFrame(schema, policy, shape=[len(schema), rows])
    elif usecols is not None:
        return DataFrame(usecols, file_policy, shape=[len(usecols), rows])

class Series(Tabular):

    """
    Stub class for Pandas Series. Series class is only expected to serve as indicators for 
    filtering. Only Series originating from a DataFrame can be used to filter that DataFrame. 
    """

    def __init__(self, policy, column, parent, shape=None, interval=None):

        """
        Initialize an abstract Pandas Series. This class is only expected to serve as indicators
        for filtering. Indexing a DataFrame will return a Series object with interval=None. Calling
        methods of Series will return Series objects with interval being ClosedIntervalV object.
        """
        self.policy = policy
        self.column = column
        self.parent = parent
        self.shape = shape
        self.interval = interval

        self.values = ndarray(self.policy)

    def __getattr__(self, attr):
        if attr == 'iloc':
            return self
        else:
            raise NotImplementedError

    def __getitem__(self, key):
        if isinstance(key, UniversalIndex):
            return self

    def __ge__(self, other):

       if self.interval is None:
           return Series(Policy([[Unsatisfiable()]]), self.column, self.parent, shape=self.shape, interval=ClosedIntervalL(_to_abstract_value(other), ExtendV('inf')))
       else:
           raise ValueError(f'Trying to re-compare a indicator Series whose interval is {self.interval}.')

    def __le__(self, other):


       if self.interval is None:
           return Series(Policy([[Unsatisfiable()]]), self.column, self.parent, shape=self.shape, interval=ClosedIntervalL(ExtendV('ninf'), _to_abstract_value(other)))
       else:
           raise ValueError(f'Trying to re-compare a indicator Series whose interval is {self.interval}.')

    def __eq__(self, other):

       if self.interval is None:
           v = _to_abstract_value(other)
           return Series(Policy([[Unsatisfiable()]]), self.column, self.parent, shape=self.shape, interval=ClosedIntervalL(v, v))
       else:
           raise ValueError(f'Trying to re-compare a indicator Series whose interval is {self.interval}.')

    def __mul__(self, other):
        if isinstance(other, int):
            return Blackbox(self.policy)
        else:
            raise ValueError('Unsupported operator for multiplication with Series')

    def map(self, *args, **kwargs):
        return Blackbox(self.policy)

def _to_abstract_value(v):

       if isinstance(v, int):
           return ExtendV(IntegerV(v))
       elif isinstance(v, str):
           return ExtendV(StringV(v))
       else:
           raise ValueError(f'Unsupported value for comparison with Series: {v}.')

class DataFrame(Tabular):

    """ Stub class for Pandas DataFrame. """

    def __init__(self, schema=[], policy=Policy([[Satisfied()]]), data=None, **kwargs):
        if data is not None:
            if isinstance(data, (Tabular, Blackbox)):
                self.policy = data.policy
            else:
                raise NotImplementedError
        else:
            self.schema = schema
            self.policy = policy
            self.columns = self.schema
            self.values = ndarray(self.policy)
            self.shape = kwargs.get('shape')
            self.index = UniversalIndex()
            if self.shape is None:
                self.shape = [1, len(schema)]

            for colName in self.schema:
                setattr(self, colName, self[colName])

    def __getattr__(self, attr):
        if attr in self.schema:
            return self.__getitem__(attr)
        elif attr == 'iloc' or attr == 'loc':
            return self
        else:
            raise ValueError(f'Attribute {attr} does not exist.')

    def __getitem__(self, key):
        """
        Privacy effect of indexing for pandas DataFrame. Refer to
        https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
        for more information.
        """
        if isinstance(key, str):
            if key in self.schema:
                return Series(self.policy.runProject([key]), key, self, shape=[self.shape[1]])
            else:
                raise ValueError(f'Label {key} not found in the dataframe.')

        elif isinstance(key, list):
            if all([col in self.schema for col in key]):
                return DataFrame(key, self.policy.runProject(key), shape=self.shape)
            if all([isinstance(x, UniversalIndex) for x in key]):
                return self
            else:
                raise ValueError(f'Label {key} not found in the dataframe.') 

        elif isinstance(key, Series):           
            assert key.parent == self, 'Find series from another dataframe whose privacy effects are not supported.'
            newPolicy = self.policy
            if key.interval.lower != ExtendV('ninf'):
                newPolicy = newPolicy.runFilter(key.column, key.interval.lower.val.val, 'ge')
            if key.interval.upper != ExtendV('inf'):
                newPolicy = newPolicy.runFilter(key.column, key.interval.upper.val.val, 'le')
            return DataFrame(self.schema, newPolicy, shape=self.shape)

        elif isinstance(key, slice):
            return self

        elif isinstance(key, tuple):
            if len(key) == 2 and isinstance(key[0], slice) and isinstance(key[1], slice):
                return self
            elif len(key) == 2 and isinstance(key[0], (list, UniversalIndex)) and isinstance(key[1], (list, str)):
                return self
            else:
                raise NotImplementedError(f'Indexing by {key} is not supported now.')

        elif isinstance(key, UniversalIndex):
            return self

        else:
            raise NotImplementedError(f'Indexing by {key} is not supported now.')

    def __setitem__(self, key, newvalue):
        if isinstance(key, str):
            if key not in self.schema:
                self.schema.append(key)
                # TODO: assert newvalue is an instance of Tabular
                self.policy = self.policy.join(newvalue.policy)
            else:
                if isinstance(newvalue, Blackbox):
                    if newvalue.policy == Policy([[Satisfied()]]):
                        self.policy = self.policy.runProject([col for col in schema if col != key])
                    else:
                        self.policy = Policy([[Unsatisfiable()]])
        else:
            raise NotImplementedError('Pandas Dataframe __setitem__ only supports key of type string now.')

    def count(self):
        return BlackBox(self.policy.runPrivacy('aggregation'))

    def drop(self, labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors='raise'):
        """ 
        Privacy Effect:
            If the function is used to drop columns, the column should be removed from the schema and corresponding filters should be removed, too. If all the rows are within the SCHEMA attribute, remove the attribute.
        """
        if axis is 1 or axis is 'columns':
            if inplace:
                if isinstance(labels, list):
                    for label in labels:
                        if label in self.schema:
                            self.schema.remove(label)
                else:
                    if labels in self.schema:
                        self.schema.remove(labels)
                return self
            else:
                if isinstance(labels, list):
                    new_schema = [col for col in self.schema if col not in labels]
                    return DataFrame(new_schema, self.policy.runProject(new_schema))
                else:
                    new_schema = [col for col in self.schema if col != labels]
                    return DataFrame(new_schema, self.policy.runProject(new_schema))
        else:
            raise NotImplementedError

    def groupby(self, **kwargs):
        """ This function disables further operations to satisfy several privacy techniques such as aggregation. """
        return Blackbox(self.policy.unSat('privacy', priv_tech = 'Aggregation'))

    def merge(self, rhs, **kwargs):
        return merge(self, rhs, **kwargs)

    def fillna(self, *args, **kwargs):
        return self

    def sum(self, axis, *args, **kwargs):
        if axis == 0:
            newPolicy = self.policy.runPrivacy('Aggregation')
            return DataFrame(schema=self.schema, policy=newPolicy, shape=[len(self.schema), 1])
        elif axis == 1:
            return Blackbox(policy=self.policy)
        else:
            raise ValueError('Do not support sum along axes except 0 or 1.')

    def sort_values(self, *args, **kwargs):
        return self

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self

def merge(lhs, rhs, **kwargs):

    assert isinstance(lhs, DataFrame) and isinstance(rhs, DataFrame), 'Only support merging two dataframes.'
    # assert len(set(lhs.schema) & set(rhs.schema)) != 0, 'Duplicate column names in two dataframes to merge'
    return DataFrame(list(set(lhs.schema + rhs.schema)), lhs.policy.join(rhs.policy))
