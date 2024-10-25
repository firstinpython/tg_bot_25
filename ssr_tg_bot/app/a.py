import time

def time_n(func):
    def a(*args, **kwargs):
        start = time.time()

        res = func(*args, **kwargs)

        print(time.time() - start)
        print(res)
    return a

# def time_n(f):
#     a = time.time()
#     print(f)
#     f()
#
#     b = time.time()
#     res = b-a
#     print(res)
#

@time_n
def f(*a, **b):
    n = [i for i in range(1,10000)]
    print(f'{a=}, {b=}')

f(1, 2, 3, a=1, b=2, c=3,v=1)
