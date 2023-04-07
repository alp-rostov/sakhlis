import math

def decor(d):
    def wrapper(*args,**kwargs):
        print ('факториал числа', args[0])
        print(d(*args,**kwargs))
    return wrapper


@decor
def w(s=5):
    return math.factorial(s)


w(30)

