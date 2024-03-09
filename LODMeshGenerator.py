import bpy
import os

bl_info = {
    "name": "LOD Generator",
    "author": "David Pitcher",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > LOD Gen Panel",
    "description": "Generates LODs for the active object with different scaling options",
    "category": "Object",
}

class GenerateLODsLocalOperator(bpy.types.Operator):
    """Generate LODs for the active object with All Local scaling"""
    bl_idname = "object.generate_lods_local"
    bl_label = "Generate LODs (All Local)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return self.generate_lods(context, 'FBX_SCALE_ALL')

    def generate_lods(self, context, scale_option):
        # Define the LOD levels and corresponding decimate ratios
        lod_levels = {
            'A': 1,
            'B': 0.8,
            'C': 0.5,
            'D': 0.3,
        }

        blend_file_path = bpy.data.filepath
        base_file_name, _ = os.path.splitext(os.path.basename(blend_file_path))

        if not base_file_name:
            self.report({'ERROR'}, "The Blender file needs to be saved to determine the base file name.")
            return {'CANCELLED'}

        original_obj = bpy.context.active_object

        for suffix, ratio in lod_levels.items():
            bpy.ops.object.duplicate()
            new_obj = bpy.context.active_object

            if ratio < 1:
                mod = new_obj.modifiers.new(name="Decimate", type='DECIMATE')
                mod.decimate_type = 'COLLAPSE'
                mod.ratio = ratio
                bpy.ops.object.modifier_apply(modifier=mod.name)

            for obj in bpy.context.scene.objects:
                if obj != new_obj:
                    bpy.data.objects.remove(obj, do_unlink=True)

            new_file_name = f"{base_file_name}{suffix}.blend"
            bpy.ops.wm.save_as_mainfile(filepath=new_file_name)
            
            export_file_name = f"{base_file_name}{suffix}.fbx"
            bpy.ops.export_scene.fbx(filepath=export_file_name, apply_scale_options=scale_option)

        self.report({'INFO'}, f"LODs Generated Successfully with {scale_option}")
        return {'FINISHED'}

class GenerateLODsUnitsOperator(GenerateLODsLocalOperator):
    """Generate LODs for the active object with FBX Units Scale"""
    bl_idname = "object.generate_lods_units"
    bl_label = "Generate LODs (FBX Units)"

    def execute(self, context):
        return self.generate_lods(context, 'FBX_SCALE_UNITS')

class LODGenPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "LOD Generator"
    bl_idname = "OBJECT_PT_lod_gen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LOD Gen'

    def draw(self, context):
        layout = self.layout
        layout.operator(GenerateLODsLocalOperator.bl_idname)
        layout.operator(GenerateLODsUnitsOperator.bl_idname)

def register():
    bpy.utils.register_class(GenerateLODsLocalOperator)
    bpy.utils.register_class(GenerateLODsUnitsOperator)
    bpy.utils.register_class(LODGenPanel)

def unregister():
    bpy.utils.unregister_class(GenerateLODsLocalOperator)
    bpy.utils.unregister_class(GenerateLODsUnitsOperator)
    bpy.utils.unregister_class(LODGenPanel)

if __name__ == "__main__":
    register()
