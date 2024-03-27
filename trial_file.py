from blurring import box_blurring
import cv2

img1=cv2.imread("cameraman.png")
gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)


blurimg=box_blurring(gray,3)


cv2.imshow("blur",blurimg)

cv2.waitKey(0)
cv2.destroyAllWindows()

