#nconstrain

Make tiny wrappers around existing numerical types to modify their behavior.

Definition example:

    def between(val, mi, ma):
        return SpecialNum(val,
                lambda x: min(max(x, mi), ma),
                lambda self: '<{} between {}, {}>'.format(self.val, mi, ma))
                
between example:

    >>> x = nconstrain.between(6, 0, 10000)
    >>> x
    <6 between 0, 10000>
    >>> x * 2
    <12 between 0, 10000>
    >>> x * 2.5
    <15.0 between 0, 10000>
    >>> x *= 999999999
    >>> x
    <10000 between 0, 10000>
    >>> x -= 1
    >>> x
    <9999 between 0, 10000>
    
modulo_n example:

    >>> x = nconstrain.modulo_n(4, 12)
    >>> x += 11
    >>> x
    <3 modulo 12>

in_set example:

    >>> x = nconstrain.in_set(3, [3, 4, 5, 6, 10])
    >>> x
    <3 in set {10, 3, 4, 5, 6}>
    >>> x += 1
    >>> x
    <4 in set {10, 3, 4, 5, 6}>
    >>> x += 3
    Traceback (most recent call last):
         ...
        raise ValueError("{} must be inside {}".format(x, s))
    ValueError: 7 must be inside {10, 3, 4, 5, 6}

## Thoughts

- Has the advantage of working for any number-like object
- Still some operator issues to work out
- A similar system could be useful for asserting invariants on arbitrary objects
