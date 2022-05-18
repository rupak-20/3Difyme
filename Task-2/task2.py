import cv2 as cv
import sys


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
                    img = cv.circle(img, (u, v), radius=0,
                                    color=(0, 0, 0), thickness=-1)

                elif line[0] == 'f':

                    x, y, z = line[2: ].split()
                    x = int(x[: len(x)//2]) - 1
                    y = int(y[: len(y)//2]) - 1
                    z = int(z[: len(z)//2]) - 1

                    faces[j] = (vertices[x], vertices[y], vertices[z])

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

    except FileNotFoundError:
        print('wavefront or image file is missing')


if __name__ == '__main__':
    img, uv = sys.argv[1:]
    draw_uv(img, uv)
