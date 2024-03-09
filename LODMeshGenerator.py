import bpy
import os

bl_info = {
    "name": "LOD Generators",
    "author": "David Pitcher",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > LOD Gen Panel",
    "description": "Generates LODs for the active object using different methods and scaling options",
    "category": "Object",
}

# Define the property group class first
class LODGenProperties(bpy.types.PropertyGroup):
    scaling_options: bpy.props.EnumProperty(
        name="Apply Scalings",
        description="Choose how to apply scalings for FBX export",
        items=[
            ('FBX_SCALE_ALL', 'All Local', 'Apply all local scalings'),
            ('FBX_SCALE_UNITS', 'FBX Units Scale', 'Apply FBX unit scaling'),
        ],
        default='FBX_SCALE_ALL'
    )

    base_name_options: bpy.props.EnumProperty(
        name="Base Name",
        description="Choose base name source for LOD generation",
        items=[
            ('FILE_NAME', 'From Blender File', 'Use the Blender file name as base'),
            ('OBJECT_NAME', 'From Object Name', 'Use the object name as base'),
        ],
        default='FILE_NAME'
    )

# Define the main operator
class GenerateLODsOperator(bpy.types.Operator):
    """Generate LODs with selected options"""
    bl_idname = "object.generate_lods"
    bl_label = "Generate LODs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        lod_props = context.scene.lod_gen_props
        # Insert your LOD generation logic here using lod_props.scaling_options and lod_props.base_name_options
        self.report({'INFO'}, "LODs Generated Successfully")
        return {'FINISHED'}

# Define the quick generation operator
class QuickGenerateLODsOperator(bpy.types.Operator):
    """Quickly Generate LODs using Object Name and FBX Units Scale"""
    bl_idname = "object.quick_generate_lods"
    bl_label = "Quick Generate LODs (Object Name, FBX Units)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Insert your quick LOD generation logic here for Object Name and FBX Units Scale
        self.report({'INFO'}, "Quick LODs Generated Successfully (Object Name, FBX Units)")
        return {'FINISHED'}

# Define the panel
class LODGenPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "LOD Generators"
    bl_idname = "OBJECT_PT_lod_gens"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LOD Gen'

    def draw(self, context):
        lod_props = context.scene.lod_gen_props
        layout = self.layout

        layout.label(text="Custom LOD Generation:")
        layout.prop(lod_props, 'scaling_options', text="Scaling Option")
        layout.prop(lod_props, 'base_name_options', text="Base Name Source")
        layout.operator(GenerateLODsOperator.bl_idname)

        layout.separator()

        layout.label(text="Quick LOD Generation:")
        layout.operator(QuickGenerateLODsOperator.bl_idname)

# Register and unregister functions
def register():
    bpy.utils.register_class(LODGenProperties)
    bpy.types.Scene.lod_gen_props = bpy.props.PointerProperty(type=LODGenProperties)
    bpy.utils.register_class(GenerateLODsOperator)
    bpy.utils.register_class(QuickGenerateLODsOperator)
    bpy.utils.register_class(LODGenPanel)

def unregister():
    bpy.utils.unregister_class(LODGenProperties)
    del bpy.types.Scene.lod_gen_props
    bpy.utils.unregister_class(GenerateLODsOperator)
    bpy.utils.unregister_class(QuickGenerateLODsOperator)
    bpy.utils.unregister_class(LODGenPanel)

if __name__ == "__main__":
    register()
