from collections import OrderedDict
from math import acos

import bpy
import numpy as np
from mathutils import Matrix, Vector

OBJ_PATH = 'C:/Users/Rupak/Documents/Study/Placement/Internship/PixelHash/Task-5/temp.obj'
FBX_PATH = 'C:/Users/Rupak/Documents/Study/Placement/Internship/PixelHash/Task-5/source.fbx'
READ_OBJ_PATH = 'C:\\Users\\Rupak\\Documents\\Study\\Placement\\Internship\\PixelHash\\Task-5\\temp.obj'

# making pose from the given vertices
def armaturePose(vertices: np.mat) -> None:

    ARMS_LEGS_FOOT = OrderedDict({
                'mixamorig:LeftArm': (11, 13), 'mixamorig:RightArm': (12, 14),
                'mixamorig:LeftForeArm': (13, 15), 'mixamorig:RightForeArm': (14, 16),
                'mixamorig:LeftUpLeg' : (23, 25), 'mixamorig:RightUpLeg': (24, 26),
                'mixamorig:LeftLeg': (25, 27), 'mixamorig:RightLeg': (26, 28), 
                'mixamorig:LeftFoot': (27, 31), 'mixamorig:RightFoot': (28, 32),
                'mixamorig:LeftToeBase': (29, 31), 'mixamorig:RightToeBase': (30, 32),
                'mixamorig:LeftToe_End': (29, 31), 'mixamorig:RightToe_End': (30, 32)
                })
                
    SPINE = OrderedDict({
                'mixamorig:Hips': (), 'mixamorig:Spine' : (),
                'mixamorig:Spine1': (), 'mixamorig:Spine2': ()
                        })

    HAND = OrderedDict({
                'mixamorig:LeftHand': (15, 17, 19), 'mixamorig:RightHand': (16, 18, 20),
                'mixamorig:LeftHandThumb1': (15, 21), 'mixamorig:RightHandThumb1': (16, 22),
                'mixamorig:LeftHandThumb2': (15, 21), 'mixamorig:RightHandThumb2': (16, 22),
                'mixamorig:LeftHandThumb3': (15, 21), 'mixamorig:RightHandThumb3': (16, 22),
                'mixamorig:LeftHandThumb4': (15, 21), 'mixamorig:RightHandThumb4': (16, 22),
                'mixamorig:LeftHandIndex1': (15, 19), 'mixamorig:RightHandIndex1': (16, 20),
                'mixamorig:LeftHandIndex2': (15, 19), 'mixamorig:RightHandIndex2': (16, 20),
                'mixamorig:LeftHandIndex3': (15, 19), 'mixamorig:RightHandIndex3': (16, 20),
                'mixamorig:LeftHandIndex4': (15, 19), 'mixamorig:RightHandIndex4': (16, 20),
                'mixamorig:LeftHandMiddle1': (15, 17, 19), 'mixamorig:RightHandMiddle1': (16, 18, 20),
                'mixamorig:LeftHandMiddle2': (15, 17, 19), 'mixamorig:RightHandMiddle2': (16, 18, 20),
                'mixamorig:LeftHandMiddle3': (15, 17, 19), 'mixamorig:RightHandMiddle3': (16, 18, 20),
                'mixamorig:LeftHandMiddle4': (15, 17, 19), 'mixamorig:RightHandMiddle4': (16, 18, 20),
                'mixamorig:LeftHandRing1': (15, 17, 19), 'mixamorig:RightHandRing1': (16, 18, 20),
                'mixamorig:LeftHandRing2': (15, 17, 19), 'mixamorig:RightHandRing2': (16, 18, 20),
                'mixamorig:LeftHandRing3': (15, 17, 19), 'mixamorig:RightHandRing3': (16, 18, 20),
                'mixamorig:LeftHandRing4': (15, 17, 19), 'mixamorig:RightHandRing4': (16, 18, 20),
                'mixamorig:LeftHandPinky1': (15, 17), 'mixamorig:RightHandPinky1': (16, 18),
                'mixamorig:LeftHandPinky2': (15, 17), 'mixamorig:RightHandPinky2': (16, 18),
                'mixamorig:LeftHandPinky3': (15, 17), 'mixamorig:RightHandPinky3': (16, 18),
                'mixamorig:LeftHandPinky4': (15, 17), 'mixamorig:RightHandPinky4': (16, 18)
    })

    SPINE = OrderedDict({
            'mixamorig:Hips': (23, 24, 11, 12), 'mixamorig:Spine': (23, 24, 11, 12),
            'mixamorig:Spine1': (23, 24, 11, 12), 'mixamorig:Spine2': (23, 24, 11, 12)
    })

    # bones to add roll to
    ROLL = {}
    updated_pos_bones = {}
    
    ob = bpy.context.active_object

    act_arm = bpy.context.object
    bpy.ops.object.mode_set(mode='EDIT')
    
    '''
    SPINE
    '''
    for (bone, index) in (SPINE).items():
        
        print("-"*80)
        act_arm.data.edit_bones[bone].use_inherit_rotation = False
        myBone = ob.pose.bones[bone]
        print(bone)
        print('Head: ', myBone.head)
        print('Tail: ', myBone.tail)
        
        point_1 = (vertices[index[0]] + vertices[index[1]])/2
        point_2 = (vertices[index[2]] + vertices[index[3]])/2
        mp_bone_vector = point_2 - point_1
        mp_bone_unit_vector = mp_bone_vector / np.linalg.norm(mp_bone_vector)
                        
        rotation = myBone.vector.rotation_difference(mp_bone_unit_vector)
        print(rotation)
        M = (
        Matrix.Translation(myBone.head) @
        rotation.to_matrix().to_4x4() @
        Matrix.Translation(-myBone.head)
        )
        myBone.matrix = M @ myBone.matrix
        print('New Tail: ', myBone.tail)
    
    '''
    LIMBS
    '''
    for (bone, index) in (ARMS_LEGS_FOOT).items():
        
        print("-"*80)
        act_arm.data.edit_bones[bone].use_inherit_rotation = False
        myBone = ob.pose.bones[bone]
        print(bone)
        print('Head: ', myBone.head)
        print('Tail: ', myBone.tail)
        
        mp_bone_vector = vertices[index[1]] - vertices[index[0]]
        mp_bone_unit_vector = mp_bone_vector / np.linalg.norm(mp_bone_vector)    
                        
        rotation = myBone.vector.rotation_difference(mp_bone_unit_vector)
        print(rotation)
        M = (
        Matrix.Translation(myBone.head) @
        rotation.to_matrix().to_4x4() @
        Matrix.Translation(-myBone.head)
        )
        
#        if bone != 'mixamorig:LeftArm' and bone != 'mixamorig:RightArm' and bone != 'mixamorig:LeftUpLeg' and bone != 'mixamorig:RightUpLeg': 
#            myBone.matrix = updated_pos_bones[bone].inverted_safe() @ myBone.matrix
            
        myBone.matrix = M @ myBone.matrix
        
#        for child in myBone.children:
#            updated_pos_bones[child.name] = M
        
        print('New Tail: ', myBone.tail)

    '''
    END OF LIMBS
    '''
    for (bone, index) in (HAND).items():

        print("-"*80)
        act_arm.data.edit_bones[bone].use_inherit_rotation = False
        myBone = ob.pose.bones[bone]
        mp_bone_unit_vector = [0, 0, 0]
        print(bone)
        print('Head: ', myBone.head)
        print('Tail: ', myBone.tail)

        if len(index) == 3:

            mp_bone_vector_1 = vertices[index[1]] - vertices[index[0]]
            mp_bone_vector_2 = vertices[index[2]] - vertices[index[0]]
            mp_bone_vector_res = (mp_bone_vector_1 + mp_bone_vector_2) / 2
            mp_bone_unit_vector = mp_bone_vector_res / np.linalg.norm(mp_bone_vector_res)

        elif len(index) == 2:

            mp_bone_vector = vertices[index[1]] - vertices[index[0]]
            mp_bone_unit_vector = mp_bone_vector / np.linalg.norm(mp_bone_vector)


        rotation = myBone.vector.rotation_difference(mp_bone_unit_vector)
        print(rotation)
        M = (
        Matrix.Translation(myBone.head) @
        rotation.to_matrix().to_4x4() @
        Matrix.Translation(-myBone.head)
        )
        myBone.matrix = M @ myBone.matrix   
        print('New Tail: ', myBone.tail)
            

    bpy.ops.object.mode_set(mode='OBJECT')


# driver code
if __name__ == "__main__":
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    # Import the source object and shift it to x=-1
    src_obj = bpy.ops.import_scene.obj( filepath = OBJ_PATH )
    selected_obj = bpy.context.selected_objects
    for obj in selected_obj:
        obj.scale[0] = 0.03
        obj.scale[1] = 0.03
        obj.scale[2] = 0.03
        obj.location[0] = -1
    
    # source.fbx
    src_obj = bpy.ops.import_scene.fbx( filepath = FBX_PATH )
    selected_obj = bpy.context.active_object
    vertices = np.zeros([33, 3])
    i = 0
    try:
        with open(READ_OBJ_PATH, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line[0] == 'v':
                    _, x, y, z = list(line.split(' '))
#                    print(x, y, z)
#                    print()
                    vertices[i][0], vertices[i][1], vertices[i][2] = x, y, z
                    i = i+1
    
    except:
        print('file not found')
    armaturePose(vertices)
