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

""" Attributes in PrivGuard. """

from typing import Tuple

class Column():
    """
    A representation of a column in a relation.
    """

    def __init__(self, col_name):
        self.col_name = col_name

    def __str__(self):
        return self.col_name

    def __eq__(self, other):
        return self.col_name == other.col_name

class Attribute(object):
    """
    The base class for all Attribute representations. All Attribute classes should
    inherit from this class.
    """

    def is_stricter_than(self, other):
        """
        The comparison operator for the partial order defined on the 
        attribute type (written "⊑" in the paper). Should return True 
        if the two attributes being compared are of the same type and
        the first ("self") is stricter than the second ("other"). As
        written in the paper, "self ⊑ other".

        Parameters
        ----------
        self : Attribute
            First attribute being compared

        other : Attribute
            Second attribute being compared

        Returns
        ----------
        True if self ⊑ other; False otherwise.

        """

        pass

    def cols(self):
        """
        The set of columns covered by this attribute.
        """

        return []

class Satisfied(Attribute):
    """
    An attribute which is already satisfied (i.e. nothing more needs to be 
    done to satisfy this policy requirement).
    """

    def __str__(self):
        return "SAT"

    __repr__ = __str__

    def is_stricter_than(self, other: Attribute):
        if isinstance(other, Satisfied):
            return True
        else:
            return False

class Unsatisfiable(Attribute):
    """
    An attribute which is not satisfiable (i.e. nothing can be done to satisfy
    this policy requirement).
    """

    def __str__(self):
        return "UNSAT"

    __repr__ = __str__

    def is_stricter_than(self, other: Attribute):
        if isinstance(other, Unsatisfiable):
            return True
        else:
            return False


# Filter and Redact deals with real data
class FilterAttribute(Attribute):
    """
    The Filter attribute. Uses the interval abstract domain to track filtering
    in the program.
    """

    def __init__(self, col, interval):
        self.col = col
        self.interval = interval

    def is_stricter_than(self, other: Attribute):
        if isinstance(other, FilterAttribute):
            if self.col == other.col:
                if self.interval.is_subset_of(other.interval):
                    return True
        return False

    def cols(self):
        return [self.col]

    def __str__(self):
        return "filter: " + self.col + " " + str(self.interval)

    def __repr__(self):
        return self.__str__()

class RedactAttribute(Attribute):
    """
    The Redact attribute. Tracks concrete column being redacted.
    """

    def __init__(self, col, slice_: Tuple[int] = (None, None)):
        self.col = col
        self.slice = slice_

    def is_stricter_than(self, other: Attribute):
        if isinstance(other, RedactAttribute):
            if self.col == other.col:
                if (self.slice[0] is None or self.slice[0] <= other.slice[0]) and (self.slice[1] is None or self.slice[1] >= other.slice[1]):
                    return True
        return False

    def cols(self):
        return [self.col]

    def __str__(self):
        return "redact: " + self.col + '(' + str(self.slice[0]) + ':' + str(self.slice[1]) + ')'

    def __repr__(self):
        return self.__str__()

# Schema deals with columns
class SchemaAttribute(Attribute):
    """
    The Schema attribute. Tracks concrete sets of columns remaining in the 
    projected relation.
    """

    def __init__(self, schema):
        self.schema = schema

    # TODO: re-write this
    def is_stricter_than(self, other: Attribute):
        if isinstance(other, SchemaAttribute):
            print(f'Warning: imprecise schema comparison: {self} vs {other}: {self.schema == other.schema}')
            if self.schema == other.schema:
                return True
            # if self.schema.is_subset_of(other.schema):
            #     return True
        return False

    def cols(self):
        return self.schema

    def __eq__(self, other):
        if isinstance(other, SchemaAttribute):
            return self.is_stricter_than(other) and other.is_stricter_than(self)
        else:
            return False

    def __str__(self):
        return 'schema: ' + str(self.schema)

    def __repr__(self):
        return self.__str__()

# The following attribute does not deal with data

class RoleAttribute(Attribute):
    """
    The Role attribute. Tracks concrete roles.
    """

    def __init__(self, role):
        self.role = role

    def is_stricter_than(self, other: Attribute):
        # TODO: how to do this?
        if isinstance(other, RoleAttribute):
            print(f'Warning: imprecise role comparison: {self} vs {other}: {self.role == other.role}')
            if self.role == other.role:
                return True
        return False

    def __eq__(self, other):
        if isinstance(other, RoleAttribute):
            return self.is_stricter_than(other) and other.is_stricter_than(self)
        else:
            return False

    def __str__(self):
        return 'role: ' + self.role

    def __repr__(self):
        return self.__str__()

class PrivacyAttribute(Attribute):
    """
    The Privacy attribute. 
    """

    def __init__(self, priv_tech, **kwargs):
        self.priv_tech = priv_tech
        self.kwargs = kwargs
        if priv_tech == 'k-anonymity':
            self.k = kwargs.get('k')
        elif priv_tech == 'l-diversity':
            self.l = kwargs.get('l')
        elif priv_tech == 't-closeness':
            self.t = kwargs.get('t')
        elif priv_tech == 'DP':
            self.eps = kwargs.get('eps')
            self.delta = kwargs.get('delta')
        elif not priv_tech in ['Anonymization', 'Aggregation']:
            raise ValueError('Invalid/Unsupported privacy technique.')

    def is_stricter_than(self, other: Attribute):
        if self.priv_tech == other.priv_tech:
            if self.priv_tech == 'k-anonymity':
                if self.k >= other.k:
                    return True
            elif self.priv_tech == 'l-diversity':
                raise NotImplemented
            elif self.priv_tech == 't-closenss':
                raise NotImplemented
            elif self.priv_tech == 'DP':
                if self.eps < other.eps and self.delta < other.delta:
                    return True
            else:
                return True
        return False

    def __str__(self):
        if self.priv_tech == 'k-anonymity':
            return f'privacy: {self.k}-anonymity'
        elif self.priv_tech == 'l-diversity':
            return f'privacy: {self.l}-diversity'
        elif self.priv_tech == 't-closeness':
            return f'privacy: {self.t}-closeness'
        elif self.priv_tech == 'DP':
            return f'privacy: DP ({self.eps}, {self.delta})'
        else:
            return 'privacy: ' + self.priv_tech

    def __repr__(self):
        return self.__str__()

class PurposeAttribute(Attribute):
    """
    The Purpose attribute (under construction).
    """

    def __init__(self, purpose):
        self.purpose = purpose

    def is_stricter_than(self, other: Attribute):
        # TODO: finish this
        pass

    def __str__(self):
        return 'purpose: ' + self.purpose

    def __repr__(self):
        return self.__str__()
