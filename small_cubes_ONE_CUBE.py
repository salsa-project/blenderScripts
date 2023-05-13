import bpy
import mathutils

# Set the dimensions of the grid and the size of each cube
grid_size = 3
cube_size = 1
cube_spacing = 3

# Create a new mesh for the cube
mesh = bpy.data.meshes.new("Cube")

# Define the vertices of the cube
verts = [(0, 0, 0),
         (cube_size, 0, 0),
         (cube_size, cube_size, 0),
         (0, cube_size, 0),
         (0, 0, cube_size),
         (cube_size, 0, cube_size),
         (cube_size, cube_size, cube_size),
         (0, cube_size, cube_size)]

# Define the faces of the cube
faces = [(0, 1, 2, 3),
         (1, 5, 6, 2),
         (5, 4, 7, 6),
         (4, 0, 3, 7),
         (0, 4, 5, 1),
         (3, 2, 6, 7)]

# Add the vertices and faces to the mesh
mesh.from_pydata(verts, [], faces)

# Create a new object for the cube
cube = bpy.data.objects.new("Cube", mesh)

# Create a new collection for the cubes
collection = bpy.data.collections.new("Cubes")
bpy.context.scene.collection.children.link(collection)

# Create a grid of cubes with fixed distance between cubes
for i in range(grid_size):
    for j in range(grid_size):
        for k in range(grid_size):
            # Create a new instance of the cube object
            instance = cube.copy()
            instance.data = mesh.copy()
            instance.matrix_world = mathutils.Matrix.Translation((i*cube_spacing, j*cube_spacing, k*cube_spacing))
            
            # Add the instance to the collection
            collection.objects.link(instance)
    
            # Create a new material for the cube
            mat = bpy.data.materials.new(name=f"Material{i}_{j}_{k}")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            principled_node = nodes.get("Principled BSDF")
            
            # Assign the material to the cube
            if instance.data.materials:
                instance.data.materials[0] = mat
            else:
                instance.data.materials.append(mat)
            
            # turn Screen space refraction ON (for the transparency , glass ...)
            instance.active_material.use_screen_refraction = True
            
            # Set the transmission value of the material (glass)
            mat.node_tree.nodes["Principled BSDF"].inputs["Transmission"].default_value = 1.0
            mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0
            
            # Set Emission
            mat.node_tree.nodes["Principled BSDF"].inputs["Emission"].default_value = (0.0, 0.0, 1.0, 1.0)
            mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0
            
            # Add a Subdivision Surface modifier to the object with 3 subdivisions
            subsurf_mod = instance.modifiers.new("Subdivision Surface", "SUBSURF")
            subsurf_mod.levels = 3
            
# Select all of the cubes
bpy.ops.object.select_all(action='SELECT')

# Select all of the cubes
for obj in collection.objects:
    obj.select_set(True)
    bpy.ops.object.shade_smooth()