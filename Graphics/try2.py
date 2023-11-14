import math
import sys

# Genera un archivo .obj que representa una rueda
def generarueda(num_lados, rad, ancho):
    # Validar los parámetros
    if num_lados < 3 or num_lados > 360:
        print("El número de lados debe estar entre 3 y 360")
        return

    # Generar los arreglos de vértices y caras
    vertices = []
    normals = []
    faces = []

    # Vértices
    for i in range(num_lados):
        # Calcular las coordenadas de los vértices
        angle = 2 * math.pi * i / num_lados
        x = rad * math.cos(angle)
        y = rad * math.sin(angle)
        z = 0  # En el plano XY
        # Agregar los vértices
        vertices.append((x, y, 0))
        # Calcular las normales de los vértices
        normal = (x, y, z)
        # Normalizar la normal dividiendo por su longitud
        length = math.sqrt(normal[0] * 2 + normal[1] * 2 + normal[2] ** 2)
        normal = (normal[0] / length, normal[1] / length, normal[2] / length)
        normals.append(normal)
        # Este vértice es el mismo pero con el ancho especificado
        vertices.append((x, y, ancho))

    # Caras
    for i in range(num_lados):
        # j sirve para obtener el vértice siguiente
        j = (i + 1) % num_lados
        # Caras laterales
        faces.append((i * 2, j * 2, j * 2 + 1))
        faces.append((j * 2 + 1, i * 2 + 1, i * 2))
        # Caras superior e inferior
        faces.append((i * 2 + 1, j * 2 + 1, 1))
        faces.append((j * 2, i * 2, 0))

    # Escribir el archivo
    with open("wheel.obj", "w") as obj_file:
        # Escribir los vértices y las caras con normales
        for i, vertex in enumerate(vertices):
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for i, normal in enumerate(normals):
            obj_file.write(f"vn {normals[i][0]} {normals[i][1]} {normals[i][2]}\n")
        for face in faces:
            obj_file.write(f"f {face[0] + 1}//{face[0] + 1} {face[1] + 1}//{face[1] + 1} {face[2] + 1}//{face[2] + 1}\n")

# Si se ejecuta este archivo directamente, generar una rueda con los parámetros
if __name__ == "_main_":
    num_lados = 8
    rad = 1.0
    ancho = 0.5

    # Si se especifican parámetros, usarlos
    if len(sys.argv) > 1:
        try:
            num_lados = int(sys.argv[1])
            rad = float(sys.argv[2])
            ancho = float(sys.argv[3])
        except (ValueError, IndexError):
            pass

    generarueda(num_lados, rad, ancho)