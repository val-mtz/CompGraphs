# Corrección tarea CG1
# Elaborado por Valeria Martínez Martínez - A01782413
# Fecha de última modificación: 28/11/2023

import math
from pathlib import Path

# Función para calcular los vértices de un polígono regular con base en el número de lados, el radio y el ancho
def calculate_vertices(sides, radius, depth):
    # Se crea una lista vacía para guardar los vértices
    vertices = []

    # Primero es necesario calcular el ángulo entre cada vértice en radianes, 
    # el cual se obtiene al dividir 2pi entre el número de lados
    angleRadians = (2 * math.pi) / sides

    # Variable para facilitar el cambio de ancho
    x = depth/2
    
    # Se agregan los vértices centrales de ambas caras "frontales" del polígono
    vertices.append((x, 0, 0))
    vertices.append((-x, 0, 0))

    # Se añaden los vértices subsecuentes en sentido de las manecillas del reloj
    for i in range(sides):
        # Se calculan los catetos del triángulo rectángulo formado por el radio y el ángulo
        z = round(radius * math.cos(angleRadians * i), 4) #adyacente
        y = round(radius * math.sin(angleRadians * i), 4) #opuesto
        
        # Añadir los vértices a la lista
        vertices.append((x, y, z))
        vertices.append((-x, y, z))
    
    return vertices

# Función para calcular las normales y las caras con base en los vértices
def calculate_normals_faces(vertices):
    normals = []
    faces = []

    # Función para calcular las caras con base en el índice actual de los vértices
    def calculate_faces(current, num_vertices, front_index, back_index):
        nonlocal normals, faces
        # Determinar los índices de la primera y segunda cara
        if current != num_vertices:
            first_face = (current + 1, current + 2, current + 4)
            second_face = (current + 1, current + 4, current + 3)
        else:
            first_face = (current + 1, current + 2, back_index)
            second_face = (current + 1, back_index, front_index)

        # Calcular el vector normal de la cara y añadirla a la lista de caras
        normal = calculate_normals(first_face)
        faces.append((first_face, normals.index(normal) + 1))
        faces.append((second_face, normals.index(normal) + 1))

    # Función para calcular las normales con base en los vértices de una cara
    def calculate_normals(face):
        nonlocal normals

        # Obtener los vértices de la cara
        face_vertices = [vertices[vertex - 1] for vertex in face]
        vertex1, vertex2, vertex3 = face_vertices

        # Calcular los vectores de los lados (aristas) de la cara
        edge_vector1 = calculate_edge_vector(vertex1, vertex2)
        edge_vector2 = calculate_edge_vector(vertex1, vertex3)

        # Calcular el producto cruz de los vectores y añadir la normal a la lista
        normal = cross_product(edge_vector1, edge_vector2)
        add_unique_normal(normal)

        return normal

    # Función para calcular el vector de un lado (arista) entre dos vértices
    def calculate_edge_vector(vertex1, vertex2):
        return tuple(v2 - v1 for v1, v2 in zip(vertex1, vertex2))
    
    # Función para añadir una normal a la lista de normales si es única
    def add_unique_normal(normal):
        nonlocal normals
        if normal not in normals:
            normals.append(normal)
    
    # Función para calcular el producto cruz entre dos vectores
    def cross_product(vector1, vector2):
        x1, y1, z1 = vector1
        x2, y2, z2 = vector2

        # Calcular el vector resultante redondeado a 4 decimales
        result_vector = (
            round(y1 * z2 - z1 * y2, 4),
            round(-(x1 * z2 - z1 * x2), 4),
            round(x1 * y2 - y1 * x2, 4))
        
        # Normalizar el vector resultante
        normalized_vector = normalize_vector(result_vector)

        return normalized_vector
    
    # Función para normalizar un vector
    def normalize_vector(vector):

        # Calcular la magnitud del vector
        magnitude = math.sqrt(sum(coordinate**2 for coordinate in vector))
        # Calcular el vector normalizado
        normalized_vector = tuple(round(coordinate / magnitude, 4) for coordinate in vector)

        return normalized_vector
    
    # Inicializar índices para las caras
    num_vertices = len(vertices)
    current_index = 2
    front_index = current_index + 1
    back_index = current_index + 2

    # Iterar sobre los vértices para obtener las caras, saltando los primeros 2 ya que son los centrales
    while current_index < num_vertices:
        if current_index % 2 == 0:
            if current_index + 1 == num_vertices - 1:
                current_face = (1, current_index + 1, front_index)
            else:
                current_face = (1, current_index + 1, current_index + 3)

            calculate_faces(current_index, num_vertices - 2, front_index, back_index)
        else:
            if current_index + 1 == num_vertices:
                current_face = (2, back_index, current_index + 1)
            else:
                current_face = (2, current_index + 3, current_index + 1)

        # Calcular el vector normal de la cara y agreagar la cara a la lista
        normal = calculate_normals(current_face)
        faces.append((current_face, normals.index(normal) + 1))

        current_index += 1

    return normals, faces


#Entradas: número de lados, radio y ancho
num_sides = input("Introduce el número de lados (entre 3 y 360): ")
if num_sides == "" or num_sides == "0":
        num_sides = "8" # Valor por default
        sides = int(num_sides)
else:
    sides = int(num_sides)
    # Validar que el número de lados esté entre 3 y 360
    while ((sides < 3 or sides > 360) and sides != 0):
        print("El número de lados debe estar entre 3 y 360")
        sides = int(input("Introduce el número de lados (entre 3 y 360): "))

str_radius = input("Introduce el radio de la rueda (float): ")
if str_radius == "":
    str_radius = "1.0" # Valor por default
radius = float(str_radius)

str_depth = input("Introduce el ancho de la rueda: ")
if str_depth == "":
    str_depth = "0.5" # Valor por default
depth = float(str_depth)

vertices = calculate_vertices(sides, radius, depth) # Calcular los vértices
normals, faces = calculate_normals_faces(vertices) # Calcular las normales y las caras

# Imprimir los vértices, normales y caras al archivo .obj
folderPath = Path("3DTest/Assets/Models/") # Indicar la ruta de la carpeta donde se encuentra el archivo
filePath = folderPath / "output.obj" # Unir la ruta de carpeta con el nombre del archivo
with open(filePath, "w") as obj_file:
    obj_file.write("# OBJ File\n")
    obj_file.write(f"# Vertices: {len(vertices)}\n") # Escribir los vértices
    for vertex in vertices:
        obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
    obj_file.write(f"# Normals: {len(normals)}\n") # Escribir las normales
    for normal in normals:
        obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
    obj_file.write(f"# Faces: {len(faces)}\n") # Escribir las caras
    for face, normal in faces:
        obj_file.write(f"f {face[0]}//{normal} {face[1]}//{normal} {face[2]}//{normal}\n")
