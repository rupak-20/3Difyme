import cv2 as cv
import sys
import numpy as np


# function to recolour eyes, eyebrows and lips
def recolour(original_mat: np.mat, albedo_mat: np.mat, uv: list, faces: list):
    # scale (u, v)
    vertices = {}
    i, j = 0, 0

    for (u, v) in uv:
        u = u*original_mat.shape[0]
        v = original_mat.shape[1] - v*original_mat.shape[1]
        u = int(u)
        v = int(v)

        # save vertices
        vertices[i] = (u, v)
        i = i+1

    # create a mask
    mask = np.zeros(
        (original_mat.shape[0], original_mat.shape[1], original_mat.shape[2]), dtype=np.uint8)

    # face values
    LIPS = {4, 5, 10, 11, 12, 13, 18, 19, 20, 21, 46, 47, 48, 49, 62, 63, 64, 65, 66, 67, 68, 69, 86, 87, 88, 89, 122, 123, 124, 125, 138, 139, 140, 141, 142, 143, 144, 145, 258, 259, 260, 261, 334, 335, 336, 337, 342, 343, 344, 345, 358, 359, 360, 361, 366, 367, 368, 369, 390, 391, 392, 393, 398, 399, 400, 401, 414, 415, 416, 417, 422,
            423, 424, 425, 438, 439, 440, 441, 446, 447, 448, 449, 462, 463, 464, 465, 478, 479, 480, 481, 514, 515, 516, 517, 606, 607, 608, 609, 614, 615, 616, 617, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 698, 699, 700, 701, 702, 703, 704, 705, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897}
    RIGHT_EYE = {2, 3, 38, 40, 526, 528, 574,
                 576, 590, 592, 610, 612, 626, 628}
    LEFT_EYE = {0, 1, 39, 41, 527, 529, 575,
                577, 591, 593, 611, 613, 627, 629}
    RIGHT_EYEBROW = {395, 397, 491, 493, 247, 249, 263, 265, 255, 257}
    LEFT_EYEBROW = {394, 396, 490, 492, 246, 248, 262, 264, 254, 256}

    # fill faces to create mask
    for i in LIPS:
        cv.fillPoly(mask, pts=[np.array((
            vertices[faces[i][0]], vertices[faces[i][1]], vertices[faces[i][2]]))],  color=(255, 255, 255))
    for i in RIGHT_EYE:
        cv.fillPoly(mask, pts=[np.array((
            vertices[faces[i][0]], vertices[faces[i][1]], vertices[faces[i][2]]))], color=(255, 255, 255))
    for i in LEFT_EYE:
        cv.fillPoly(mask, pts=[np.array((
            vertices[faces[i][0]], vertices[faces[i][1]], vertices[faces[i][2]]))], color=(255, 255, 255))
    for i in RIGHT_EYEBROW:
        cv.fillPoly(mask, pts=[np.array((
            vertices[faces[i][0]], vertices[faces[i][1]], vertices[faces[i][2]]))], color=(255, 255, 255))
    for i in LEFT_EYEBROW:
        cv.fillPoly(mask, pts=[np.array((
            vertices[faces[i][0]], vertices[faces[i][1]], vertices[faces[i][2]]))], color=(255, 255, 255))

    # recolouring the image
    mask = mask//255
    albedo_mat = original_mat*mask + albedo_mat*(1-mask)

    # return recoloured matrix
    return albedo_mat


# driver function
if __name__ == '__main__':

    face_path, albedo_path, obj_path = sys.argv[1:]  # get paths

    img = cv.imread(face_path)   # read original image
    albedo = cv.imread(albedo_path)     # read albedo
    uv = []
    faces = []

    with open(obj_path, 'r') as obj:  # read uv
        lines = obj.readlines()

        for line in lines:
            if line[: 2] == 'vt':
                u, v = list(map(float, line[2:].split()))
                uv.append((u, v))

            elif line[0] == 'f':

                x, y, z = line[2:].split()
                x = int(x[: len(x)//2]) - 1
                y = int(y[: len(y)//2]) - 1
                z = int(z[: len(z)//2]) - 1

                faces.append([x, y, z])

    recoloured_img = recolour(img, albedo, uv, faces)
    status = cv.imwrite('recoloured.png', recoloured_img)
    if status:
        print('recoloured image saved')
    else:
        print('recoloured image not saved')
