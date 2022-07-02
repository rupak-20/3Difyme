import sys
from math import acos

import cv2 as cv
import mediapipe as mp
import numpy as np


class Headshot:
    # in order of left, center, right
    images = []
    vertices = np.empty([3, 468, 3])
    hidden_faces = []
    uv = np.empty([3, 468, 2])
    faces = []      # same for every face mesh

    # get images (left, center, right) and face
    def __init__(self, left_img: np.mat, center_img: np.mat, right_img: np.mat, faces: np.mat):
        self.images = [left_img, center_img, right_img]
        # print(self.images[0].shape)
        # print(self.images[1].shape)
        # print(self.images[2].shape)
        self.faces = faces

    
    # get vertices from mediapipe face mesh API
    def get_vertices(self):
        mp_face_mesh = mp.solutions.face_mesh

        for index, img in enumerate(self.images):
            with mp_face_mesh.FaceMesh(
                    static_image_mode=True,
                    max_num_faces=1,
                    min_detection_confidence=0.8) as face_mesh:

                results = face_mesh.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))
                ver = np.empty([468, 3])

                for face in results.multi_face_landmarks:
                    for i, landmark in enumerate(face.landmark):
                        x = landmark.x
                        y = landmark.y
                        z = landmark.z

                        # shape = img.shape
                        # relative_x = int(x * shape[1])
                        # relative_y = int(y * shape[0])
                        # relative_z = int(z * shape[2])
                        ver[i] = [x, y, z]
            self.vertices[index] = ver


    # find hidden faces for all images
    def set_hidden_faces(self, camera_axis: np.mat, threshold: float = 90):
        for i in range(3):
            invisible = []

            for index, face in enumerate(self.faces):
                # print(self.vertices[i])
                vec1 = self.vertices[i][face[1]] - self.vertices[i][face[0]]
                vec2 = self.vertices[i][face[2]] - self.vertices[i][face[0]]
                normal = np.cross(vec1, vec2)   # normal to face (coming out of the plane)

                normal_mag = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
                camera_axis_mag = (camera_axis[0]**2 + camera_axis[1]**2 + camera_axis[2]**2)**0.5

                if normal_mag != 0 and camera_axis_mag != 0:
                    rad = acos(np.dot(normal, camera_axis) / (normal_mag*camera_axis_mag))
                    deg = np.rad2deg(rad)
                    if deg < threshold:
                        invisible.append(index)

            self.hidden_faces.append(invisible)


    # create uv from (x, y) coords of face mesh vertices
    def create_uv(self):
        for i in range(3):
            # height, width, _ = self.images[i].shape
            for j, vertex in enumerate(self.vertices[i]):
                self.uv[i][j] = [vertex[0], vertex[1]]
            # self.uv[i] = self.adjust_uv(self.uv[i])


    # def adjust_uv(self, uv: np.mat):
    #     # Flip UV vertically
    #     uv[::, 0] =  uv[::, 0] * -1 + 1

    #     # Rotate 180
    #     uv = (uv - 0.5) * -1 + 0.5
    #     return uv


    # draw vertices from face mesh on images
    def draw_uv(self):
        for i in range(3):
            img = np.copy(self.images[i])
            for (u, v) in self.uv[i]:
                u = u*self.images[i].shape[1]
                v = v*self.images[i].shape[0]
                u = int(u)
                v = int(v)
                img = cv.circle(img, (u, v), radius=1, color=(0, 0, 255), thickness=2)

            cv.imwrite(str(i) + '.jpg', img)


    # merge left and right image to fill hidden portions in center image
    def merge_img(self):
        self.create_uv()
        # self.draw_uv()
        consolidated_img_mask = np.zeros(self.images[1].shape, dtype=np.uint8)

        # combined image mask
        for face in self.hidden_faces[1]:
            if face not in self.hidden_faces[0]:
                # consolidated_img_mask =  cv.bitwise_or(consolidated_img_mask, self.transformed_img_patch(face, 0))
                consolidated_img_mask =  consolidated_img_mask + self.transformed_img_patch(face, 0)
            elif face not in self.hidden_faces[2]:
                # consolidated_img_mask = cv.bitwise_or(consolidated_img_mask, self.transformed_img_patch(face, 2))
                consolidated_img_mask =  consolidated_img_mask + self.transformed_img_patch(face, 2)

        cv.imwrite('consolidated_img_mask.jpg', consolidated_img_mask)


    # crop and transform image patch
    def transformed_img_patch(self, face_index: int, side_index):
        hc, wc = self.images[1].shape[:2]
        hs, ws = self.images[side_index].shape[:2]
        # source triangle ([[x1, y1], [x2, y2], [x3, y3]])
        src = np.array([[self.uv[side_index][self.faces[face_index][0]][0]*ws, self.uv[side_index][self.faces[face_index][0]][1]*hs],
                        [self.uv[side_index][self.faces[face_index][1]][0]*ws, self.uv[side_index][self.faces[face_index][1]][1]*hs],
                        [self.uv[side_index][self.faces[face_index][2]][0]*ws, self.uv[side_index][self.faces[face_index][2]][1]*hs]], dtype=int)
        # target triangle ([[x1, y1], [x2, y2], [x3, y3]])
        tgt = np.array([[self.uv[1][self.faces[face_index][0]][0]*wc, self.uv[1][self.faces[face_index][0]][1]*hc],
                        [self.uv[1][self.faces[face_index][1]][0]*wc, self.uv[1][self.faces[face_index][1]][1]*hc],
                        [self.uv[1][self.faces[face_index][2]][0]*wc, self.uv[1][self.faces[face_index][2]][1]*hc]], dtype=int)

        # code to verify the target or source points below. result stored in consolidated_img_mask
        # dst = np.zeros([hc, wc, 3], dtype = np.uint8)
        # for i in range(3):
        #     u, v = tgt[i]
        #     dst = cv.circle(dst, (u, v), radius=1, color=(255, 255, 255), thickness=2)

        r1 = cv.boundingRect(src)
        r2 = cv.boundingRect(tgt)
        tri1Cropped = []
        tri2Cropped = []

        for i in range(0, 3):
            tri1Cropped.append(((src[i][0] - r1[0]), (src[i][1] - r1[1])))
            tri2Cropped.append(((tgt[i][0] - r2[0]), (tgt[i][1] - r2[1])))

        # crop the bounding rect
        # rect = cv.boundingRect(src)
        # x,y,w,h = rect
        # cropped = self.images[side_index][y:y+h, x:x+w].copy()
        base = self.images[side_index].copy()
        # make mask
        src_pts = src - src.min(axis=0)
        mask = np.zeros(base.shape[:2], np.uint8)
        cv.drawContours(mask, [src_pts], -1, (255, 255, 255), -1, cv.LINE_AA)
        # do bit-op
        dst = cv.bitwise_and(base, base, mask=mask)

        # apply affine transformation to dst
        M = cv.getAffineTransform(np.float32(tri1Cropped), np.float32(tri2Cropped))
        dst = cv.warpAffine(dst, M, base.shape[-2::-1], None, flags=cv.INTER_LINEAR, borderMode=cv.BORDER_REFLECT_101)

        return dst


    # write .obj files for face mesh
    def write_obj(self, obj_path: str, save_hidden: bool = True, save_faces: bool = True):
        for i, file_name in enumerate(['left', 'center', 'right']):
            with open(obj_path + '/' + file_name + '.obj', 'w') as export:
                export.write('face\nmtllib face.mtl\n\n# Vertices\n')

                for vertex in self.vertices[i]:
                    x, y, z = vertex[0], -vertex[1], -vertex[2]
                    export.writelines('v ' + str(x) + ' ' +
                                      str(y) + ' ' + str(z) + '\n')

                export.write('\n\n#Faces\n')
                if save_faces == True:
                    for face in self.faces:
                        export.writelines(
                            'f ' + str(face[0] + 1) + ' ' + str(face[1] + 1) + ' ' + str(face[2] + 1) + '\n')

        # save another .obj file for hidden vertices
        if save_hidden == True:
            for i, file_name in enumerate(['left_hidden', 'center_hidden', 'right_hidden']):
                with open(obj_path + '/' + file_name + '.obj', 'w') as export:
                    export.write('face\nmtllib face.mtl\n\n# Vertices\n')

                    for ver in self.hidden_faces[i]:
                        v1 = self.vertices[i][self.faces[ver][0]]
                        v2 = self.vertices[i][self.faces[ver][1]]
                        v3 = self.vertices[i][self.faces[ver][2]]
                        export.writelines(
                            'v ' + str(v1[0]) + ' ' + str(-v1[1]) + ' ' + str(-v1[2]) + '\n')
                        export.writelines(
                            'v ' + str(v2[0]) + ' ' + str(-v2[1]) + ' ' + str(-v2[2]) + '\n')
                        export.writelines(
                            'v ' + str(v3[0]) + ' ' + str(-v3[1]) + ' ' + str(-v3[2]) + '\n')
                    export.write('\n\n#Faces\n')


# get faces from a pre-existing face_mesh.obj file
def get_faces(obj_path: str) -> list:
    faces = []

    with open(obj_path, 'r') as obj:
        lines = obj.readlines()

        for line in lines:
            if line[: 2] == 'f ':
                v1, v2, v3 = line[2:].split()
                v1 = int(v1[: len(v1)//2]) - 1
                v2 = int(v2[: len(v2)//2]) - 1
                v3 = int(v3[: len(v3)//2]) - 1
                faces.append([v1, v2, v3])

    return faces


# driver code
def main(left_img_path: str, center_img_path: str, right_img_path: str, obj_path: str):
    threshold = 90      # threshold angle in deg
    camera_axis = np.array([0, 0, 1])
    left_img = cv.imread(left_img_path)
    center_img = cv.imread(center_img_path)
    right_img = cv.imread(right_img_path)
    # faces and vertices index are same
    faces = np.asarray(get_faces(obj_path + 'mp_face.obj'))

    head = Headshot(left_img, center_img, right_img, faces)
    head.get_vertices()
    head.set_hidden_faces(camera_axis)

    head.write_obj(obj_path, True)

    head.merge_img()


if __name__ == "__main__":
    # requires left img, center img, right img and face_mesh obj file path
    left_img_path, center_img_path, right_img_path, obj_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    main(left_img_path, center_img_path, right_img_path, obj_path)
