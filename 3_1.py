import cv2
import numpy as np

# 色の設定
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
gray = (128, 128, 128)
dgray = (32, 32, 32)
# 初期化されていない画像を用意し、白で塗りつぶす
img = np.empty((480, 640, 3), np.uint8)
img.fill(255)
# 直線と矢印
cv2.line(img, (50, 50), (150, 150), blue, 8, cv2.LINE_AA)
cv2.arrowedLine(img, (50, 250), (150, 200),
                red, 8, cv2.LINE_4, 0, 0.3)
# 破線の格子目盛
for lx in range(50, 640, 50):
    for ly in range(0, 480, 15):
        cv2.line(img, (lx, ly), (lx, ly + 10), gray)
for ly in range(50, 480, 50):
    for lx in range(0, 640, 15):
        cv2.line(img, (lx, ly), (lx + 10, ly), gray)
# 長方形_1
cv2.rectangle(img, (200, 100), (300, 250), dgray, cv2.FILLED)
# 長方形_2
p1 = (250, 50)
p2 = (325, 150)
cv2.rectangle(img, p1, p2, green, 16)
# 多角形_1 (5角形の内部塗りつぶし）
points = np.array([[400, 100], [475, 150], [400, 250],
                   [350, 200], [350, 150]], np.int32)
cv2.fillConvexPoly(img, points, (200, 0, 0))
# 多角形_2 (3角形の枠線のみ)
poly = np.array([[130, 280], [550, 200], [420, 450]], np.int32)
cv2.polylines(img, [poly], True, (0, 200, 255), 5)
# 円と楕円
cv2.circle(img, (550, 200), 50, red, 5)
cv2.ellipse(img, (550, 100), (60, 30),
            30, 90, 360, green, cv2.FILLED)
# 文字
cv2.putText(img, 'Hello World', (50, 400),
            cv2.FONT_HERSHEY_SIMPLEX, 2, blue, 4)

cv2.imshow('win_img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
