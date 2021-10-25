import numpy as np
from matplotlib import pyplot as plt
import time as time


# Build a matrix that contains the hexagon grid
def build_matrix(size):
    height = 2 * size - 1
    width = 4 * size - 3
    matrix = np.zeros((height, width), dtype=int)
    set = []
    for h in range(height):
        for w in range(width):
            if size % 2 == (w-h) % 2:
                continue
            if h < size - 1 - w:
                continue
            if h > size - 1 + w:
                continue
            if h < w + (size - width - 1):
                continue
            if h > (size + width - 1) - w:
                continue
            matrix[h, w] = 1
            pair = (h, w)
            set.append(pair)

    return matrix, set


# Greedy algo, selects a grid if possible, looking from left and onwards
def greedy(set, m_shape):
    grid = np.zeros(m_shape, dtype=int)
    selected = []

    for p in set:
        select = True
        for p0 in selected:
            p_0 = p[0]
            p_1 = p[1]
            p0_0 = p0[0]
            p0_1 = p0[1]
            dist_x = p_0 - p0_0
            dist_y = p_1 - p0_1
            if (p_0 + dist_x, p_1 + dist_y) in selected:
                select = False
                break
            elif (p_0 + dist_x, p0_1 - dist_y) in selected:
                select = False
                break
            elif (p0_0 - dist_x, p_1 + dist_y) in selected:
                select = False
                break
            elif (p0_0 - dist_x, p0_1 - dist_y) in selected:
                select = False
                break
        if select:
            grid[p[0], p[1]] = 1
            selected.append(p)

    return grid, selected


# Greedy algo, selects a grid if possible, but looking starting from the middle of the set
# Does not work very well
def in_greedy(set, m_shape):
    grid = np.zeros(m_shape, dtype=int)
    selected = []

    l = len(set)
    for x in range(l):
        select = True

        if x % 2:
            i = int(l / 2) - 1 - int(x / 2)
        else:
            i = int(l / 2) + int(x / 2)

        p = set[i]
        for p0 in selected:
            p_0 = p[0]
            p_1 = p[1]
            p0_0 = p0[0]
            p0_1 = p0[1]
            dist_x = p_0 - p0_0
            dist_y = p_1 - p0_1
            if (p_0 + dist_x, p_1 + dist_y) in selected:
                select = False
                break
            elif (p_0 + dist_x, p0_1 - dist_y) in selected:
                select = False
                break
            elif (p0_0 - dist_x, p_1 + dist_y) in selected:
                select = False
                break
            elif (p0_0 - dist_x, p0_1 - dist_y) in selected:
                select = False
                break
        if select:
            grid[p[0], p[1]] = 1
            selected.append(p)

    return grid, selected


# Greedy algo, selects a grid if possible, but looking from the outsides of the set and working inwards
# Better than greedy for most sizes
# The problem is that it starts bottom right and top left. It does not know of the grids geometry
def out_greedy(set, m_shape):
    grid = np.zeros(m_shape, dtype=int)
    selected = []

    l = len(set)
    for y in range(l):
        select = True

        x = l - y - 1
        if x % 2:
            i = int(l / 2) - 1 - int(x / 2)
        else:
            i = int(l / 2) + int(x / 2)

        p = set[i]
        for p0 in selected:
            p_0 = p[0]
            p_1 = p[1]
            p0_0 = p0[0]
            p0_1 = p0[1]
            dist_x = p_0 - p0_0
            dist_y = p_1 - p0_1
            if (p_0 + dist_x, p_1 + dist_y) in selected:
                select = False
                break
            elif (p_0 + dist_x, p0_1 - dist_y) in selected:
                select = False
                break
            elif (p0_0 - dist_x, p_1 + dist_y) in selected:
                select = False
                break
            elif (p0_0 - dist_x, p0_1 - dist_y) in selected:
                select = False
                break
        if select:
            grid[p[0], p[1]] = 1
            selected.append(p)

    return grid, selected


# count the selected cells
def counter(sets):
    return len(sets)


# Takes a list of strings and concatenates them to one string, each element separated by ', '
def to_string(list_of_strings):
    concat_string = ''
    for l in list_of_strings:
        concat_string += l + ', '
    return concat_string


# Stores a result file at path. First line is score. Second line is the result string.
# If there is already a file at path it will be overwritten.
# param path: string for where to store results. "results/X.txt" where X is the size of the Graph
# param result_string: string representing the solution
# param score: int representing the number of selected cells in the grid
def my_write(path, result_string, score):
    content = str(score) + '\n' + to_string(result_string)
    file = open(path, "w")
    file.write(content)
    file.close()


# If the given score is lower than the recorded score for the given size the
# result_string is saved to file named 'size'.txt in the results folder
# runs my_write internally
def store_results(size, result_string, score):
    path = "results/" + str(size) + ".txt"

    try:
        file = open(path, "r")
        content = file.readlines()
        file.close()

        if len(content) == 2:
            ref = int(content[0])
            if score > ref:
                print('found new best score of: ', score, ' for size: ', size)
                my_write(path, result_string, score)
            else:
                print('found', score, 'cells, did not beat old solution of:', ref, 'for size:', size)
        else:
            print('Weird file at path: ', path)
    except IOError:
        print('did not find file at path: ', path, '. Creating a new one')
        my_write(path, result_string, score)


def formatter(cells, n, mat):
    # print('cells: ', cells)

    n_cells = []
    for c in cells:
        idx = sum(mat[c[0], :c[1]])
        n_cells.append((c[0], idx))

    # print('new_cells: ', n_cells)

    d = {}
    for c in n_cells:
        if c[0] in d:
            d[c[0]].append(c[1])
        else:
            d[c[0]] = [c[1]]
    # print('d: ', d)

    l = []
    for i in range(2 * n - 1):
        s = '{'
        if i in d:
            s = s + str(d[i])[1:-1]
        s = s + '}'
        l.append(s)

    print('l: ', l)
    return l


def main(n, algo):
    m, s = build_matrix(n)

    m_shape = m.shape

    if algo == 'greedy':
        grid, cells = greedy(s, m_shape)
    elif algo == 'in_greedy':
        grid, cells = in_greedy(s, m_shape)
    elif algo == 'out_greedy':
        grid, cells = out_greedy(s, m_shape)
    else:
        print(algo, 'is not an available algorithm, exiting.')
        exit()

    # plt.imshow(m+grid)
    # plt.show()

    score = counter(cells)
    formatted_cells = formatter(cells, num, m)

    return formatted_cells, score


N = [11]
# N = [2, 6, 11, 18, 27, 38]
# N = [2, 6, 11, 18, 27, 38, 50, 65, 81, 98, 118, 139, 162, 187, 214, 242, 273, 305, 338, 374, 411, 450, 491, 534, 578]
algo = 'out_greedy'

t0 = time.time()
for num in N:
    r, s = main(num, algo)

    store_results(num, r, s)

print('elapsed time = ', time.time() - t0)
