import sys

import cv2 as cv
import mediapipe as mp
import numpy as np


# conveting image to .obj file
def imageToOBJ(image: np.mat, export_path: str) -> None:
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.8) as pose:

        # conveting the image to RGB before processing
        results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

        if results.pose_landmarks:
            with open(export_path, 'w') as export:
                scale = 4
                vertices = {}
                _ = 1

                # writing vertices
                export.write('o face\nmtllib face.mtl\n\n# Vertices\n')
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    x, y, z = float(lm.x * scale), float(lm.y * scale), float(lm.z * scale)
                    # saving vertices for future
                    vertices[_] = (x, y, z)
                    _ = _ + 1
                    export.writelines('v ' + str(x) + ' ' + str(y) + ' ' + str(z) + '\n')

                # writing uv
                export.write('\n\n#UV\n')
                for vertex in vertices.values():
                    export.writelines('vt ' + str(vertex[0]) + ' ' + str(vertex[1]) + '\n')

                # writing faces
                export.write('\n\n#Faces\n')
                for conn in mp_pose.POSE_CONNECTIONS:
                    export.writelines('f ' + str(conn[0] + 1) + ' ' + str(conn[1] + 1) + '\n')


# driver code
if __name__ == "__main__":
    _, img_path, export_path = sys.argv
    img = cv.imread(img_path)

    imageToOBJ(img, export_path)
