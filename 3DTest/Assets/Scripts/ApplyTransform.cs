using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyTransforms : MonoBehaviour 
{
    [SerializeField] Vector3 displacement;
    [SerializeField] float angle;
    [SerializeField] AXIS rotationAxis;

    Mesh mesh; // Mesh is a class in Unity that stores the vertex data of a 3D object (vertices, normals, triangles, etc.)
    Vector3[] baseVertices;
    Vector3[] newVertices;

    //Start is called before the first frame update
    void Start()
    {
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        baseVertices = mesh.vertices;

        // Allocate memory for the copy of the vertex array
        newVertices = new Vector3[baseVertices.Length];
        // Copy the vertex array (coordinates)
        for (int i = 0; i < baseVertices.Length; i++)
        {
            newVertices[i] = baseVertices[i];
        }

        doTransform();

    }

    void Update()
    {
        doTransform();
    }

    void doTransform()
    {
        //Time.deltatime is to move the object at a constant speed regardless of the frame rate
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time, 
                                                      displacement.y * Time.time, 
                                                      displacement.z * Time.time);

        Matrix4x4 moveOrigin = HW_Transforms.TranslationMat(-displacement.x, 
                                                            -displacement.y, 
                                                            -displacement.z);
        
        Matrix4x4 moveObject = HW_Transforms.TranslationMat(displacement.x, 
                                                            displacement.y, 
                                                            displacement.z);

        Matrix4x4 rotate = HW_Transforms.RotateMat(angle * Time.time, rotationAxis);

        //Matrix4x4 composite = moveObject * rotate * moveOrigin;
        Matrix4x4 composite = move * rotate;

        for (int i = 0; i < newVertices.Length; i++)
        {
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1.0f);
            newVertices[i] = composite * temp;
        }

        // Assign the new vertices to the matrix 
        mesh.vertices = newVertices;
        mesh.RecalculateNormals();
    }
}