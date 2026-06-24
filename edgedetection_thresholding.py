import cv2

# Read image in grayscale
img = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Image not found")
    exit()

# Thresholding

ret, thresh = cv2.threshold(
    img,
    120,
    255,
    cv2.THRESH_BINARY
)

# Canny Edge Detection

edges = cv2.Canny(
    img,
    100,
    200
)

# Bitwise Operations


# AND
bit_and = cv2.bitwise_and(thresh, edges)

# OR
bit_or = cv2.bitwise_or(thresh, edges)

# NOT
bit_not = cv2.bitwise_not(thresh)


cv2.imshow("Original Image", img)
cv2.imshow("Thresholded Image", thresh)
cv2.imshow("Canny Edges", edges)

cv2.imshow("Bitwise AND", bit_and)
cv2.imshow("Bitwise OR", bit_or)
cv2.imshow("Bitwise NOT", bit_not)

cv2.waitKey(0)
cv2.destroyAllWindows()
