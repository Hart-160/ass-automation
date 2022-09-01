import cv2
import numpy as np

#vid = 'C:\\Users\\roma\\Documents\\D4DJ Unpack\\tbk\\test.mp4'
pic = 'test.png'

img = cv2.imread(pic)
cv2.namedWindow('Track')
cv2.resizeWindow('Track',640, 400)

def empty(v):
    pass

cv2.createTrackbar('Hue Min', 'Track', 0, 179, empty)
cv2.createTrackbar('Hue Max', 'Track', 179, 179, empty)
cv2.createTrackbar('Sat Min', 'Track', 0, 255, empty)
cv2.createTrackbar('Sat Max', 'Track', 255, 255, empty)
cv2.createTrackbar('Val Min', 'Track', 0, 255, empty)
cv2.createTrackbar('Val Max', 'Track', 255, 255, empty)

def get_mask():
    h_min = cv2.getTrackbarPos('Hue Min', 'Track')
    h_max = cv2.getTrackbarPos('Hue Max', 'Track')
    s_min = cv2.getTrackbarPos('Sat Min', 'Track')
    s_max = cv2.getTrackbarPos('Sat Max', 'Track')
    v_min = cv2.getTrackbarPos('Val Min', 'Track')
    v_max = cv2.getTrackbarPos('Val Max', 'Track')
    
    #print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    return lower, upper

#cap = cv2.VideoCapture(vid)
#success, frame = cap.read()
success = True
while success:
    frame = cv2.resize(img, (0,0),fx=0.3, fy=0.3)
    fhsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    lower, upper = get_mask()
    mask = cv2.inRange(fhsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Result', result)
    #cv2.imshow('Test', frame)
    cv2.waitKey(1)
    #success, frame = cap.read()

#cv2.destroyAllWindows()
#cap.release()