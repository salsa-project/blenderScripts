import bpy
import random
import math

# Deselect all objects
bpy.ops.object.select_all(action="DESELECT")

# Set the number of frames in the animation
bpy.context.scene.frame_end = 350

# Set the frame rate
bpy.context.scene.render.fps = 30



# Add the spheres
spheres = []
emission_nodes = []
for i in range(10):
    # Add the sphere and select it
    bpy.ops.mesh.primitive_uv_sphere_add(
        location=(random.uniform(-100, 100), random.uniform(-100, 100), 0)
    )
    sphere = bpy.context.active_object

    spheres.append(sphere)
    
    # Add a new material to the sphere
    mat = bpy.data.materials.new(name="EmissionMaterial")


    # Set the material's properties
    mat.diffuse_color = (0, 1, 1, 1)  # Yellow
    mat.specular_intensity = 0
    mat.use_nodes = True
    node_tree = mat.node_tree

    # Add an emission node
    emission_node = node_tree.nodes.new(type="ShaderNodeEmission")
    emission_node.inputs[1].default_value = random.uniform(-100, 50)  # Initial emission strength
    emission_node.inputs[0].default_value = (0, 1, 1, 1)  # Yellow

    # Set the emission node as the output node
    node_tree.nodes.remove(node_tree.nodes[1])  # Remove the default diffuse node (dsiconnect Principled BSDF shader node)
    output_node = node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    node_tree.links.new(emission_node.outputs[0], output_node.inputs[0])
    
    sphere.data.materials.append(mat)
   

    # Set the sphere's scale
    scale = random.uniform(1, 2)
    sphere.scale = (scale, scale, scale)

    # Set the sphere's initial keyframe
    sphere.keyframe_insert(data_path="location", frame=1)
    
    # Set the emission initial keyframe
    emission_node.inputs[1].keyframe_insert(data_path="default_value", frame=1)
    
    # Set a random emission strength
    emission_node.inputs[1].default_value = random.uniform(-100, 50)
    
    # Set the keyframe
    emission_node.inputs[1].keyframe_insert(data_path="default_value", frame=i , index=-1)
    
    # Add the emission node to the list of emission nodes
    emission_nodes.append(emission_node)


# Animate the spheres
for i in range(1, 351):
    for index, sphere in enumerate(spheres):
        # Calculate the sphere's new location
        x = sphere.location.x + random.uniform(-1, 1)
        y = sphere.location.y + random.uniform(-1, 1)
        z = sphere.location.z + random.uniform(-2, 2)

        # Set the sphere's location
        sphere.location = (x, y, z)
    
        # Set the sphere's keyframe
        sphere.keyframe_insert(data_path="location", frame=i, index=-1)
        
        # get the emission_node for this sphere
        emission_node = emission_nodes[index]

        # Set a random emission strength
        emission_node.inputs[1].default_value = random.uniform(-100, 50)
    
        # Set the keyframe
        emission_node.inputs[1].keyframe_insert(data_path="default_value", frame=i , index=-1)