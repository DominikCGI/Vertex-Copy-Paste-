import bpy
import bmesh

bl_info = {
    "name": "Vertex Copy-Paste",
    "blender": (2, 80, 0),
    "category": "Mesh",
    "author": "KO-DCGI",
    "version": (1, 1),
    "description": "Copy and paste multiple vertex coordinates across meshes while preserving strict selection order",
    "location": "View3D > Sidebar > Tool Tab",
}

# Store copied vertex coordinates in strict selection order
copied_coords = []

def get_selected_vertices(obj):
    """Returns a list of selected vertex coordinates in selection order using select_history."""
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    
    selected_verts = [ele for ele in reversed(bm.select_history) if isinstance(ele, bmesh.types.BMVert)]
    return [v.co.copy() for v in selected_verts]

def set_selected_vertices(obj, coords):
    """Applies stored coordinates to selected vertices in exact selection order."""
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    
    selected_verts = [ele for ele in reversed(bm.select_history) if isinstance(ele, bmesh.types.BMVert)]
    
    if len(selected_verts) != len(coords):
        return False  # Mismatch in selection count
    
    for v, new_co in zip(selected_verts, coords):
        v.co = new_co
    
    bmesh.update_edit_mesh(obj.data)
    return True

class CopyVertexCoordinates(bpy.types.Operator):
    """Copy selected vertex coordinates in strict selection order"""
    bl_idname = "mesh.copy_vertex_coords"
    bl_label = "Copy Vertex Coords"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global copied_coords
        obj = context.active_object
        if obj and obj.type == 'MESH' and obj.mode == 'EDIT':
            copied_coords = get_selected_vertices(obj)
            if copied_coords:
                self.report({'INFO'}, f"Copied {len(copied_coords)} vertices in strict order")
            else:
                self.report({'WARNING'}, "No vertices selected")
        else:
            self.report({'WARNING'}, "Not in Edit Mode or invalid object")
        return {'FINISHED'}

class PasteVertexCoordinates(bpy.types.Operator):
    """Paste copied vertex coordinates while preserving strict selection order"""
    bl_idname = "mesh.paste_vertex_coords"
    bl_label = "Paste Vertex Coords"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global copied_coords
        obj = context.active_object
        if copied_coords and obj and obj.type == 'MESH' and obj.mode == 'EDIT':
            success = set_selected_vertices(obj, copied_coords)
            if success:
                self.report({'INFO'}, f"Pasted {len(copied_coords)} vertices correctly in strict order")
            else:
                self.report({'WARNING'}, "Selection count mismatch – ensure you selected the same number of vertices")
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
