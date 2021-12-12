import time
import cv2
import numpy as np


def nothing(x):
    pass


cap = cv2.VideoCapture('data/sample1.mp4')
cv2.namedWindow('win_dst')
cv2.createTrackbar('iterate', 'win_dst', 8, 64, nothing)
dst = np.empty((480, 640, 3), np.uint8)

# dilateの注目領域
kernel = np.ones((3, 3), np.uint8)

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # dilate処理の回数の取得
    iterations = cv2.getTrackbarPos('iterate', 'win_dst')

    # dilate処理の計測
    start_time = time.perf_counter()
    dst = cv2.dilate(src, kernel, dst, iterations=iterations)
    duration = (time.perf_counter() - start_time) * (10 ** 6)  # micro-sec

    # 周期 (micro-sec)の表示
    text = '{:>5.0f} us'.format(duration)
    cv2.putText(dst, text, (16, 32), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 0), 2)

    cv2.imshow('win_dst', dst)
    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()


'''  EXAMPLES

#  以下はdilate構造フィルタの例です。
#  dilate構造フィルタ定義の行を置き換えて指定可能です。

kernel = np.array(
    [[0, 0, 0, 1, 0, 0, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [1, 1, 1, 1, 1, 1, 1],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 0],
     [0, 0, 0, 1, 0, 0, 0]], np.uint8)

'''
