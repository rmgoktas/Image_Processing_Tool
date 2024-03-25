from image_operations import multiplication
import cv2

img1=cv2.imread("peppers.jpeg")
img2=cv2.imread("peppers.jpeg")

mul=multiplication(img1,img2)

cv2.imshow("multiplaticion",mul)











cv2.waitKey(0)
cv2.destroyAllWindows()

