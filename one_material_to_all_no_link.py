import bpy

#####assign the same non-linked material to all objects in the scene####

# Get the material to assign to the objects
material = bpy.data.materials.get("led")

# If the material doesn't exist, create it
if material is None:
    material = bpy.data.materials.new(name="led")

    # Set the material to not be linked to any object
    material.use_fake_user = True

# Loop through all the objects in the scene and assign the material
for obj in bpy.context.scene.objects:
    obj.active_material = material.copy()