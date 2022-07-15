import sys
import numpy as np
import bpy
from mathutils import Matrix, Vector

# get (vertices, uv, faces) from .obj file
def get_vertices_uv_vn_faces(obj_path: str) -> tuple:
    # get vertices
    vertices = []
    uv = []
    vn = []
    faces = []

    try:
        # read .obj file to get vertices, uv and faces
        with open(obj_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line[: 2] == 'v ':
                    x, y, z = list(map(float, line[1: len(line) - 1].split()))
                    vertices.append((x, y, z))

                elif line[: 2] == 'vt':
                    u, v = list(map(float, line[2:].split()))
                    uv.append((u, v))

                elif line[: 2] == 'f ':
                    x, y, z = line[2:].split()
                    x = int(x[: len(x)//2]) - 1
                    y = int(y[: len(y)//2]) - 1
                    z = int(z[: len(z)//2]) - 1
                    faces.append((x, y, z))
    except(FileNotFoundError):
        print('file not found')

    return (vertices, uv, faces)


def write_obj(vertices: list, import_path: str, export_path: str) -> None:

    with open(export_path, 'w') as export:
        export.write('o face\nmtllib face.mtl\n\n# Vertices\n')
        for vertex in vertices:
            x, y, z = vertex
            export.writelines('v ' + str(x) + ' ' + str(y) + ' ' + str(z) + '\n')

        with open(import_path, 'r') as file:
            try: 
                lines = file.readlines()

                for line in lines:
                    if line[: 2] == 'vt' or line[: 2] == 'vn' or line[: 2] == 'f ':
                        export.writelines(line)
            except FileNotFoundError:
                 print('file not found')


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


def restructure_face(mp_vertices: np.mat, mp_faces: np.mat, import_face_path: str, export_face_path: str) -> None:
    # delete all objects before importing
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    # import .obj file to restructure face
    src_obj = bpy.ops.import_scene.obj(filepath = import_face_path)
    selected_obj = bpy.context.selected_objects
    bpy.context.view_layer.objects.active = selected_obj[0]
    ob = bpy.context.active_object
    mesh = ob.data
    mat_world = ob.matrix_world


    # toggle to EDIT mode
    bpy.ops.object.mode_set(mode='EDIT')

    # move face to mp_face
    visited = set()
    res_vertices = []
    x, y, z = 0, 0, 0

    for vertex in mesh.vertices:
        mapped = FALSE
        for vertex_indices in mp_faces:
            x, y, z = vertex.co.x, vertex.co.y, vertex.co.z
            if vertex not in visited and inside_triangle((x, y, z), (mp_vertices[vertex_indices[0]], 
                                                                    mp_vertices[vertex_indices[1]], 
                                                                    mp_vertices[vertex_indices[2]])):
                point = mp_vertices[vertex_indices[0]]
                plane = np.cross(mp_vertices[vertex_indices[1]] - point,
                                mp_vertices[vertex_indices[2]] - point)
                print('y before: ', y, end=' ')
                y  = (plane[0]*(point[0] - x) + plane[1]*point[1] + plane[2]*(point[2] - z))/plane[1]
                print('y after: ', y)

                res_vertices.append((x, y, z))
                mapped = TRUE

                # pos_world = mat_world @ vertex.co
                # pos_world.y = pos_world.y + y
                # vertex.co = mat_world.inverted() @ pos_world

                # mat_edit = mat_world.inverted() @ Matrix.Translation(Vector((0, y, 0))) @ mat_world
                # vertex.co = mat_edit @ vertex.co
                # move vertex to x, y, z

                # vertex.co.y = y
                # visited.add(vertex)

        if not mapped:
            res_vertices((x, y, z))
            # visited.add((x, y, z))
                
    
    # write obj
    write_obj(res_vertices, import_face_path, export_face_path)

    # toggle to OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # export restructured .obj file
    # bpy.ops.export_scene.obj(filepath = export_face_path)


# driver code
if __name__ == '__main__':

    mp_face = 'C:\\Users\\Rupak\\Documents\\Study\\Placement\\Internship\\PixelHash\\Task-6\\mp_face.obj'
    import_face = 'C:/Users/Rupak/Documents/Study/Placement/Internship/PixelHash/Task-6/face.obj'
    export_face = 'C:/Users/Rupak/Documents/Study/Placement/Internship/PixelHash/Task-6/export.obj'
    # mp_face, import_face, export_face = sys.argv[1], sys.argv[2], sys.argv[3]
    vertices, uv, faces = get_vertices_uv_vn_faces(mp_face)
    vertices = np.array(vertices)
    faces = np.array(faces)

    print(vertices)
    print(faces)

    restructure_face(vertices, faces, import_face, export_face)
