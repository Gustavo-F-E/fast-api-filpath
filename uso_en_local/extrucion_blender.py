import bpy

# Crear un perfil (por ejemplo, un círculo)
bpy.ops.mesh.primitive_circle_add(radius=1, location=(0, 0, 0))

# Crear una curva como trayectoria
bpy.ops.curve.primitive_bezier_curve_add(location=(0, 0, 0))
curve = bpy.context.object
curve.scale = (1, 1, 5)  # Escalar la curva para definir la trayectoria

# Usar un modificador de extrusión
profile = bpy.context.selected_objects[0]  # Seleccionar el perfil
profile.modifiers.new("CurveModifier", type='CURVE')
profile.modifiers["CurveModifier"].object = curve
