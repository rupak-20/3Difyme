import numpy as np


# calculate barycentric coordinates
def barycentric_coords(a: np.mat, b: np.mat, c: np.mat, d: np.mat, p: np.mat) -> np.mat:
    pbcd = np.linalg.det(np.array([[p[0], b[0], c[0], d[0]],
                                   [p[1], b[1], c[1], d[1]],
                                   [p[2], b[2], c[2], d[2]],
                                   [1, 1, 1, 1]]))
    apcd = np.linalg.det(np.array([[a[0], p[0], c[0], d[0]],
                                   [a[1], p[1], c[1], d[1]],
                                   [a[2], p[2], c[2], d[2]],
                                   [1, 1, 1, 1]]))
    abpd = np.linalg.det(np.array([[a[0], b[0], p[0], d[0]],
                                   [a[1], b[1], p[1], d[1]],
                                   [a[2], b[2], p[2], d[2]],
                                   [1, 1, 1, 1]]))
    abcd = np.linalg.det(np.array([[a[0], b[0], c[0], d[0]],
                                   [a[1], b[1], c[1], d[1]],
                                   [a[2], b[2], c[2], d[2]],
                                   [1, 1, 1, 1]]))

    u = pbcd/abcd
    v = apcd/abcd
    w = abpd/abcd
    x = 1-u-v-w

    return [u, v, w, x]


# driver code
if __name__ == '__main__':
    a = np.array([0, 0, 0])
    b = np.array([10, 0, 0])
    c = np.array([0, 10, 0])
    d = np.array([5, 5, 10])
    p = np.array([15, 0, 0])

    print(barycentric_coords(a, b, c, d, p))