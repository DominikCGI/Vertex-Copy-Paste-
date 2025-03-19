import bpy
import bmesh

bl_info = {
    "name": "Vertex Copy-Paste",
    "blender": (2, 80, 0),
    "category": "Mesh",
    "author": "KO-DCGI",
    "version": (1, 0),
    "description": "Copy and paste vertex coordinates",
    "location": "View3D > Sidebar > Tool Tab",
}

# Store copied coordinates globally
copied_coords = None

class CopyVertexCoordinates(bpy.types.Operator):
    """Copy selected vertex coordinates"""
    bl_idname = "mesh.copy_vertex_coords"
    bl_label = "Copy Vertex Coords"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global copied_coords
        obj = context.active_object
        if obj and obj.type == 'MESH' and obj.mode == 'EDIT':
            bm = bmesh.from_edit_mesh(obj.data)
            selected_verts = [v for v in bm.verts if v.select]
            if selected_verts:
                copied_coords = selected_verts[0].co.copy()
                self.report({'INFO'}, "Coordinates copied")
            else:
                self.report({'WARNING'}, "No vertex selected")
        else:
            self.report({'WARNING'}, "Not in Edit Mode or invalid object")
        return {'FINISHED'}

class PasteVertexCoordinates(bpy.types.Operator):
    """Paste copied vertex coordinates"""
    bl_idname = "mesh.paste_vertex_coords"
    bl_label = "Paste Vertex Coords"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global copied_coords
        obj = context.active_object
        if copied_coords and obj and obj.type == 'MESH' and obj.mode == 'EDIT':
            bm = bmesh.from_edit_mesh(obj.data)
            selected_verts = [v for v in bm.verts if v.select]
            if selected_verts:
                selected_verts[0].co = copied_coords
                bmesh.update_edit_mesh(obj.data)
                self.report({'INFO'}, "Coordinates pasted")
            else:
                self.report({'WARNING'}, "No vertex selected")
        else:
            self.report({'WARNING'}, "No copied coordinates or invalid mode")
        return {'FINISHED'}

class VIEW3D_PT_VertexCopyPastePanel(bpy.types.Panel):
    """Creates a Panel in the 3D View"""
    bl_label = "Vertex Copy-Paste"
    bl_idname = "VIEW3D_PT_vertex_copy_paste"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.copy_vertex_coords", text="Copy")
        layout.operator("mesh.paste_vertex_coords", text="Paste")

classes = [
    CopyVertexCoordinates,
    PasteVertexCoordinates,
    VIEW3D_PT_VertexCopyPastePanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
