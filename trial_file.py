from blurring import box_blurring
import cv2

img1=cv2.imread("cameraman.png")



blurimg=box_blurring(img1,3)


cv2.imshow("blur",blurimg)

cv2.waitKey(0)
cv2.destroyAllWindows()


