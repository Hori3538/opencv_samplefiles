import cv2
import numpy as np


def nothing(x):
    pass


file = 'data/sample1.mp4'
win_name = 'Floating'
bar_normalize = 'normalize'

cap = cv2.VideoCapture(file)
cv2.namedWindow(win_name)
cv2.createTrackbar(bar_normalize, win_name, 100, 200, nothing)

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    factor = cv2.getTrackbarPos(bar_normalize, win_name)
    factor = factor / 100.0                        # スケーリング[0, 2]

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)   # グレースケール[0, 255]
    gray = gray.astype(np.float32) / 255.0         # 浮動小数点数化[0, 1]
    norm = cv2.normalize(                          # 正規化[0, 2]
        gray, None, 0.0, factor, cv2.NORM_MINMAX)

    cv2.putText(norm, '{:1.3f}'.format(factor), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, 0 if cv2.mean(norm)[0] > 0.5 else 1)

    cv2.imshow(win_name, norm)
    if cv2.waitKey(30) == 27:
        break

cv2.destroyWindow(win_name)
