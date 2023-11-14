import math
from pathlib import Path

radius = 1
width = 0.5
sides = 8
vertices = []
faces = []
normals = []

#Calculate the angle of the triangle
angle = 360 / sides

vertices.append((0, 0, width / 2))
vertices.append((0, 0, -width / 2))


for i in range(sides):
    # Calculate the angle in radians
    angleRad = math.radians(i * angle)

    # Calculate the coordinates of the vertex
    x = radius * math.cos(angleRad)
    y = radius * math.sin(angleRad)

    z_top = width / 2
    z_bottom = -width / 2

    # Calculate vertices for top and bottom faces
    vertices.append((x, y, z_top))
    vertices.append((x, y, z_bottom))

    magnitude = math.sqrt(x ** 2 + y ** 2 + z_top ** 2)
    a = x / magnitude
    b = y / magnitude
    c = z_top / magnitude

    # Calculate normals for top face
    normals.append((-a, -b, -c))

    magnitude = math.sqrt(x ** 2 + y ** 2 + z_bottom ** 2)
    a = x / magnitude
    b = y / magnitude
    c = z_bottom / magnitude

    # Calculate normals for bottom face
    normals.append((-a, -b, -c))

for i in range(sides):

    # j is used to get the next vertex
    j = (i + 1) % sides
    # j = 1
    # j = 2 ...

    # Create side faces 
    faces.append((i * 2, j * 2, j * 2 + 1)) # (2, 2, 3)
    faces.append((j * 2 + 1, i * 2 + 1, i * 2))


#Create faces for the top and bottom
for i in range(sides - 1):
    faces.append((1, (i + 1) * 2 + 1, (i + 1) * 2 + 3)) # (1, 3, 1)
    faces.append((2, (i + 1) * 2 + 4, (i + 1) * 2  +2 )) 

faces.append((1, 17, 3))
faces.append((2, 4, 18))


folderPath = Path("3DTest/Assets/Models/")
filePath = folderPath / "objWheelFile.obj"
with open(filePath, "w") as obj_file:
    obj_file.write("# OBJ File\n")

    obj_file.write("# Vertices: " + str(len(vertices)) + "\n")
    for vertex in vertices:
        obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

    obj_file.write("# Normals: " + str(len(normals)) + "\n")
    for normal in normals:
        obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")

    obj_file.write(f"# Faces: {len(faces)}\n")
    for face in faces:
        v1 = face[0]
        v2 = face[1]
        v3 = face[2]
        obj_file.write(f"f {v1}//1 {v2}//2 {v3}//3\n")