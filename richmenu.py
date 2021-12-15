import cv2
import numpy as np
size = (405,1200)
img = np.ones(size,np.uint8)
for i in range(size[0]):
    for j in range(size[1]):
        img[i][j] = 255
        
for i in range(size[0]):
    for j in range(size[1]):
        if i > size[0] // 2:
            if (j < size[1] // 3) or (j > (size[1]*2) // 3):
                img[i][j] = 0
        else:
            if (j > size[1] // 3) and (j < (size[1]*2) // 3):
                img[i][j] = 0
            
cv2.imwrite("richmenu2.jpeg",img)
cv2.waitKey(0)