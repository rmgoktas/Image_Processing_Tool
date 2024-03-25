from adaptive_threshold import threshold
import cv2

img1=cv2.imread("cameraman.png")
gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

thres=threshold(gray,255,2,3)
adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3,0)
cv2.imshow("thres",thres)
cv2.imshow("adaptive",adaptive_threshold)









cv2.waitKey(0)
cv2.destroyAllWindows()

