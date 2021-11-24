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

""" Data types supported in the collected data. """

import datetime

def min_exval(v1, v2):
    """ Return the smaller one between two extended values."""
    if v1 <= v2:
        return v1
    return v2

def max_exval(v1, v2):
    """ Return the larger one between two extended values. """
    if v1 >= v2:
        return v2
    return v1

class Val(object):

    """ Parent class for values in PrivGuard policies. """

    def __init__(self, val):
        # print(f'Warning: making a Val({val})')
        self.val = val

    def __lt__(self, other):
        if isinstance(other, Val):
            return (self.val < other.val)
        else:
            return (self.val < other)

    def __le__(self, other):
        if isinstance(other, Val):
            return (self.val <= other.val)
        else:
            return (self.val <= other)

    def __eq__(self, other):
        if isinstance(other, Val):
            return (self.val == other.val)
        else:
            return (self.val == other)

    def __ne__(self, other):
        if isinstance(other, Val):
            return (self.val != other.val)
        else:
            return (self.val != other)

    def __ge__(self, other):
        if isinstance(other, Val):
            return (self.val >= other.val)
        else:
            return (self.val >= other)


    def __gt__(self, other):
        if isinstance(other, Val):
            return (self.val > other.val)
        else:
            return (self.val > other)

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return self.__str__()

class IntegerV(Val):

    """ Integer values in PrivGuard policies. """

    def __init__(self, val):
        Val.__init__(self, val)

    def __add__(self, other):
        return IntegerV(self.val + other)

    def __sub__(self, other):
        return IntegerV(self.val - other)

class StringV(Val):

    """ String values in PrivGuard policies. """

    def __init__(self, val):
        Val.__init__(self, val)

class DateV(Val):

    """ Date values in PrivGuard policies. """

    def __init__(self, val: datetime.datetime):
        Val.__init__(self, val)

class ExtendV(object):

    """
    Extend any value with upper bound: inf and lower bound: ninf
    """

    def __init__(self, val):
        if isinstance(val, ExtendV):
            raise RuntimeError(f'Tried to double-extend the value {val}')
        self.val = val

    def __str__(self):
        return "e" + str(self.val)

    def __lt__(self, other):
        if (other.val is 'inf') and (self.val is 'inf'):
            return False
        elif (other.val is 'inf') and (self.val is not 'inf'):
            return True
        elif (other.val is 'ninf'):
            return False
        elif (self.val is 'ninf'):
            return True
        elif (self.val is 'inf'):
            return False
        return (self.val < other.val)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other):
        if (other.val is 'inf') and (self.val is 'inf'):
            return True
        elif (other.val is 'inf') and (self.val is not 'inf'):
            return False
        elif (other.val is 'ninf') and (self.val is 'ninf'):
            return True
        elif (other.val is 'ninf') and (self.val is not 'ninf'):
            return False
        return (self.val == other.val)

    def __ne__(self, other):
        return not (self.__eq__(other))

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other):
        if (other.val is 'inf'):
            return False
        elif (self.val is 'inf'):
            return True
        elif (self.val is 'ninf'):
            return False
        elif (other.val is 'ninf') and (self.val is not 'ninf'):
            return True
        elif (other.val is 'ninf') and (self.val is 'ninf'):
            return False
        return (self.val > other.val)
