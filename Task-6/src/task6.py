import sys
import numpy as np


# get (vertices, uv, faces) from .obj file
def get_vertices_uv_faces(obj_path: str) -> tuple:
    # get vertices
    vertices = {}
    uv = {}
    faces = {}
    i, j , k = 0, 0, 0
    try:
        # read .obj file to get vertices, uv and faces
        with open(obj_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line[0] == 'v' and line[1] != 't':
                    x, y, z = list(map(float, line[1: len(line) - 1].split()))
                    vertices[i] = (x, y, z)
                    i = i + 1

                elif line[:2] == 'vt':
                    u, v = list(map(float, line[2:].split()))
                    uv[j] = (u, v)
                    j = j + 1

                elif line[0] == 'f':
                    x, y, z = line[2:].split()
                    x = int(x[: len(x)//2]) - 1
                    y = int(y[: len(y)//2]) - 1
                    z = int(z[: len(z)//2]) - 1
                    faces[k] = (x, y, z)
                    k = k + 1
    except(FileNotFoundError):
        print('file not found')

    return (vertices, uv, faces)


# find the difference between 2 .obj files and return vertices, uv and faces
def find_diff(obj1: tuple, obj2: tuple) -> tuple:
    vertices = [i for i in obj1[0].values() if i not in obj2[0].values()]
    uv = [i for i in obj1[1].values() if i not in obj2[1].values()]
    faces = [i for i in obj1[2].values() if i not in obj2[2].values()]
    
    return (vertices, uv, faces)


# write .obj file to export_obj_path using the given obj_data containing vertices, uv and faces
def write_obj(export_obj_path: str, obj_data: tuple) -> None:

    with open(export_obj_path, 'w') as export:
        # writing vertices
        export_obj_path.write('o face\nmtllib face.mtl\n\n# Vertices\n')
        for vertex in obj_data[0]:
            x, y, z = vertex
            export_obj_path.writelines('v ' + str(x) + ' ' + str(y) + ' ' + str(z) + '\n')

        # writing uv
        export_obj_path.write('\n\n#UV\n')
        for uv in obj_data[1]:
            export_obj_path.writelines('vt ' + str(uv[0]) + ' ' + str(uv[1]) + '\n')\

        # writing faces
        for face in obj_data[2]:
            x, y, z = face
            export_obj_path.writelines('f ' + str(x)+'/'+str(x) + ' ' +  str(y)+'/'+str(y) + ' '  +  str(z)+'/'+str(z)+ '\n')


# map points in face.obj (from mediapipe) to head.obj
def map_vertex_to_vertex(FACE: np.array, HEAD: np.array) -> list:
    visited = set()
    mapped_vertices = []

    for i in FACE:
        min_dist = 100000000
        closest_vertex = ()
        
        for j in HEAD:
            temp = (j[0], j[1], j[2])
            if temp in visited:
                continue
            print(i , j)
            dist = ((i[0] - j[0])**2 + (i[1] - j[1])**2 + (i[2] - j[2])**2)**0.5
            if dist < min_dist:
                closest_vertex = j
                min_dist = dist
        mapped_vertices.append(i, closest_vertex)
        temp = (closest_vertex[0], closest_vertex[1], closest_vertex[2])
        visited.add(closest_vertex)
    
    return mapped_vertices


# given vertices of triangle return its area
def area_of_triangle(a: tuple, b: tuple, c: tuple) -> float:
    return abs(a[0]*(b[2] - c[2]) + b[0]*(c[2] - a[2]) + c[0]*(a[2] - b[2]))/2.0


# utility function to find if a point lies inside a triangle formed by 3 other points
def inside_triangle(p: tuple, triangle: tuple) -> bool:
    p1, p2, p3 = triangle[0], triangle[1], triangle[2]
    area = area_of_triangle(p1, p2, p3)
    area1 = area_of_triangle(p, p2, p3)
    area2 = area_of_triangle(p1, p, p3)
    area3 = area_of_triangle(p1, p2, p)

    return area == area1 + area2 + area3


# find vertices in head.obj for each face in face.obj
def move_vertex(mp_faces: np.mat, mp_vertices: np.mat, obj_vertices: set) -> None:
    res_obj_vertices = np.zeros((len(obj_vertices, 3)))
    for vertex_indices in mp_faces:
        for vertex in obj_vertices:
            if inside_triangle(vertex, mp_vertices[vertex_indices[0]], mp_vertices[vertex_indices[1]], mp_vertices[vertex_indices[2]]):
                x, y, z = vertex
                point = mp_vertices[vertex_indices[0]]
                plane = np.cross(mp_vertices[vertex_indices[1]] - point,
                                mp_vertices[vertex_indices[2]] - point)
                y  = (plane[0]*(point[0] - x) + plane[1]*point[1] + plane[2]*(point[2] - z))/plane[1]

                res_obj_vertices[] = x, y, z
                obj_vertices.remove(vertex)

    return res_obj_vertices
        
    
    



# driver code
if __name__ == '__main__':

    face_path, head_path = sys.argv[1], sys.argv[2]
