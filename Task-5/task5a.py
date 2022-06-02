import sys

import cv2 as cv
import mediapipe as mp
import numpy as np


# conveting image to .temp file
def imageToVertex(image: np.mat) -> None:
    # mediapipe config
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.8) as pose:

        # conveting the image to RGB before processing
        results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

        if results.pose_landmarks:
            # translating and rotating points to bring the subject to origin
            nose = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x, results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.NOSE].y, results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].z)
            left_foot_index = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x, results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].z)
            right_foot_index = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x, results.pose_landmarks.landmark[
                            mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].z)
            # left_hip = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x, results.pose_landmarks.landmark[
            #                 mp_pose.PoseLandmark.LEFT_HIP].y, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].z)
            # right_hip = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x, results.pose_landmarks.landmark[
            #                 mp_pose.PoseLandmark.RIGHT_HIP].y, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].z)
            # left_heel = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL].x, results.pose_landmarks.landmark[
            #                 mp_pose.PoseLandmark.LEFT_HEEL].y, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL].z)

            lowest_point = left_foot_index if left_foot_index[1] > right_foot_index[1] else right_foot_index
            # hip_dist = ((left_hip[0]-right_hip[0])**2 + (left_hip[1]-right_hip[1])**2 + (left_hip[2]-right_hip[2])**2)**0.5
            # foot_dist = ((left_foot_index[0]-left_heel[0])**2 + (left_foot_index[1]-left_heel[1])**2 + (left_foot_index[2]-left_heel[2])**2)**0.5
            # scale =  hip_dist/foot_dist
                    

            vertices = {}
            _ = 1
            # writing vertices
            with open('temp.obj', 'w') as export:
                export.write('o face\nmtllib face.mtl\n\n# Vertices\n')
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    x, y, z = (lm.x - nose[0]) * 100, (-lm.y + lowest_point[1]) * 100, (-lm.z + lowest_point[2]) *100*0.375

                    # saving vertices for future
                    vertices[_] = (x, y, z)
                    _ = _ + 1
                    export.writelines('v ' + str(x) + ' ' + str(y) + ' ' + str(z) + '\n')

                # writing uv
                export.write('\n\n#UV\n')
                for vertex in vertices.values():
                    export.writelines(
                        'vt ' + str(vertex[0]) + ' ' + str(vertex[1]) + '\n')

                # writing faces
                export.write('\n\n#Faces\n')
                for conn in mp_pose.POSE_CONNECTIONS:
                    export.writelines(
                        'f ' + str(conn[0] + 1) + ' ' + str(conn[1] + 1) + '\n')


# driver code
if __name__ == "__main__":
    img_path = sys.argv[1]
    img = cv.imread(img_path)

    imageToVertex(img)
