import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mpg1')
out = cv2.VideoWriter('Lipnet/evaluation/samples/output.mpg',fourcc, 20.0, (640,480))
#Timer to record only for 3 seconds
start_time=time.time()
while(time.time()-start_time<3):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    cv2.imshow('frame',frame)
    #Save frame to output location
    out.write(frame);
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
