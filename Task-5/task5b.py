import bpy
import numpy as np
from collections import OrderedDict
from mathutils import Vector


# making pose from the given vertices
def armaturePose(vertices: np.mat) -> None:

    # Enter the OBJECT mode
    bpy.ops.object.mode_set( mode = 'OBJECT' )
    # Select and delete all objects to start with a clean space
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    # Import the source object and shift it to x=-1
    src_FBXfilePath = 'C:/Users/Rupak/Documents/Study/Placement/Internship/PixelHash/Task-5/temp.obj'
    src_obj = bpy.ops.import_scene.obj( filepath = src_FBXfilePath )
    selected_obj = bpy.context.selected_objects
    for obj in selected_obj:
        obj.scale[0] = 0.03
        obj.scale[1] = 0.03
        obj.scale[2] = 0.03
        obj.location[0] = 0
    
    src_OBJfilePath = 'C:/Users/Rupak/Documents/Study/Placement/Internship/PixelHash/Task-5/source.fbx'
    src_obj = bpy.ops.import_scene.fbx( filepath = src_OBJfilePath )
    selected_obj = bpy.context.active_object

    ARMS_LEGS_FOOT = OrderedDict({
                'mixamorig:LeftArm': (11, 13), 'mixamorig:RightArm': (12, 14),
                'mixamorig:LeftForeArm': (13, 15), 'mixamorig:RightForeArm': (14, 16),
                'mixamorig:LeftUpLeg' : (23, 25), 'mixamorig:RightUpLeg': (24, 26),
                'mixamorig:LeftLeg': (25, 27), 'mixamorig:RightLeg': (26, 28), 
                'mixamorig:LeftFoot': (27, 31), 'mixamorig:RightFoot': (28, 32),
                'mixamorig:LeftToeBase': (29, 31), 'mixamorig:RightToeBase': (30, 32),
                'mixamorig:LeftToe_End': (29, 31), 'mixamorig:RightToe_End': (30, 32)
                })
                
    SPINE = OrderedDict({'mixamorig:Hips': (), 'mixamorig:Spine' : (),
                        'mixamorig:Spine1': (), 'mixamorig:Spine2': ()})
                        
    parent_tail_loc = {}

    HEAD = {''}

    # hand: (wrist, pinky, index); thumb: (wrist, thumb); pinky: (wrist, pinky); index: (wrist, index)
    HANDS = {'mixamorig:LeftHand': (15, 17, 19), 'mixamorig:RightHand': (16, 18, 20),
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
            'mixamorig:LeftHandPinky4': (15, 17), 'mixamorig:RightHandPinky4': (16, 18)}

    # bones to add roll to
    ROLL = {}
    
    ob = bpy.context.active_object
    
    act_arm = bpy.context.object
    bpy.ops.object.mode_set(mode='EDIT')
    # rotate arms, legs and foot
    for (bone, index) in (ARMS_LEGS_FOOT).items():
        
        bone_vector = vertices[index[1]] - vertices[index[0]]
        bone_mag = (bone_vector[0]**2 + bone_vector[1]**2 + bone_vector[2]**2)**0.5
        bone_unit_vector = bone_vector / bone_mag
        
        bone_unit_vector = Vector((bone_unit_vector[0], bone_unit_vector[1], bone_unit_vector[2]))
        myBone = ob.pose.bones[bone]
        
        print(bone)
        print('Unit Vector: ', bone_unit_vector)

        print('Head: ', myBone.head)
        print('Tail: ', myBone.tail)
        print('Tail-Head: ', myBone.vector)
        
        bone_magnitude = (myBone.vector[0]**2 + myBone.vector[1]**2 + myBone.vector[2]**2)**0.5
        
        if bone == 'mixamorig:LeftArm' or bone == 'mixamorig:RightArm' or bone == 'mixamorig:LeftUpLeg' or bone == 'mixamorig:RightUpLeg':
            
            temp = myBone.head + (bone_unit_vector)*bone_magnitude
            if myBone.child:
                parent_tail_loc[myBone.child.name] = temp
                print(parent_tail_loc[myBone.child.name])
            act_arm.data.edit_bones[myBone.name].tail = temp
            
        else:
            
            temp = parent_tail_loc[myBone.name] + (bone_unit_vector)*bone_magnitude
            if myBone.child:
                parent_tail_loc[myBone.child.name] = temp
                print(parent_tail_loc[myBone.child.name])
            act_arm.data.edit_bones[myBone.name].tail = temp
        
        print('Bone Magnitude: ', bone_magnitude)
        print(bone_unit_vector*bone_magnitude)
        print('New Tail: ', myBone.tail)
        print()

    bpy.ops.object.mode_set(mode='OBJECT')


# driver code
if __name__ == "__main__":
    import_path = 'C:\\Users\\Rupak\\Documents\\Study\\Placement\\Internship\\PixelHash\\Task-5\\vertices.temp'
    vertices = np.zeros([33, 3])
    i = 0

    try:
        with open(import_path, 'r') as file:
            lines = file.readlines()

            for line in lines:
                _, x, y, z = list(line.split(' '))
                print(x, y, z)
                vertices[i][0], vertices[i][1], vertices[i][2] = x, y, z
                i = i+1
    
    except:
        print('file not found')

    armaturePose(vertices)
