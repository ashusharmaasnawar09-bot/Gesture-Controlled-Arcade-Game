import cv2
import numpy as np 

image = cv2.imread("assignment_4/opencv.jpeg")
if image is not None:
    print("Image is Loaded")
    
if image is None:
    print("Image is not loaded ")
    exit()
    
choice = input("what function you want to perform")

if choice == "gblur" :
    blurred_image = cv2.GaussianBlur( image , (5,5) , 0)
    cv2.imshow("original image" , image)
    cv2.imshow("blurred_image" , blurred_image )

elif  choice == "mblur" :
    median_blur = cv2.medianBlur( image , 5)
    cv2.imshow("original image" , image)
    cv2.imshow("blurred_image" , median_blur )

elif  choice == "sharpen" :
    sharpened_kernel = np.array([
        [0,-1,0],
        [-1,5,-1],
        [0,-1,0]
    ])
    sharpened_image = cv2.filter2D( image , -1 , sharpened_kernel)
    cv2.imshow("original image" , image)
    cv2.imshow("sharpened Image " , sharpened_image)

else:
    print("give a valid input")
    exit()

cv2.waitKey(0)
cv2.destroyAllWindows()
