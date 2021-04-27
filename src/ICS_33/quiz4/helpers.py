from predicate import is_prime
import prompt
import traceback

# primes is used to test code you write below
def primes(max=None):
    p = 2
    while max == None or p <= max:
        if is_prime(p):
            yield p
        p += 1
         
# Generators must be able to iterate through any iterable.
# hide is present and called to ensure that your generator code works on
#   general iterable parameters (not just a string, list, etc.)
# For example, although we can call len(string) we cannot call
#   len(hide(string)), so the generator functions you write should not
#   call len on their parameters
# Leave hide in this file and add code for the other generators.

def hide(iterable):
    for v in iterable:
        yield v


# A function to return the nth yielded value in iterable (1sth, 2nd, ..etc)
# returns None if the iterable doesn't have n values
# Interesting when iterable is infinite
def nth(iterable, n):
    for i,v in enumerate(iterable,1):
        if i == n:
            return v
    return None