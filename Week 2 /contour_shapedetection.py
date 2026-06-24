import cv2

# Read Image
img = cv2.imread("Contour & Shape Detection/circle.png")

# Convert to Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Binary Threshold
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Find Contours
contours, hierarchy = cv2.findContours(
thresh,
cv2.RETR_TREE,
cv2.CHAIN_APPROX_SIMPLE
)

# Draw all contours
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

for contour in contours:

# Approximate contour
approx = cv2.approxPolyDP(
contour,
0.01 * cv2.arcLength(contour, True),
True
)

corners = len(approx)

if corners == 3:
shape_name = "Triangle"

elif corners == 4:
shape_name = "Rectangle"

elif corners == 5:
shape_name = "Pentagon"

elif corners > 5:
shape_name = "Circle"

else:
shape_name = "Unknown"

# Draw approximated contour
cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)

# Get first vertex coordinates
x = approx.ravel()[0]
y = approx.ravel()[1] - 10

# Put shape name
cv2.putText(
img,
shape_name,
(x, y),
cv2.FONT_HERSHEY_COMPLEX,
0.6,
(0, 0, 255),
2
)

cv2.imshow("Contours", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
