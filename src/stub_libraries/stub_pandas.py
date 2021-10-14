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
sys.path.append(os.environ.get('PRIVGUARD') + "/src/parser")

from blackbox import Blackbox
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
        print('Policy: ' + str(policy))
    with open(data_folder + 'meta.txt', 'r') as f:
        schema = f.readline().strip().replace('"', '').split(',')
        # print('Data Schema: ' + str(schema))

    if not schema and usecols == None:
        with open(data_folder + 'meta.txt', 'r') as f:
            schema = f.readline().strip().replace('"', '').split(',')
            # print('Data Schema: ' + str(schema))
        return DataFrame(schema, policy)
    elif schema:
        return DataFrame(schema, policy)
    elif usecols is not None:
        return DataFrame(usecols, file_policy)

class Series:

    """
    Stub class for Pandas Series. Series class is only expected to serve as indicators for 
    filtering. Only Series originating from a DataFrame can be used to filter that DataFrame. 
    """

    def __init__(self, policy, column, parent, interval=None):

        """
        Initialize an abstract Pandas Series. This class is only expected to serve as indicators
        for filtering. Indexing a DataFrame will return a Series object with interval=None. Calling
        methods of Series will return Series objects with interval being ClosedIntervalV object.
        """
        self.policy = policy
        self.column = column
        self.parent = parent
        self.interval = interval

        self.values = ndarray(self.policy)

    def __ge__(self, other):

       if self.interval is None:
           return Series(Policy([[Unsatisfiable()]]), self.column, self.parent, ClosedIntervalL(_to_abstract_value(other), ExtendV('inf')))
       else:
           raise ValueError(f'Trying to re-compare a indicator Series whose interval is {self.interval}.')

    def __le__(self, other):


       if self.interval is None:
           return Series(Policy([[Unsatisfiable()]]), self.column, self.parent, ClosedIntervalL(ExtendV('ninf'), _to_abstract_value(other)))
       else:
           raise ValueError(f'Trying to re-compare a indicator Series whose interval is {self.interval}.')

    def __eq__(self, other):

       if self.interval is None:
           v = _to_abstract_value(other)
           return Series(Policy([[Unsatisfiable()]]), self.column, self.parent, ClosedIntervalL(v, v))
       else:
           raise ValueError(f'Trying to re-compare a indicator Series whose interval is {self.interval}.')

    def __mul__(self, other):
        if isinstance(other, int):
            return Blackbox(self.policy)
        else:
            raise ValueError('Unsupported operator for multiplication with Series')

    # def append(self, other, **kwargs):
    #     if other.policy == Policy([[Satisfied()]]):
    #         return self
    #     else:
    #         return Blackbox(Policy([[Unsatisfiable()]]))

    # def map(self, *args, **kwargs):
    #         return Blackbox(Policy([[Unsatisfiable()]]))

def _to_abstract_value(v):

       if isinstance(v, int):
           return ExtendV(IntegerV(v))
       elif isinstance(v, str):
           return ExtendV(StringV(v))
       else:
           raise ValueError(f'Unsupported value for comparison with Series: {v}.')

class DataFrame:

    """ Stub class for Pandas DataFrame. """

    def __init__(self, schema=[], policy=Policy([[Satisfied()]]), **kwargs):
        self.schema = schema
        self.policy = policy

        for colName in self.schema:
            setattr(self, colName, self[colName])

        self.columns = self.schema
        self.values = ndarray(self.policy)

    def __getitem__(self, key):
        """
        Privacy effect of indexing for pandas DataFrame. Refer to
        https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
        for more information.
        """
        if isinstance(key, str):
            if key in self.schema:
                return Series(self.policy.runProject([key]), key, self)
            else:
                raise ValueError(f'Label {key} not found in the dataframe.')

        elif isinstance(key, list):
            if all([col in self.schema for col in key]):
                return DataFrame(key, self.policy.runProject(key))
            else:
                raise ValueError(f'Label {key} not found in the dataframe.') 

        elif isinstance(key, Series):           
            assert key.parent == self, 'Series from another dataframe whose privacy effects are not supported.'
            newPolicy = self.policy
            if key.interval.lower != ExtendV('ninf'):
                newPolicy = newPolicy.runFilter(key.column, key.interval.lower.val.val, 'ge')
            if key.interval.upper != ExtendV('inf'):
                newPolicy = newPolicy.runFilter(key.column, key.interval.upper.val.val, 'le')
            return DataFrame(self.schema, newPolicy)

        else:
            raise NotImplementedError

    def __setitem__(self, key, newvalue):
        if isinstance(newvalue, Blackbox):
             if newvalue.policy == Policy([[Satisfied()]]):
                 self.policy = self.policy.runProject([col for col in schema if col != key])
             else:
                 self.policy = Policy([[Unsatisfiable()]])

    def count(self):
        return BlackBox(self.policy.runPrivacy('aggregation'))

    # TODO: double check
    def drop(self, labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors='raise'):
        """ 
        Privacy Effect:
            If the function is used to drop columns, the column should be removed from the schema and corresponding filters should be removed, too.
        Original:
            Drop rows or columns in the dataframe.
        """
        if axis is 1 or axis is 'columns':
            if inplace:
                # !!! this part is super problematic
                if type(labels) is list:
                    for label in labels:
                        if label in self.schema:
                            self.schema.remove(label)
                else:
                    if labels in self.schema:
                        self.schema.remove(labels)
                return None
            new_schema = [col for col in self.schema if col not in labels]
            return DataFrame(new_schema, self.policy)
        else:
            if inplace:
                return None
            return self

    def groupby(self, **kwargs):
        """ This function disables further operations to satisfy several privacy techniques such as aggregation. """
        return Blackbox(self.policy.unSat('privacy', priv_tech = 'Aggregation'))

    def merge(self, rhs, **kwargs):
        return merge(self, rhs, **kwargs)

def merge(lhs, rhs, **kwargs):

    assert isinstance(lhs, DataFrame) and isinstance(rhs, DataFrame), 'Only support merging two dataframes.'
    # assert len(set(lhs.schema) & set(rhs.schema)) != 0, 'Duplicate column names in two dataframes to merge'
    return DataFrame(list(set(lhs.schema + rhs.schema)), lhs.policy.join(rhs.policy))
