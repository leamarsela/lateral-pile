import timeit

setup = 'from math import sqrt'

code = '''
def squaring():
    mylist = []
    for x in range(50):
        mylist.append(sqrt(x))'''

print(timeit.timeit(stmt=code, setup=setup, number=100000000))





