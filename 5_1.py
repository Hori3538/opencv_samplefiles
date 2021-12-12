import cv2
import numpy as np

src = cv2.imread('data/fruits.png')
width, height = src.shape[1], src.shape[0]
dst = np.ones((height, width, 3), np.uint8) * 128

for y in range(8, height, 16):
    for x in range(8, width, 16):
        #  ピクセル値取得
        b = src[y, x, 0]
        g = src[y, x, 1]
        r = src[y, x, 2]
        cv2.circle(dst, (x+4, y+3), b // 50, (255, 0, 0), -1)  # 青点
        cv2.circle(dst, (x-4, y+3), g // 50, (0, 255, 0), -1)  # 緑点
        cv2.circle(dst, (x,   y-3), r // 50, (0, 0, 255), -1)  # 赤点

cv2.imshow('win_src', src)
cv2.imshow('win_dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
