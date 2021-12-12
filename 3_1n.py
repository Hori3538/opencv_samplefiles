import cv2
import numpy as np

fonts = list(filter(lambda c: c.startswith('FONT_'), list(cv2.__dict__.keys())))

height = 100
margin = 40
size = (len(fonts)*height + margin, 480)
img = np.empty((*size, 3), np.uint8)
img.fill(255)

opencv = 'OpenCV'
color = (0, 0, 0)
xpos1 = 10
xpos2 = 100
ypos = height
scale = 2
thickness = 4

for idx, f in enumerate(fonts):
    fid = int(cv2.__dict__[f])
    cv2.putText(img, str(idx), (xpos1, ypos), fid, scale, color, thickness)
    cv2.putText(img, opencv, (xpos2, ypos), fid, scale, color, thickness)
    ypos += height
    print(f, fid)

cv2.imshow('win_img', img)
cv2.waitKey(0)

cv2.destroyAllWindows()
