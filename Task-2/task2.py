import cv2 as cv
import sys


def draw_uv(image_path: str, uv_path: str):
    # open wavefront file and get texture coordinates
    try:
        with open(uv_path, 'r') as uv:
            lines = uv.readlines()

            # open the image file
            img = cv.imread(image_path)

            for line in lines:
                # ignore lines which do not begin with vt
                if line[: 2] != 'vt':
                    continue

                # modify u and v to map onto the image {0 <= (u,v) <=1}
                u, v = list(map(float, line[2:].split()))
                u = u*img.shape[0]
                v = img.shape[1] - v*img.shape[1]

                # plot the point on the image
                img = cv.circle(img, (int(u), int(v)), radius=0,
                                color=(0, 0, 0), thickness=-1)

            # write the uv mapped image file
            status = cv.imwrite('uv_map.png', img)
            if status == False:
                print('UV map not saved')
            else:
                print('UV map saved')

    except FileNotFoundError:
        print('wavefront or image file is missing')


if __name__ == '__main__':
    py, img, uv = sys.argv
    draw_uv(img, uv)
