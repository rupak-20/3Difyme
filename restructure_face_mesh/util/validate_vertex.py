import numpy as np


def validate_vertex_vector(ver: np.mat, a: np.mat, b: np.mat, c: np.mat) -> bool:
    unit_ver_a = (a - ver) / np.linalg.norm(a - ver)
    unit_ver_b = (b - ver) / np.linalg.norm(b - ver)
    unit_ver_c = (c - ver) / np.linalg.norm(c - ver)

    resultant_mag = np.linalg.norm(unit_ver_a + unit_ver_b + unit_ver_c)
    if resultant_mag > 1:
        return False

    return True


def validate_vertex_barycentric_2d(ver: np.mat, a: np.mat, b: np.mat, c: np.mat) -> bool:
    ver, a, b, c = ver[:2], a[:2], b[:2], c[:2]
    AB = b - a
    AC = c - a
    BC = c - b
    AP = ver - a
    BP = ver - b
    # area of a triangle is proportional to area of a parallellogram formed from 2 of congruent triangles
    v = np.linalg.norm(np.cross(AB, AP))/np.linalg.norm(np.cross(AB, AC))
    u = np.linalg.norm(np.cross(AC, AP))/np.linalg.norm(np.cross(AB, AC))
    w = np.linalg.norm(np.cross(BC, BP))/np.linalg.norm(np.cross(AB, AC))

    if u>1 or v>1 or w>1:
        return False
    
    return True


def get_vertices(obj_path: str) -> np.mat:
    vertices = []

    with open(obj_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line[:2] == 'v ':
                x, y, z = list(map(float, line[2:].strip().split(' ')))
                vertices.append([x, y, z])
    
    return np.asarray(vertices)


def outside_triangle(ignore: set, vertices: np.mat, mapping_path: str) -> np.mat:
    outside_triangle = []
    try:
        with open(mapping_path, 'r') as mapping:
            lines = mapping.readlines()
            for line in lines:
                unmapped_vertex, a, b, c = list(map(int, line.strip().split(' ')))
                if unmapped_vertex in ignore:
                    continue
                # unmapped_vertex, a, b, c = vertices[unmapped_vertex], vertices[a], vertices[b], vertices[c]
                if validate_vertex_vector(vertices[unmapped_vertex], vertices[a], vertices[b], vertices[c]) == False:
                    outside_triangle.append([unmapped_vertex, a, b, c])

    except FileNotFoundError:
        print('file not found')
    
    return np.asarray(outside_triangle)


def write_vertices(vertices: list, indices: list, export_path: str) -> None:
    with open(export_path, 'w') as file:
        lines = ''
        for i in indices:
            line = 'v ' + str(vertices[i][0]) + ' ' + str(vertices[i][1]) + ' ' + str(vertices[i][2]) + '\n'
            lines += line
        file.writelines(lines)

    
def ignore_vertices(file_path: str) -> set:
    ignore = set()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            for x in line.strip().split(' '):
                ignore.add(int(x))
    
    return ignore


if __name__ == '__main__':
    obj = '/home/rupak/Documents/Study/Placement/Internship/PixelHash/Task-6/obj/face.obj'
    mapping = '/home/rupak/Documents/Study/Placement/Internship/PixelHash/Task-6/txt/skimmed_main_mapping.txt'
    export = '/home/rupak/Documents/Study/Placement/Internship/PixelHash/Task-6/obj/vertices.obj'
    ignore_path = '/home/rupak/Documents/Study/Placement/Internship/PixelHash/Task-6/txt/ignore_vertices.txt'
    ignore = ignore_vertices(ignore_path)
    vertices = get_vertices(obj)
    outside = outside_triangle(ignore, vertices, mapping)
    
    print(outside)
    print(outside.shape)

    indices = [i[0] for i in outside]
    write_vertices(vertices, indices, export)