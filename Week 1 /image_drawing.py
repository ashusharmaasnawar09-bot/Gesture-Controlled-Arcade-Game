import cv2
import numpy as np 

image = cv2.imread("Screenshot 2026-06-10 at 5.33.13 PM.png")

if image is None:
     print("Image is not loaded ")

else:

    choice = input("What image drawing you want to do to this image ?")
 
    if choice == "line":
        pt1 = (50,50)
        pt2 = (200,250)
        color = (255,100,100)
        thickness = 4 
        cv2.line( image , pt1 , pt2 , color , thickness )
        cv2.imshow("Adding line to an Image" , image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



    elif choice == "rectangle":
        pt1 = (50,50)
        pt2 = (200,250)
        color = (255,100,100)
        thickness = 4 
        cv2.rectangle( image , pt1 , pt2 , color , thickness )
        cv2.imshow("Adding rectangle to an Image" , image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == "circle":
        center = (150,150)
        radius = 50 
        thickness = 3
        color = (255, 100 , 100)
        cv2.circle( image , center , radius , color  , thickness)
        cv2.imshow("Adding line to an Image" , image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == "text":
        text = input("what text you want to put?")
        org = (100,300)
        fontscale = 1.2
        color = (255 , 100 , 100)
        thickness = 2
        cv2.putText( image , text , org , cv2.FONT_HERSHEY_COMPLEX , fontscale , color , thickness )
        cv2.imshow("Adding line to an Image" , image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

