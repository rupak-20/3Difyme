import cv2 as cv
import sys
import numpy as np


def draw_uv(image_path: str, uv_path: str):
    # open wavefront file and get texture coordinates
    try:
        with open(uv_path, 'r') as uv:
            lines = uv.readlines()

            # open the image file
            img = cv.imread(image_path)
            vertices = {}
            faces = {}
            face = []
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

                    faces[j] = np.array((vertices[x], vertices[y], vertices[z]))

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
                (img.shape[0], img.shape[1], img.shape[2]), dtype=np.int8)

            LIPS = {61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 292, 375, 321, 405, 314, 17, 84, 181, 91, 146, 76, 184, 74, 73, 72, 11, 302, 303, 304, 408, 206, 307, 320, 404, 315, 16, 85, 180, 90,
                    77, 62, 183, 42, 41, 38, 12, 268, 271, 272, 407, 293, 325, 319, 403, 316, 15, 86, 179, 89, 96, 78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 306}
            RIGHT_EYE = {390, 373, 374, 380, 381, 382, 362,
                         398, 384, 385, 386, 387, 388, 466, 263, 249}
            LEFT_EYE = {7, 163, 144, 145, 153, 154, 155,
                        133, 173, 157, 158, 159, 160, 161, 246, 33}
            RIGHT_EYEBROW = {395, 397, 491, 493, 247, 249, 263, 265, 255, 257}
            LEFT_EYEBROW = {394, 396, 490, 492, 246, 248, 262, 264, 254, 256}

            print(type([faces[0]]))

            # for i in LIPS:
            #     cv.fillPoly(mask, pts=[faces[i]], color=(255, 255, 255))
            # for i in RIGHT_EYE:
            #     cv.fillPoly(mask, pts=[faces[i]], color=(255, 255, 255))
            # for i in LEFT_EYE:
            #     cv.fillPoly(mask, pts=[faces[i]], color=(255, 255, 255))
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

    except FileNotFoundError:
        print('wavefront or image file is missing')


if __name__ == '__main__':
    img, uv = sys.argv[1:]
    draw_uv(img, uv)
