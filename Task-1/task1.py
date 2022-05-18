import bpy
import mathutils

cube = bpy.data.objects["Cube"]

# one blender unit in x-direction
#vec = mathutils.Vector((1.0, 0.0, 0.0))
#inv = cube.matrix_world.copy()
#inv.invert()

#vec_rot = vec @ inv
#cube.location = cube.location + vec_rot

# cube translation along x-axis by 10 units
cube.location[0] = 10

# cube rotation along y axis by 45 degree
cube.rotation_euler[1] = 0.78

# cube scaling by 2 units along x, y and z axis
cube.scale[0] = 2
cube.scale[1] = 2
cube.scale[2] = 2

# printing the object value of the seleted cube
print(bpy.context.active_object)