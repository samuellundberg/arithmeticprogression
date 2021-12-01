import numpy as np
from numpy import random as rd
import itertools as it
from matplotlib import pyplot as plt


# select every possible point in a line without making an arithmetic progression
# this is the greedy selection, will not be great for bigger lines
def greedy(n):
    l = np.zeros((n, 1), dtype=int)
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
    l = np.zeros((n, 1), dtype=int)
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

# greedy but start in the ends
def side_greedy(n):
    l = np.zeros((n, 1), dtype=int)
    indexes = []
    for y in range(n):
        x = n - y - 1
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


# determines whether a set is free of arithmetic progressions
def is_ap_free(points):
    for p1 in points:
        for p2 in points:
            if p2 <= p1 or (p1 + p2) % 2 == 1:
                continue
            mid = p1/2 + p2/2

            if mid in points:
                return False

    return True


# Approximate r(n-a_l)
def get_rnal(x, l, S):
    rnal = 1e9
    if x in S:
        rnal = S.index(x) + 1
    elif x < l:
        for s in S:
            if x < s:
                rnal = S.index(s)
                break

    return rnal


# Hard coded values for r(n-a_l)
def get_rnal_real(n):
    # r(3n) <= 6 n, for every n > 16.
    if n < 2:
        return 1
    elif n < 4:
        return 2
    elif n < 5:
        return 3
    elif n < 9:
        return 4
    elif n < 11:
        return 5
    elif n < 13:
        return 6
    elif n < 14:
        return 7
    elif n < 20:
        return 8
    elif n < 24:
        return 9
    elif n < 26:
        return 10
    else:
        return 11


# storing approximations of r(n) where aprox(r(n)) <= r(n)
# This is done by storing the longest seen sequence within n
def update_rn(rn, S):
    length = len(S)
    n = S[-1]
    max_n = len(rn)

    for i in range(max_n - n + 1):
        if rn[max_n-i] < length:
            rn[max_n-i] = length
    return rn


# gets the current best estimate of rn for a given n
def get_rn(rn, n):
    return rn(n)


# Recursive greedy, backs down if set to small. fails if no set can be found
# Inspired by Janusz Dybizbanski's Sequences containing no 3-term arithmetic progressions, 2012
def rec_greedy(n, k):
    l = 2
    S = [1, 2]
    count = 0

    n2rn = {}
    for i in range(n):
        n2rn[i+1] = 0

    while len(S) > 1 and (len(S) < k or not is_ap_free(S)):
        count += 1
        if count == 10000:
            print('tapout')
            break

        if is_ap_free(S) and S[-1] < n:
            n2rn = update_rn(n2rn, S)
            S.append(S[-1] + 1)
            l += 1

        else:
            # testar att approx r(n-al) till sum(S[:n-al])
            # rnal = get_rnal(n - S[l - 1], l, S)

            rnal = get_rnal_real(n - S[l - 1])

            # om l är större än 1 och r(n-al) < k-l+1
            while (l > 1 and rnal < k - l + 1) or S[l-1] > n:
                l = l - 1

                #rnal = get_rnal(n - S[l - 1], l , S)
                rnal = get_rnal_real(n - S[l - 1])

            S = S[:l]
            S[-1] = S[-1] + 1

    if len(S) == k:
        print('done')
        print('rn_ests: ')
        print(n2rn)
        return S
    else:
        print('fail')
        return 0


l = rec_greedy(26, 11)

print(l)
