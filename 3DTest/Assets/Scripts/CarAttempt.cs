// Desplazar coche hacia una dirección dada mientras se desplazan y giran las ruedas
// Valeria Martínez Martínez - A01782413
// 2023/12/01

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarAttempt : MonoBehaviour
{
    // Field para ingresar las coordenadas de desplazamiento del automóvil
    [SerializeField] Vector3 displacement;

    // Field para ingresar el ángulo de rotación
    [SerializeField] float rotationAngle;

    // Ángulo actual
    float angle;

    // Campo para poder asignar qué objeto se va a usar como rueda
    public GameObject wheelPrefab;

    Mesh mesh;

    // Vértices para el movimiento
    Vector3[] newVertices;
    Vector3[] baseVertices;

    Mesh[] wheelMeshes = new Mesh[4];
    Vector3[][] wheelBaseVertices = new Vector3[4][];
    Vector3[][] wheelNewVertices = new Vector3[4][];

    // Crear 4 GameObjects para las ruedas
    GameObject[] wheels = new GameObject[4];

    // Field para ingresar las posiciones de las ruedas respecto al coche
    [SerializeField] Vector3[] wheelPositions;

    void Start()
    {
        // Creación de las ruedas con base en el prefab
        for (int i = 0; i < wheels.Length; i++)
        {
            wheels[i] = Instantiate(wheelPrefab, Vector3.zero, Quaternion.identity);
        }

        // Obtener la mesh del coche
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        // Obtener los vértices base del coche
        baseVertices = mesh.vertices;

        // Se crea una copia de los vértices base
        newVertices = new Vector3[baseVertices.Length];
        for (int i = 0; i < baseVertices.Length; i++)
        {
            newVertices[i] = baseVertices[i];
        }

        // Se obtienen las meshes y los vértices base para cada una de las ruedas
        for (int i = 0; i < 4; i++)
        {
            wheelMeshes[i] = wheels[i].GetComponentInChildren<MeshFilter>().mesh;
            wheelBaseVertices[i] = wheelMeshes[i].vertices;
        }
        
        // Se crea una copia de los vértices base para cada una de las ruedas
        for (int i = 0; i < 4; i++)
        {
            wheelNewVertices[i] = new Vector3[wheelBaseVertices[i].Length];
            for (int j = 0; j < 4; j++)
            {
                wheelNewVertices[i][j] = wheelBaseVertices[i][j];
            }
        }
    }

    void Update()
    {
        DoTransform();
    }

    void DoTransform()
    {
        // Cálculo del ángulo de rotación basado en el desplazamiento
        angle = Mathf.Atan2(displacement.x, displacement.z) * Mathf.Rad2Deg;

        // Matrices de transformación
        Matrix4x4 translation = HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle, AXIS.Y);

        // Combinación de las matrices para simular ambas partes del movimiento
        Matrix4x4 composite = translation * rotate;

        // Ciclo para el movimiento del automóvil
        for (int i = 0; i < newVertices.Length; i++)
        {
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            newVertices[i] = composite * temp;
        }

        // Se actualizan los vértices del auto y se recalculan las normales
        mesh.vertices = newVertices;
        mesh.RecalculateNormals();

        // Matriz de rotación para las ruedas
        Matrix4x4 rotateWheel = HW_Transforms.RotateMat(rotationAngle * Time.time, AXIS.X);

        // Ciclo para el movimiento de las ruedas
        for (int i = 0; i < 4; i++)
        {
            Matrix4x4 wheelTranslation = HW_Transforms.TranslationMat(wheelPositions[i].x, wheelPositions[i].y, wheelPositions[i].z);
            Matrix4x4 wheelComposite = composite * wheelTranslation * rotateWheel;

            // Transformación de los vértices de cada rueda
            for (int j = 0; j < wheelNewVertices[i].Length; j++)
            {
                Vector4 temp = new Vector4(wheelBaseVertices[i][j].x, wheelBaseVertices[i][j].y, wheelBaseVertices[i][j].z, 1);
                wheelNewVertices[i][j] = wheelComposite * temp;
            }
            
            // Se actualizan los vértices y se recalculan las normales para cada rueda
            wheelMeshes[i].vertices = wheelNewVertices[i];
            wheelMeshes[i].RecalculateNormals();
        }
    }
}
