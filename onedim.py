import numpy as np
from numpy import random as rd
import itertools as it


# select every possible point in a line without making an arithmetic progression
# this is the greedy selection, will not be great for bigger lines
def greedy(n):
    l = np.zeros(n, dtype=int)
    indexes = []

    for p in range(n):
        select = True
        for p0 in indexes:
            dist = p - p0
            if p + dist in indexes or p0 - dist in indexes:
                select = False
                continue
        if select:
            l[p] = 1
            indexes.append(p)

    return l


# greedy but start in middle
def mid_greedy(n):
    l = np.zeros(n, dtype=int)
    indexes = []
    for x in range(n):
        if x % 2:
            p = int(n/2) - 1 - int(x/2)
        else:
            p = int(n/2) + int(x/2)
        select = True
        for p0 in indexes:
            dist = p - p0
            if p + dist in indexes or p0 - dist in indexes:
                select = False
                continue

        if select:
            l[p] = 1
            indexes.append(p)
    return l


# Does like greedy but only selects the point 50% of the times
# and gradualy increases the probability of the point being found
def often_greedy(n):
    l = np.zeros(n, dtype=int)
    indexes = []
    blocked = []

    for p in range(n):
        select = True
        for p0 in indexes:
            dist = p - p0
            if p + dist in indexes or p0 - dist in indexes:
                select = False
                continue
        if select and 0.5 * (1 - p/n) < rd.rand(1):
            l[p] = 1
            indexes.append(p)
        elif select:
            blocked.append(p)

    return l, blocked


# select every possible point in a line without making an arithmetic progression
# but consider the points in an random order
# now we must look on the sides, not just in the middle
def perm_greedy(n):
    l = np.zeros(n, dtype=int)
    perm = rd.permutation(n)
    indexes = []
    for p in perm:
        select = True
        for p0 in indexes:
            dist = p - p0
            if p + dist in indexes or p0 - dist in indexes:
                select = False
                continue

        if select:
            l[p] = 1
            indexes.append(p)

    return l


# Should count selected cells and validate that a line is free of arithmetic progressions
# returns -1 if ap, else number of cells
def counter(l):
    indexes = []
    for idx, val in enumerate(l):
        if val:
            indexes.append(idx)
    for x, i in enumerate(indexes):
        for j in indexes[:x]:
            middle = int((i + j) / 2)
            if middle in indexes and (i + j) % 2 == 0:
                print('found the arithmetic progression: ', j, middle, i)
                return -1

    return len(indexes)


num = 27
# N = [2, 6, 11]
# N = [2, 6, 11, 18, 27, 38, 50, 65, 81, 98, 118, 139, 162, 187, 214, 242, 273, 305, 338, 374, 411, 450, 491, 534, 578]

# algo = 'perfect16'

line = greedy(num)
line2 = mid_greedy(num)
line3, r = often_greedy(num)
line4 = perm_greedy(num)

print('greedy = ', counter(line))
print('perm_greedy = ', counter(line4))
print('often_greedy = ', counter(line3))
print('mid_greedy = ', counter(line2))

