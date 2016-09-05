"""
This module contains some abstractions of numerical objects.
"""


def reflect(name):
    return '__r{}'.format(name.lstrip('__'))

def unreflect(name):
    return '__{}'.format(name.lstrip('__r'))

binary_ops = ['__add__', '__sub__', '__mul__', '__matmul__', '__truediv__',
        '__floordiv__', '__mod__', '__divmod__', '__pow__', '__lshift__',
        '__rshift__', '__and__', '__xor__', '__or__']
reflected_ops = [reflect(n) for n in binary_ops]
unary_ops = ['__neg__', '__pos__', '__abs__', '__invert__']


class SpecialNum(object):
    """
    A numerical object that wraps an inner number and applies a function
    to it after each operation.
    """

    def __init__(self, val, post_op, reprfunc):
        """
        Create an instance of `SpecialNum`.

        val: the inner number to use
        post_op: the function to apply to the number after each operation
        reprfunc: the __repr__ function to use
        """

        self.post_op = post_op
        self.val = self.post_op(val)
        self.reprfunc = reprfunc

        for name in binary_ops + reflected_ops:
            def implement(name):
                def implementation(self, other):
                    try:
                        other = other.val
                    except AttributeError:
                        pass

                    retval = getattr(self.val, name)(other)
                    if retval is NotImplemented:
                        if name in binary_ops:
                            retval = getattr(other, reflect(name))(self.val)
                        else:
                            retval = getattr(other, unreflect(name))(self.val)

                    return SpecialNum(retval, post_op, reprfunc)
                return implementation

            setattr(self.__class__, name, implement(name))

        for name in unary_ops:
            def implement(name):
                def implementation(self):
                    retval = getattr(self.val, name)()
                    return SpecialNum(self.post_op(retval), post_op, reprfunc)
                return implementation

            setattr(self.__class__, name, implement(name))


    def __index__(self):
        if hasattr(self.val, '__index__'):
            return self.val.__index__()
        else:
            raise NotImplemented


    def _val(self, other):
        """
        A helper function that deals with the fact that `other` may be either a
        `SpecialNum` or a primitive.
        """
        try:
            other = other.val
        except:
            pass
        return other


    def __lt__(self, other):
        return self.val < self._val(other)


    def __le__(self, other):
        return self.val < self._val(other)


    def __eq__(self, other):
        return self.val == self._val(other)


    def __ne__(self, other):
        return self.val != self._val(other)


    def __gt__(self, other):
        return self.val > self._val(other)


    def __ge__(self, other):
        return self.val >= self._val(other)


    def __hash__(self):
        return self.val.__hash__()


    def __repr__(self):
        return self.reprfunc(self)


    def assign(self, val):
        """Reassign the inner value"""
        self.val = self.post_op(val)



def above(val, minimum):
    return SpecialNum(val,
            lambda x: max(x, minimum),
            lambda self: '<{} at least {}>'.format(self.val, minimum))


def below(val, maximum):
    return SpecialNum(val,
            lambda x: min(x, maximum),
            lambda self: '<{} at most {}>'.format(self.val, maximum))


def between(val, mi, ma):
    return SpecialNum(val,
            lambda x: min(max(x, mi), ma),
            lambda self: '<{} between {}, {}>'.format(self.val, mi, ma))


def modulo_n(val, n):
    return SpecialNum(val,
            lambda x: x % n,
            lambda self: '<{} modulo {}>'.format(self.val, n))


def rounded(val, ndigits):
    return SpecialNum(val,
            lambda x: round(x, ndigits),
            lambda self: '<{} rounded to {} digits>'.format(self.val, ndigits))


def in_set(val, s):
    s = set(s)
    def check(x):
        if not x in s:
            raise ValueError("{} must be inside {}".format(x, s))
        return x
    return SpecialNum(val,
            check,
            lambda self: '<{} in set {}>'.format(self.val, s))
