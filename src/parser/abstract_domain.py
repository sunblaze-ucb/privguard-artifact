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

""" Abstract domains for PrivGuard. """

from typed_value import ExtendV

class Lattice(object):
    """ Parent class for abstract lattices in PrivGuard policies. """

    def is_subset_of(self, other):
        pass

    def disjunct(self, other):
        pass

    def conjunct(self, other):
        pass

class ClosedIntervalL(Lattice):
    """ ClosedInterval lattice for extended values. """

    def __init__(self, lower, upper, lower_bound=None, upper_bound=None):
        assert isinstance(lower, ExtendV)
        assert isinstance(upper, ExtendV)

        self.lower = lower
        self.upper = upper
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def is_subset_of(self, other: Lattice):
        assert isinstance(other, ClosedIntervalL)

        if self.lower >= other.lower and self.upper <= other.upper:
             return True
        return False 

    def disjunct(self, other: Lattice):
        return ClosedInterval(lower=min_exval(self.lower, other.lower), upper=max_exval(self.upper, other.upper), lower_bound=self.lower_bound, upper_bound=self.upper_bound)

    def conjunct(self, other: Lattice):
        return ClosedInterval(lower=max_exval(self.lower, other.lower), upper=min_exval(self.upper, other.upper), lower_bound=self.lower_bound, upper_bound=self.upper_bound)

    def __str__(self):
        return '[' + str(self.lower) + ', ' + str(self.upper) + ']'

    def __repr__(self):
        return self.__str__()

class SchemaL(Lattice):
    """ Schema lattice. """

    def __init__(self, schema, full_schema=None):
        self.schema = schema
        self.full_schema = full_schema

    def is_subset_of(self, other: Lattice):
        return set(self.schema).issubset(set(other.schema))

    def disjunct(self, other: Lattice):
        return [x for x in self.schema if x in other.schema]

    def conjunct(self, other: Lattice):
        return list(set(self.schema)|set(other.schema))

    def __str__(self):
        string = '[' + self.schema[0] 
        for i in range(1, len(self.schema)):
            string += ", " + self.schema[i]
        return string

    def __repr__(self):
        return self.__str__()
