import bpy
import sys


def copy_animation(source_path: str, target_path: str, export_path: str):
    bpy.ops.import_scene.fbx(filepath=source_path)
    arm1 = bpy.context.active_object

    bpy.ops.import_scene.fbx(filepath=target_path)
    arm2 = bpy.context.active_object

    # Deselect everything
    bpy.ops.object.select_all(action='DESELECT')

    # Select armatures in correct order
    bpy.context.view_layer.objects.active = arm2
    arm2.select_set(True)

    bpy.context.view_layer.objects.active = arm1
    arm1.select_set(True)

    # Copy animation data
    bpy.ops.object.make_links_data(type='ANIMATION')

    # Deselect everything
    bpy.ops.object.select_all(action='DESELECT')

    # Select target armature only
    bpy.context.view_layer.objects.active = arm2
    arm2.select_set(True)

    # Export selected objects filtering ARMATURE type only
    bpy.ops.export_scene.fbx(filepath=export_path, use_selection=True, object_types={
                             'ARMATURE'}, add_leaf_bones=False)


if __name__ == '__main__':
    _, source, target = sys.argv

    copy_animation(source, target, 'export.fbx')