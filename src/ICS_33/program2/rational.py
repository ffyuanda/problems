from goody import irange, type_as_str
import math


class Rational:

    def __init__(self, num=0, denom=1):

        if type(num) is not int:
            raise AssertionError("{}.{} num is not int: {}".format(self.__class__.__name__, self.__init__.__name__, num))
        if type(denom) is not int:
            raise AssertionError(
                "{}.{} denom is not int: {}".format(self.__class__.__name__, self.__init__.__name__, denom))
        if denom == 0:
            raise AssertionError("{}.{} denominator should not be 0".format(self.__class__.__name__, self.__init__.__name__))

        self.denom = abs(denom // Rational._gcd(abs(num), abs(denom)))
        self.num = num // Rational._gcd(abs(num), abs(denom)) if denom > 0 else -(num // Rational._gcd(abs(num), abs(denom)))

    @staticmethod
    # Called as Rational._gcd(...); no self parameter
    # Helper method computes the Greatest Common Divisor of x and y
    def _gcd(x : int, y : int) -> int:
        assert type(x) is int and type(y) is int and x >= 0 and y >= 0,\
          'Rational._gcd: x('+str(x)+') and y('+str(y)+') must be integers >= 0'
        while y != 0:
            x, y = y, x % y
        return x

    @staticmethod
    # Called as Rational._validate_arithmetic(..); no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), lt (left type) and rt (right type)
    # An example call (from my __add__ method), which checks whether the type of
    #   right is a Rational or int is...
    # Rational._validate_arithmetic(right, {Rational,int},'+','Rational',type_as_str(right))
    def _validate_arithmetic(v : object, t : {type}, op : str, left_type : str, right_type : str):
        if type(v) not in t:
            raise TypeError('unsupported operand type(s) for '+op+
                            ': \''+left_type+'\' and \''+right_type+'\'')

    @staticmethod
    # Called as Rational._validate_relational(..); no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), and rt (right type)
    def _validate_relational(v : object, t : {type}, op : str, right_type : str):
        if type(v) not in t:
            raise TypeError('unorderable types: '+
                            'Rational() '+op+' '+right_type+'()')

   # Put all other methods here

    def __repr__(self):
        return "Rational({},{})".format(self.num, self.denom)

    def __str__(self):
        return '{}/{}'.format(self.num, self.denom)

    def __neg__(self):
        return Rational(-self.num, self.denom)

    def __pos__(self):
        return Rational(self.num, self.denom)

    def __abs__(self):
        return Rational(abs(self.num), abs(self.denom))

    def __add__(self, other: "Rational" or int):
        Rational._validate_arithmetic(other, {Rational, int}, '+', 'Rational', type_as_str(other))
        if type(other) == int:
            other = Rational(other, 1)
        if self.denom == other.denom:
            return Rational(self.num + other.num, self.denom)
        else:
            return Rational(self.num * other.denom + self.denom * other.num, self.denom * other.denom)

    def __radd__(self, other: "Rational" or int):
        return self.__add__(other)

    def __sub__(self, other: "Rational" or int):
        Rational._validate_arithmetic(other, {Rational, int}, '-', 'Rational', type_as_str(other))
        return self.__add__(-other)

    def __rsub__(self, other: "Rational" or int):
        return -self.__sub__(other)

    def __mul__(self, other: "Rational" or int):
        Rational._validate_arithmetic(other, {Rational, int}, '*', 'Rational', type_as_str(other))
        if type(other) == int:
            result = Rational(self.num * other, self.denom)
        else:
            result = Rational(self.num * other.num, self.denom * other.denom)
        return result

    def __rmul__(self, other: "Rational" or int):
        return self.__mul__(other)

    def __truediv__(self, other: "Rational" or int):
        Rational._validate_arithmetic(other, {Rational, int}, '/', 'Rational', type_as_str(other))
        if type(other) == int:
            return self.__mul__(Rational(1, other))
        else:
            return self.__mul__(Rational(other.denom, other.num))

    def __rtruediv__(self, other: "Rational" or int):
        if type(other) == int:
            filp_result = self.__truediv__(other)
            result = Rational(filp_result.denom, filp_result.num)
            return result
        return self.__truediv__(other)

    def __pow__(self, power, modulo=None):
        if type(power) != int:
            raise TypeError('power is not int')
        num = int(self.num ** abs(power))
        denom = int(self.denom ** abs(power))
        if power >= 0:
            return Rational(num, denom)
        else:
            return Rational(denom, num)

    def __bool__(self):
        return False if self.num == 0 else True

    def __eq__(self, other: "Rational" or int):
        Rational._validate_relational(other, {Rational, int}, '==', type_as_str(other))

        if type(other) == int:
            r = Rational(other, 1)
        else:
            r = Rational(other.num, other.denom)
        return self.denom == r.denom and self.num == r.num

    def __lt__(self, other: "Rational" or int):
        Rational._validate_relational(other, {Rational, int}, '<', type_as_str(other))
        if type(other) == int:
            return True if self.num / self.denom < other else False
        else:
            return True if self.num / self.denom < other.num / other.denom else False

    def __gt__(self, other):
        Rational._validate_relational(other, {Rational, int}, '>', type_as_str(other))
        return not (self.__lt__(other) or self.__eq__(other))

    def __le__(self, other):
        Rational._validate_relational(other, {Rational, int}, '<=', type_as_str(other))
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        Rational._validate_relational(other, {Rational, int}, '>=', type_as_str(other))
        return self.__gt__(other) or self.__eq__(other)

    def __getitem__(self, item: int or str):

        if type(item) == str and item != "":

            item = item.lower()
            try:
                if 'numerator'.index(str(item)) == 0:
                    return self.num
            except ValueError:
                pass

            try:
                if 'denominator'.index(str(item)) == 0:
                    return self.denom
            except ValueError:
                pass

        elif type(item) == int:
            if item == 0:
                return self.num
            elif item == 1:
                return self.denom

        raise TypeError('index is illegal')

    def __call__(self, *args):
        digits = args[0]
        f_Rational = real_divide2(self.num, self.denom, digits)
        return f_Rational

    def __setattr__(self, key, value):
        # print(self.__dict__)
        if 'num' not in self.__dict__.keys() or 'denom' not in self.__dict__.keys():
            super().__setattr__(key, value)
        else:
            raise NameError("no attributes can be modified/added")


def real_divide2(dividend, divisor, digits=100):
    trunc_digit = digits + 1
    quo_str = '0'
    add_decimal = True
    while digits > 0:
        if dividend // divisor == 0 and dividend % divisor != 0:
            dividend *= 10
            if add_decimal:
                quo_str += '.'
                add_decimal = False
            quo_str += '0'
            continue

        quo, dividend = dividend // divisor, dividend % divisor
        quo_str = quo_str[:-1] + str(quo)
        if dividend == 0:
            break

        if add_decimal:
            quo_str += '.'
            add_decimal = False
        else:
            digits -= 1
    deci_index = quo_str.index('.')
    return quo_str[:deci_index] + quo_str[deci_index:deci_index + trunc_digit]


# e ~ 1/0! + 1/1! + 1/2! + 1/3! ... 1/n!
def compute_e(n):
    answer = Rational(1)
    for i in irange(1,n):
        answer += Rational(1,math.factorial(i))
    return answer

# Newton: pi = 6*arcsin(1/2); see the arcsin series at http://mathforum.org/library/drmath/view/54137.html
# Check your results at http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
#   also see http://www.numberworld.org/misc_runs/pi-5t/details.html
def compute_pi(n):
    def prod(r):
        answer = 1
        for i in r:
            answer *= i
        return answer

    answer = Rational(1,2)
    x      = Rational(1,2)
    for i in irange(1,n):
        big = 2*i+1
        answer += Rational(prod(range(1,big,2)),prod(range(2,big,2)))*x**big/big
    return 6*answer


if __name__ == '__main__':
    #Simple tests before running driver
    print()
    import driver
    driver.default_file_name = 'bscp22S21.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
