import numpy as np


# calculate barycentric coordinates
def barycentric_coords(tri_a: np.mat, tri_b: np.mat, tri_c: np.mat, point: np.mat) -> np.mat:
    AB = tri_b - tri_a
    AC = tri_c - tri_a
    BC = tri_c - tri_b
    AP = point - tri_a
    BP = point - tri_b
    # area of a triangle is proportional to area of a parallellogram formed from 2 of congruent triangles
    v = np.linalg.norm(np.cross(AB, AP))/np.linalg.norm(np.cross(AB, AC))
    u = np.linalg.norm(np.cross(AC, AP))/np.linalg.norm(np.cross(AB, AC))
    w = np.linalg.norm(np.cross(BC, BP))/np.linalg.norm(np.cross(AB, AC))

    return [u, v, w]


# driver code
if __name__ == '__main__':
    a = np.array([10, 20, 39])
    b = np.array([15, 12, 22])
    c = np.array([9, 15, 29])
    p = np.array([11, 13, 26])

    print(barycentric_coords(a, b, c, p))