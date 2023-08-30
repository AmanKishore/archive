import cv2
import numpy as np
import os
import sys

# img_path = sys.argv[1]

# name, ext = os.path.splitext(img_path)

# img = cv2.imread(img_path)
# # cv2.imshow('Test',img)
# # if cv2.waitKey(0) & 0xff == 27:
# #     cv2.destroyAllWindows()
# #Edges
# grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# grey = cv2.medianBlur(grey, 5)
# edges = cv2.adaptiveThreshold(grey, 255,
# 		cv2.ADAPTIVE_THRESH_MEAN_C,
# 		cv2.THRESH_BINARY, 11, 11)

# # Cartoon
# color = cv2.bilateralFilter(img, 9, 250, 250)
# cartoon = cv2.bitwise_and(color, color, mask=edges)

# cv2.imwrite(f"{name}_cartoon{ext}", cartoon)

import cv2
import numpy as np
img1 = cv2.imread('selena.jpg')
img2 = cv2.imread('selena_cartoon.jpg')
vis = np.concatenate((img1, img2), axis=1)
cv2.imwrite('selena.png', vis)