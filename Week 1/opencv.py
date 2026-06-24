import cv2
import numpy as np

image = cv2.imread("iitb.jpeg")

choice = input("what function you want to do with this image ?")



if choice == "show":
    cv2.imshow("IIT BOMBAY",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
elif choice == "gray":
    gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray iit bombay" , gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
elif choice == "save":
    cv2.imwrite("saved_image.jpeg" , image)


