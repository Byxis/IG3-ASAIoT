import cv2
import numpy as np

HEIGHT, WIDTH = 500, 500  
RADIUS = 50  
PERIOD = 30
waste_img = cv2.imread('img.png')
def update_pos(x, y, x_step, y_step):
    if x + RADIUS + x_step < WIDTH:
        x += x_step
    if y + RADIUS + y_step < HEIGHT:
        y += y_step

    return x, y, x_step, y_step

canevas = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255
center_x, center_y = 312, 82 
x_step, y_step = 0, 10
rows,cols,channels = waste_img.shape
waste_img = cv2.resize(waste_img, (RADIUS*2, RADIUS*2))


import cv2
camera = cv2.VideoCapture(0)
if(not(camera.isOpened())):
    print("Impossible d'ouvrir la webcam.")
    exit()

while(True):
    # Capture frame-by-frame
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)
    if(not(ret)):
        print("Impossible de recevoir une nouvelle frame. Quitte...")
        break
    if (center_x + RADIUS) <= WIDTH- 10 and (center_y + RADIUS) <= HEIGHT - 10:
        frame[center_y:center_y+RADIUS*2, center_x:center_x+RADIUS*2] = waste_img
        center_x, center_y, x_step, y_step = update_pos(center_x, center_y, x_step, y_step)

    cv2.imshow('frame', frame)
    if(cv2.waitKey(1) == ord('q')):
        break
# When everything done, release the capture
camera.release()


cv2.destroyAllWindows()
