import sys
from collections import OrderedDict

import bpy
import numpy as np
from mathutils import Matrix

VERTICES = np.zeros([33, 3])
ARMS_LEGS_FOOT = OrderedDict({
                'mixamorig:LeftShoulder': (12, 11), 'mixamorig:RightShoulder': (11, 12),
                'mixamorig:LeftArm': (11, 13), 'mixamorig:RightArm': (12, 14),
                'mixamorig:LeftForeArm': (13, 15), 'mixamorig:RightForeArm': (14, 16),
                'mixamorig:LeftUpLeg' : (23, 25), 'mixamorig:RightUpLeg': (24, 26),
                'mixamorig:LeftLeg': (25, 27), 'mixamorig:RightLeg': (26, 28), 
                'mixamorig:LeftFoot': (27, 31), 'mixamorig:RightFoot': (28, 32),
                'mixamorig:LeftToeBase': (29, 31), 'mixamorig:RightToeBase': (30, 32),
                'mixamorig:LeftToe_End': (29, 31), 'mixamorig:RightToe_End': (30, 32)
                })
SPINE = OrderedDict({
        'mixamorig:Hips': (23, 24, 11, 12), 'mixamorig:Spine': (23, 24, 11, 12),
        'mixamorig:Spine1': (23, 24, 11, 12), 'mixamorig:Spine2': (23, 24, 11, 12)
        })


# roll bone with the angle between 2 vectors
def bone_roll(bone_name: str, vector1: np.mat, vector2: np.mat, direction: int, axis: str) -> None:
    unit_vector1 = vector1 / np.linalg.norm(vector1)
    unit_vector2 = vector2 / np.linalg.norm(vector2)
    dot_product = np.dot(unit_vector1, unit_vector2)
    angle = np.arccos(dot_product)

    bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'
    ob = bpy.context.active_object
    bone = ob.pose.bones[bone_name]
    bone.rotation_mode = 'XYZ'
    bone.rotation_euler.rotate_axis(axis, direction * angle)


# rotate bone to the given vector
def rotate_bone(bone_vector: np.mat, bone) -> None:
    bone_vector = bone_vector / np.linalg.norm(bone_vector)
    rotation = bone.vector.rotation_difference(bone_vector)
    M = (
    Matrix.Translation(bone.head) @
    rotation.to_matrix().to_4x4() @
    Matrix.Translation(-bone.head)
    )
    bone.matrix = M @ bone.matrix


# set face and neck
def set_face() -> None:
    ob = bpy.context.active_object
    md_face_vector = (VERTICES[3] + VERTICES[6])/2 - (VERTICES[7] + VERTICES[8])/2
    right_shoulder_vector = np.array(ob.pose.bones['mixamorig:RightShoulder'].head - ob.pose.bones['mixamorig:Head'].head)
    left_shoulder_vector = np.array(ob.pose.bones['mixamorig:LeftShoulder'].head - ob.pose.bones['mixamorig:Head'].head)
    face_normal_vector = np.cross(right_shoulder_vector, left_shoulder_vector)
    cross_1 = np.cross(md_face_vector, face_normal_vector)
    
    if cross_1[2] < 0:
        bone_roll('mixamorig:Neck', face_normal_vector, md_face_vector, 1, 'Y')
    else:
        bone_roll('mixamorig:Neck', face_normal_vector, md_face_vector, -1, 'Y')
    if cross_1[0] > 0:
        bone_roll('mixamorig:Head', face_normal_vector, md_face_vector, -1, 'X')
    else:
        bone_roll('mixamorig:Head', face_normal_vector, md_face_vector, 1, 'X')


# set spine
def set_spine() -> None:
    ob = bpy.context.active_object
    act_arm = bpy.context.object

    for (bone_name, index) in SPINE.items():
        act_arm.data.edit_bones[bone_name].use_inherit_rotation = False
        bone = ob.pose.bones[bone_name]
        point_1 = (VERTICES[index[0]] + VERTICES[index[1]])/2
        point_2 = (VERTICES[index[2]] + VERTICES[index[3]])/2
        mp_bone_vector = point_2 - point_1
        rotate_bone(mp_bone_vector, bone)


# set arms, legs and feet
def set_limbs() -> None:
    ob = bpy.context.active_object
    act_arm = bpy.context.object
    
    for (bone_name, index) in ARMS_LEGS_FOOT.items():
        act_arm.data.edit_bones[bone_name].use_inherit_rotation = False
        bone = ob.pose.bones[bone_name]
        mp_bone_vector = VERTICES[index[1]] - VERTICES[index[0]]
        rotate_bone(mp_bone_vector, bone)


def set_hands() -> None:
    ob = bpy.context.active_object

    # arm and wrist roll in left hand (note the order of vectors in cross product)
    md_left_wrist_index = VERTICES[19] - VERTICES[15]
    md_left_wrist_pinky = VERTICES[17] - VERTICES[15]
    left_wrist_index = np.array((ob.pose.bones['mixamorig:LeftHandIndex4'].tail - ob.pose.bones['mixamorig:LeftHand'].tail))
    left_wrist_pinky = np.array((ob.pose.bones['mixamorig:LeftHandPinky4'].tail - ob.pose.bones['mixamorig:LeftHand'].tail))
    # find normal vector to left palm from vertices obtained from mediapipe
    left_hand_normal_vector = np.cross(left_wrist_pinky, left_wrist_index)
    # find normal vector to left palm from vertices obtained from armature
    md_left_hand_normal_vector = np.cross(md_left_wrist_pinky, md_left_wrist_index)
    # roll arm and hand bone
    bone_roll('mixamorig:LeftHand', left_hand_normal_vector, md_left_hand_normal_vector, -1/2, 'Y')
    bone_roll('mixamorig:LeftForeArm', left_hand_normal_vector, md_left_hand_normal_vector, -1/2, 'Y')

    # arm and wrist roll in right hand
    md_right_wrist_index = VERTICES[20] - VERTICES[16]
    md_right_wrist_pinky = VERTICES[18] - VERTICES[16]
    right_wrist_index = np.array((ob.pose.bones['mixamorig:RightHandIndex4'].tail - ob.pose.bones['mixamorig:RightHand'].tail))
    right_wrist_pinky = np.array((ob.pose.bones['mixamorig:RightHandPinky4'].tail - ob.pose.bones['mixamorig:RightHand'].tail))
    # find normal vector to right palm from vertices obtained from mediapipe
    right_hand_normal_vector = np.cross(right_wrist_index, right_wrist_pinky)
    # find normal vector to right palm from vertices obtained from armature
    md_right_hand_normal_vector = np.cross(md_right_wrist_index, md_right_wrist_pinky)

    bone_roll('mixamorig:RightHand', right_hand_normal_vector, md_right_hand_normal_vector, 1/2, 'Y')
    bone_roll('mixamorig:RightForeArm', right_hand_normal_vector, md_right_hand_normal_vector, 1/2, 'Y')


# making pose from the given vertices
def armaturePose(import_fbx_path: str, export_fbx_path) -> None:
    # delete all objects before importing
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    # import .fbx file to add pose
    src_obj = bpy.ops.import_scene.fbx(filepath = import_fbx_path)
    selected_obj = bpy.context.active_object

    # toggle to EDIT mode
    bpy.ops.object.mode_set(mode='EDIT')
    # set spine
    set_spine()
    # set limbs
    set_limbs()
    # toggle to POSE mode
    bpy.ops.object.mode_set(mode='POSE')
    # set hands
    set_hands()
    # set face and neck
    set_face()
    # toggle to OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # export .fbx file
    bpy.ops.export_scene.fbx(filepath = export_fbx_path)


# driver code
if __name__ == "__main__":
    # get import path for .fbx file, export path for .fbx file and .obj file path
    fbx_path, export_path, obj_path = sys.argv[4], sys.argv[5], sys.argv[6]
    i = 0

    try:
        # read .obj file to get vertices
        with open(obj_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line[0] == 'v' and line[1] != 't':
                    _, x, y, z = list(line.split(' '))
                    # store vertices as an numpy array
                    VERTICES[i][0], VERTICES[i][1], VERTICES[i][2] = x, y, z
                    i = i+1
    except(FileNotFoundError):
        print('file not found')

    armaturePose(fbx_path, export_path)
