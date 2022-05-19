import cv2 as cv
import sys
import numpy as np


def recolour(image_path: str, uv_path: str):
    # open wavefront file and get texture coordinates
    try:
        with open(uv_path, 'r') as uv:
            lines = uv.readlines()

            # open the image file
            img = cv.imread(image_path)
            vertices = {}
            faces = {}
            i, j = 0, 0  # pointer variables

            for line in lines:

                # plot points
                if line[: 2] == 'vt':

                    # modify u and v to map onto the image {0 <= (u,v) <=1}
                    u, v = list(map(float, line[2:].split()))
                    u = u*img.shape[0]
                    v = img.shape[1] - v*img.shape[1]
                    u = int(u)
                    v = int(v)

                    # save vertices for drawing lines
                    vertices[i] = (u, v)
                    i = i+1

                    # plot the point on the image
                    img = cv.circle(img, [u, v], radius=0,
                                    color=(0, 0, 0), thickness=-1)

                elif line[0] == 'f':

                    x, y, z = line[2:].split()
                    x = int(x[: len(x)//2]) - 1
                    y = int(y[: len(y)//2]) - 1
                    z = int(z[: len(z)//2]) - 1

                    faces[j] = np.array(
                        (vertices[x], vertices[y], vertices[z]))

                    # plot the lines for a face
                    img = cv.line(img, pt1=faces[j][0], pt2=faces[j][1],
                                  color=(0, 0, 0), thickness=1)
                    img = cv.line(img, pt1=faces[j][1], pt2=faces[j][2],
                                  color=(0, 0, 0), thickness=1)
                    img = cv.line(img, pt1=faces[j][2], pt2=faces[j][0],
                                  color=(0, 0, 0), thickness=1)

                    j = j+1

            # write the uv mapped image file
            status = cv.imwrite('uv_map.png', img)
            if status == False:
                print('UV map not saved')
            else:
                print('UV map saved')

            # create a mask
            mask = np.zeros(
                (img.shape[0], img.shape[1], img.shape[2]), dtype=np.uint8)

            LIPS = {4, 5, 10, 11, 12, 13, 18, 19, 20, 21, 46, 47, 48, 49, 62, 63, 64, 65, 66, 67, 68, 69, 86, 87, 88, 89, 122, 123, 124, 125, 138, 139, 140, 141, 142, 143, 144, 145, 258, 259, 260, 261, 334, 335, 336, 337, 342, 343, 344, 345, 358, 359, 360, 361, 366, 367, 368, 369, 390, 391, 392, 393, 398, 399, 400, 401, 414, 415, 416, 417, 422,
                    423, 424, 425, 438, 439, 440, 441, 446, 447, 448, 449, 462, 463, 464, 465, 478, 479, 480, 481, 514, 515, 516, 517, 606, 607, 608, 609, 614, 615, 616, 617, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 698, 699, 700, 701, 702, 703, 704, 705, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897}
            RIGHT_EYE = {2, 3, 38, 40, 526, 528, 574,
                         576, 590, 592, 610, 612, 626, 628}
            LEFT_EYE = {0, 1, 39, 41, 527, 529, 575,
                        577, 591, 593, 611, 613, 627, 629}
            RIGHT_EYEBROW = {395, 397, 491, 493, 247, 249, 263, 265, 255, 257}
            LEFT_EYEBROW = {394, 396, 490, 492, 246, 248, 262, 264, 254, 256}

            for i in LIPS:
                cv.fillPoly(mask, pts=[faces[i]], color=(255, 255, 255))
            for i in RIGHT_EYE:
                cv.fillPoly(mask, pts=[faces[i]], color=(255, 255, 255))
            for i in LEFT_EYE:
                cv.fillPoly(mask, pts=[faces[i]], color=(255, 255, 255))
            for i in RIGHT_EYEBROW:
                cv.fillPoly(mask, pts=[faces[i]], color=(255, 255, 255))
            for i in LEFT_EYEBROW:
                cv.fillPoly(mask, pts=[faces[i]], color=(255, 255, 255))

            # write the mask image file
            status = cv.imwrite('mask.png', mask)
            if status == False:
                print('mask not saved')
            else:
                print('mask saved')

            # preserving colour
            img = cv.imread('face.png')
            albedo = cv.imread('face_albedo.png')
            mask = mask//255
            albedo = img*mask + albedo*(1-mask)

            # write the final image file
            status = cv.imwrite('coloured.png', albedo)
            if status == False:
                print('coloured image not saved')
            else:
                print('coloured image saved')

    except FileNotFoundError:
        print('wavefront or image file is missing')


if __name__ == '__main__':
    img, uv = sys.argv[1:]
    recolour(img, uv)
