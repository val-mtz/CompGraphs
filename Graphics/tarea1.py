import math
from pathlib import Path

def calculate_regular_polygon_vertices(sides, radius, depth):
    #interior_angle = (sides - 2) * math.pi / sides
    #angle_between_vertices = 2 * math.pi / sides

    vertices = []
    normals = []
    for i in range(sides):
        angle_rad = i * 2 * math.pi / sides
        x = radius * math.cos(angle_rad)
        y = radius * math.sin(angle_rad)
        z = 0 #depth
        vertices.append((x, y, z))

        normal = (x, y, z)        
        length = math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
        normal = (normal[0] / length, normal[1] / length, normal[2] / length)
        normals.append(normal)

        vertices.append((x, y, depth))
        
    return vertices, normals

def generate_faces(sides):
    faces = []
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((i * 2, j * 2, j * 2 + 1))
        faces.append((j * 2 + 1, i * 2 + 1, i * 2))
        faces.append((i * 2 + 1, j * 2 + 1, 1))
        faces.append((j * 2, i * 2, 0))

    return faces

#Pedir input
num_sides = input("Introduce el número de lados (entre 3 y 360): ")
if num_sides == "" or num_sides == "0":
        num_sides = "8"
        sides = int(num_sides)
else:
    sides = int(num_sides)
    while ((sides < 3 or sides > 360) and sides != 0):
        print("El número de lados debe estar entre 3 y 360")
        sides = int(input("Introduce el número de lados (entre 3 y 360): "))

str_radius = input("Introduce el radio de la rueda (float): ")
if str_radius == "":
    str_radius = "1.0"
radius = float(str_radius)

str_depth = input("Introduce el ancho de la rueda: ")
if str_depth == "":
    str_depth = "0.5"
depth = float(str_depth)

vertices, normals = calculate_regular_polygon_vertices(sides, radius, depth)
faces = generate_faces(sides)

# Output vertices, normals, and faces in OBJ format
folderPath = Path("../3DTest/Assets/Models/")
filePath = folderPath / "output.obj"
with open(filePath, "w") as obj_file:
    obj_file.write("# OBJ File\n")

    obj_file.write("# Vertices: " + str(len(vertices)) + "\n")
    for vertex in vertices:
        obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
    obj_file.write("# Normals: " + str(len(normals)) + "\n")
    for normal in normals:
        obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
    obj_file.write("# Faces: " + str(len(faces)) + "\n")
    for face in faces:
        obj_file.write(f"f {face[0]}//{sides+1} {face[1]}//{sides+1} {face[2]}//{sides+1}\n")

"""
def calculate_regular_polygon_vertices(sides, radius, depth):
    interior_angle = (sides - 2) * math.pi / sides
    angle_between_vertices = 2 * math.pi / sides

    vertices = []
    normals = []
    for i in range(sides):
        angle_rad = i * angle_between_vertices
        x = radius * math.cos(angle_rad)
        y = radius * math.sin(angle_rad)
        z = depth
        vertices.append((x, y, z))

        # Calculate normals (assuming the polygon is oriented along the z-axis)
        normal_x = x / radius
        normal_y = y / radius
        normal_z = 0
        normals.append((normal_x, normal_y, normal_z))

    return vertices, normals

def generate_faces(sides):
    faces = []
    for i in range(sides):
        vertex1 = i % sides
        vertex2 = (i + 1) % sides
        vertex3 = sides + vertex1
        vertex4 = sides + vertex2

        # Upper triangular face
        upper_face = (vertex1 + 1, vertex3 + 1, vertex2 + 1)
        faces.append(upper_face)

        # Lower triangular face
        lower_face = (vertex2 + 1, vertex3 + 1, vertex1 + 1)
        faces.append(lower_face)

        # Side faces
        side_face1 = (vertex1 + 1, vertex2 + 1, vertex4 + 1, vertex3 + 1)
        side_face2 = (vertex2 + 1, vertex1 + 1, vertex3 + 1, vertex4 + 1)
        faces.extend([side_face1, side_face2])

    return faces

# Example usage
num_sides = int(input("Introduce el número de lados (entre 3 y 360): "))
#If the user gives no input, use 10 as a default value
if num_sides == 0:
    num_sides = 8
while ((num_sides < 3 or num_sides > 360) and num_sides != 0):
    print("El número de lados debe estar entre 3 y 360")
    num_sides = int(input("Introduce el número de lados (float entre 3 y 360): "))
radius = float(input("Introduce el radio de la rueda (float): "))
if radius == 0:
    radius = 1.0
depth = float(input("Introduce el ancho de la rueda: "))
if depth == 0:
    depth = 0.5
vertices, normals = calculate_regular_polygon_vertices(num_sides, radius, depth)
faces = generate_faces(num_sides)

# Output vertices, normals, and faces in OBJ format
folderPath = Path("3DTest/Assets/Models/")
filePath = folderPath / "output.obj"
with open(filePath, "w") as obj_file:
    obj_file.write("# OBJ File\n")

    obj_file.write("# Vertices: " + str(len(vertices)) + "\n")
    for vertex in vertices:
        obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
    obj_file.write("# Normals: " + str(len(normals)) + "\n")
    for normal in normals:
        obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
    obj_file.write("# Faces: " + str(len(faces)) + "\n")
    for face in faces:
        obj_file.write(f"f {face[0]}//{num_sides+1} {face[1]}//{num_sides+1} {face[2]}//{num_sides+1}\n")
"""