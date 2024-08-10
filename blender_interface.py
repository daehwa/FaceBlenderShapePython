import bpy
import bmesh
import numpy as np
import open3d as o3d

class EMBlender:
    def __init__(self,path="sranipal_head.fbx"):
        self.load_fbx(path)
        self.set_params()
        self.set_active_object()
        self.init_visualizer()

    def init_visualizer(self):
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name='Pantoenna Viewer')

        ob = self.set_key_shapes(np.zeros(37))
        verts, faces = self.get_keypoints(ob)
        mesh_o3d = o3d.geometry.TriangleMesh()  
        mesh_o3d.vertices = o3d.utility.Vector3dVector(verts)
        mesh_o3d.triangles = o3d.utility.Vector3iVector(faces)
        mesh_o3d.compute_vertex_normals()
        # mesh_o3d.paint_uniform_color([0.9, 0.8, 0.7])
        vis.add_geometry(mesh_o3d)
        self.mesh_o3d = mesh_o3d
        self.vis = vis

    def update_visualizer(self,blender):
        ob = self.set_key_shapes(blender)
        verts, faces = self.get_keypoints(ob)
        self.mesh_o3d.vertices = o3d.utility.Vector3dVector(verts)
        self.mesh_o3d.triangles = o3d.utility.Vector3iVector(faces)
        self.mesh_o3d.compute_vertex_normals()
        self.vis.update_geometry(self.mesh_o3d)
        self.vis.poll_events()
        self.vis.update_renderer()

    def set_params(self):
        self.fig = None
        self.headings = np.array([
                "Jaw_Left","Jaw_Right","Jaw_Forward","Jaw_Open","Mouth_Ape_Shape",
                "Mouth_Upper_Left","Mouth_Upper_Right","Mouth_Lower_Left","Mouth_Lower_Right",
                "Mouth_Upper_Overturn","Mouth_Lower_Overturn","Mouth_Pout","Mouth_Smile_Left","Mouth_Smile_Right",
                "Mouth_Sad_Left","Mouth_Sad_Right","Cheek_Puff_Left","Cheek_Puff_Right","Cheek_Suck",
                "Mouth_Upper_UpLeft","Mouth_Upper_UpRight","Mouth_Lower_DownLeft","Mouth_Lower_DownRight",
                "Mouth_Upper_Inside","Mouth_Lower_Inside","Mouth_Lower_Overlay",
                "Tongue_LongStep1","Tongue_LongStep2","Tongue_Left","Tongue_Right","Tongue_Up","Tongue_Down",
                "Tongue_Roll","Tongue_UpLeft_Morph","Tongue_UpRight_Morph","Tongue_DownLeft_Morph","Tongue_DownRight_Morph"])

    def load_fbx(self,path):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.fbx(filepath = path)

    def set_active_object(self):
        head = bpy.data.objects['Head']
        self.active_obj = head
        bpy.context.view_layer.objects.active = self.active_obj
        me = self.active_obj.data

    def set_key_shapes(self,lipshape):
        bpy.context.object.update_from_editmode()
        for i,heading in enumerate(self.headings):
            self.active_obj.data.shape_keys.key_blocks[heading].value = lipshape[i]
        # make a modified and deformed copy
        ob = bpy.context.object.copy()
        me = self.get_modified_mesh(self.active_obj)
        ob.modifiers.clear()
        ob.data = me
        # bpy.context.collection.objects.link(ob)
        return ob

    def get_modified_mesh(self, ob, cage=False):
        bm = bmesh.new()
        bm.from_object(
                ob,
                bpy.context.evaluated_depsgraph_get(),
                cage=cage,
                )
        #bm.transform(ob.matrix_world)
        me = bpy.data.meshes.new("Deformed")
        bmesh.ops.triangulate(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
        return me

    # def get_keypoints(self,ob):
    #     verts = []
    #     for v in ob.data.vertices:
    #         x = v.co.x
    #         y = v.co.y
    #         z = v.co.z
    #         v_ = np.array([x,y,z])
    #         verts.append(v_)
    #     verts = np.array(verts)
    #     return verts

    def get_keypoints(self, ob):
        # Extract vertex coordinates (without normalization)
        verts = np.array([v.co for v in ob.data.vertices])
        # 3d plot
        # this way is faster
        # vertices = np.empty(len(ob.data.vertices) * 3, dtype=np.float32)
        # ob.data.vertices.foreach_get("co", vertices)

        # # Reshape the array into a list of vectors (x, y, z)
        # verts = vertices.reshape((-1, 3))

        # Access the vertices and faces
        faces = np.array([f.vertices for f in ob.data.polygons])
        return verts, faces

    def filter_mouth_keypoints(self,keypoints):
        # upto 8800
        # keypoints = keypoints[0:100] # lower gum and tongue
        # keypoints = keypoints[180:314] # tongue boundary
        # keypoints = keypoints[314:400] # right eye
        # keypoints = keypoints[400:600] # eyes
        # keypoints = keypoints[600:3500] # upper gum and teeth
        # keypoints = keypoints[3500:5850] # lower gum and teeth
        ##### from here, they are on surface level ####
        # keypoints = keypoints[5850:5950] # some weird middle line
        # keypoints = keypoints[5950:5980] # right eye
        # keypoints = keypoints[5977:6015] # right lip boundary ********* 
        # keypoints = keypoints[6015:7350] # right surface others
        # keypoints = keypoints[7359:7397] # left lip boundary *********
        # keypoints = keypoints[7397:8800] # left surface others
        return keypoints

    # def get_eyes

    def get_lip(self,keypoints):
        lip = np.concatenate([keypoints[5977:6015],keypoints[7359:7397]])
        return lip

    def get_tongue(self,keypoints):
        tongue = keypoints[180:314]
        return tongue

    def get_cheek(self,keypoints):
        cheek = np.concatenate([keypoints[6341:6381],keypoints[7723:7763]])
        return cheek

    def get_key_tongue(self,tongue):
        tongue = tongue[59:60,:] # tongue tip
        return tongue

    def get_key_cheek(self,cheek):
        cheek_right = cheek[29,:]
        cheek_left = cheek[69,:]
        cheek = np.stack([cheek_right,cheek_left],axis=0)
        return cheek

if __name__ == "__main__":
    emb = EMBlender()
    for i in np.linspace(0,1,100):
        print(i)
        blender = np.ones(37)*i
        emb.update_visualizer(blender)


