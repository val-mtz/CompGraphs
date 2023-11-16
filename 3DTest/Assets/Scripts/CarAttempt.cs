using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarAttempt : MonoBehaviour
{
    [SerializeField] Vector3 displacement;
    [SerializeField] float rotationAngle;
    float angle;
    public GameObject wheelPrefab;

    Mesh mesh;

    Vector3[] newVertices;
    Vector3[] baseVertices;

    Mesh[] wheelMeshes = new Mesh[4];

    Vector3[][] wheelBaseVertices = new Vector3[4][];
    Vector3[][] wheelNewVertices = new Vector3[4][];
    
    GameObject[] wheels = new GameObject[4];

    [SerializeField] Vector3[] wheelPositions;

    void Start()
    {
        for(int i = 0; i < wheels.Length; i++)
        {
            wheels[i] = Instantiate(wheelPrefab, Vector3.zero, Quaternion.identity);
        }

        mesh = GetComponentInChildren<MeshFilter>().mesh;

        baseVertices = mesh.vertices;

        newVertices = new Vector3[baseVertices.Length];
        for (int i = 0; i < baseVertices.Length; i++)
        {
            newVertices[i] = baseVertices[i];
        }

        for (int i = 0; i < 4; i++)
        {
            wheelMeshes[i] = wheels[i].GetComponentInChildren<MeshFilter>().mesh;
            wheelBaseVertices[i] = wheelMeshes[i].vertices;
        }

        for (int i = 0; i < 4; i++)
        {
            wheelNewVertices[i] = new Vector3[wheelBaseVertices[i].Length];
            for(int j = 0; j < 4; j++)
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
        angle = Mathf.Atan2(displacement.x, displacement.z) * Mathf.Rad2Deg;

        Matrix4x4 translation = HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);
        Matrix4x4 moveOrigin = HW_Transforms.TranslationMat(-displacement.x, -displacement.y, -displacement.z);
        Matrix4x4 moveObject = HW_Transforms.TranslationMat(displacement.x, displacement.y, displacement.z);
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle, AXIS.Y);

        Matrix4x4 composite = translation * rotate;

        for (int i = 0; i < newVertices.Length; i++)
        {
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            newVertices[i] = composite * temp;
        }

        mesh.vertices = newVertices;
        mesh.RecalculateNormals();

        Matrix4x4 rotateWheel = HW_Transforms.RotateMat(rotationAngle, AXIS.X);

        for (int i = 0; i < 4; i++)
        {
            Matrix4x4 wheelTranslation = HW_Transforms.TranslationMat(wheelPositions[i].x, wheelPositions[i].y, wheelPositions[i].z);
            Matrix4x4 wheelComposite = composite * wheelTranslation * rotateWheel;

            for (int j = 0; j < wheelNewVertices[i].Length; j++)
            {
                Vector4 temp = new Vector4(wheelBaseVertices[i][j].x, wheelBaseVertices[i][j].y, wheelBaseVertices[i][j].z, 1);
                wheelNewVertices[i][j] = wheelComposite * temp;
            }

            wheelMeshes[i].vertices = wheelNewVertices[i];
            wheelMeshes[i].RecalculateNormals();
        }
    }
}
