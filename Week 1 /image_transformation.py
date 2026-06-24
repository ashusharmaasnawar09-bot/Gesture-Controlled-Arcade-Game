import cv2

image = cv2.imread("input.jpg")

resized = cv2.resize(image, (300, 300)) 
cropped = image[100:300, 50:250]  

(h, w) = image.shape[:2]
center = (w // 2, h // 2)

angle = 45  
scale = 1.0

M = cv2.getRotationMatrix2D(center, angle, scale)
rotated = cv2.warpAffine(image, M, (w, h))

flipped = cv2.flip(image, 1)


cv2.imshow("Original", image)
cv2.imshow("Resized", resized)
cv2.imshow("Cropped", cropped)
cv2.imshow("Rotated", rotated)
cv2.imshow("Flipped", flipped)

cv2.waitKey(0)
cv2.destroyAllWindows()
