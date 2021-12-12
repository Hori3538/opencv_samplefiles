import cv2
import numpy as np

cap = cv2.VideoCapture('data/sample2.mp4')
dst = np.empty((256, 256, 3), np.uint8)
color = ((255, 0, 0), (0, 255, 0), (0, 0, 255))

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    dst.fill(255)
    for channel in range(3):
        # ヒストグラムを計算
        hist = cv2.calcHist([src], [channel], None, [256], [0, 256])
        # 折れ線の開始座標（左下）
        prev_xy = (0, 255)
        for x in range(256):
            # 現在座標
            current_xy = (x, 255 - int(hist[x] / 50))
            # 前座標と現在座標を結ぶ
            cv2.line(dst, prev_xy, current_xy, color[channel])
            # 現在座標を前座標に保存
            prev_xy = current_xy
    cv2.imshow('win_src', src)
    cv2.imshow('win_dst', dst)
    if cv2.waitKey(10) == 27:
        break

cv2.destroyAllWindows()
