





using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BasicLerp : MonoBehaviour
{
    [SerializeField] Vector3 startPos;
    [SerializeField] Vector3 endPos;

    [Range (0.0f, 1.0f)]
    [SerializeField] float t;
    [SerializeField] float moveTime;
    float elapsedTime = 0.0f;

    void Start()
    {
        transform.position = startPos;
    }

    void Update()
    {
        t = elapsedTime / moveTime;

        //Use a function to smooth the movement
        t = t * t * (3.0f - 2.0f * t);

        Vector3 position = startPos + (endPos - startPos) * t;

        //Move the object using the Unity transforms
        transform.position = position;

        Matrix4x4 move = HW_Transforms.TranslationMat(position.x, position.y, position.z);

        elapsedTime += Time.deltaTime;

        if (elapsedTime > moveTime)
        {
            //elapsedTime = moveTime;
            elapsedTime = 0.0f;

            Vector3 temp = endPos;
            endPos = startPos;
            startPos = temp;
        }
    }

}