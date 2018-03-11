#takes image from webcam and detects movement
#when it sees movement it sends a windows 10 toast message
#uses cv2 and win10toast libraries

import cv2
from win10toast import ToastNotifier


def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

toaster = ToastNotifier() 
cam = cv2.VideoCapture(0)

#The threshold may need adjusting to suit your webcam
threshold = 140500
winName = "Movement Detector"
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
 
# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
last_capture = False
movement = False

while True:
    last_capture = movement
    movement = False
    
    #displaying output
    cv2.imshow( winName, diffImg(t_minus, t, t_plus) )
  
    if cv2.countNonZero(diffImg(t_minus, t, t_plus)) > threshold:
        movement = True
    else:
        print("false")

    # Read next image
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    #escape key
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break

    if movement == True:
        if last_capture == True:
            pass
        else:
            toaster.show_toast("Someone is at your door", "You may want to check it!")
 
print("Goodbye")
