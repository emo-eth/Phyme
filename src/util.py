'''General utils'''


def flatten(x):
    '''Generator of values from a 2d collection'''
    for y in x:
        yield from y
