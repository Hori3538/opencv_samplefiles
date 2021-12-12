import cv2
import numpy as np

cap = cv2.VideoCapture('data/campus.mp4')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
dst_float = np.ones((height, width, 3), np.float32) * 0.5

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    src_float = src.astype(np.float32) / 255.0
    #  重みづけ平均
    dst_float = (dst_float * 0.99) + (src_float * 0.01)
    # 差分の絶対値の計算
    diff_float = cv2.absdiff(src_float, dst_float)
    diff = (diff_float * 255).astype(np.uint8)
    # ネガポジ反転
    diff_inv = cv2.bitwise_not(diff)
    
    cv2.imshow('win_src', src)
    cv2.imshow('win_dst_float', dst_float)
    cv2.imshow('win_diff_float', diff_float)
    cv2.imshow('win_diff_inv', diff_inv)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
