import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture("/dev/video2")

TARGET_SIZE = (640,360)

while(True):
    ret,im = cap.read()
    im_resized = cv2.resize(im, TARGET_SIZE)
    im_flipped = cv2.flip(im_resized, 1)    

    mask = cv2.inRange(im_flipped,(0,0,0),(80,80,80))
    cv2.imshow('mask', mask)
    cv2.moveWindow('mask',TARGET_SIZE[0],0)

    #print(np.sum(mask/255))

    # if(np.sum(mask/255) > 10000):
    if(np.sum(mask/255) > 0.45*im_flipped.shape[0]*im_flipped.shape[1]):
        cv2.putText(im_flipped,'Black',(50,100),
                    fontFace = cv2.FONT_HERSHEY_PLAIN,
                    fontScale = 5,
                    thickness = 3,
                    color = (0,0,255))         

    cv2.imshow('camera', im_flipped)
    cv2.moveWindow('camera',0,0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()