import cv2
import numpy as np

cap = cv2.VideoCapture('data/duck_greenback.mp4')
back = cv2.resize(cv2.imread('data/book.png'),
                  (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
kernel = np.ones((7, 7), np.uint8)

#  色相範囲ウィンドウと色相環の生成
img_hue1 = np.zeros((300, 300, 3), np.uint8)
for h in range(0, 180):
    cv2.ellipse(img_hue1, (150, 150), (120, 120), -90,
                2*h, 2*h+2, (h, 255, 255), -1)
img_hue1 = cv2.cvtColor(img_hue1, cv2.COLOR_HSV2BGR)


def nothing(x):
    pass


cv2.namedWindow('win_hue')
cv2.createTrackbar('h_min', 'win_hue', 30, 180, nothing)
cv2.createTrackbar('h_max', 'win_hue', 110, 180, nothing)

while True:
    ret, src = cap.read()  # 前景（アヒル）
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    [h_min, h_max] = list(sorted([cv2.getTrackbarPos('h_min', 'win_hue'),
                                  cv2.getTrackbarPos('h_max', 'win_hue')]))
    
    # BGRからHSVに変換し、1チャンネルに分離
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h1, s1, v1 = cv2.split(hsv)
    # 色相Hからマスク生成
    mask = cv2.inRange(h1, h_min, h_max)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2) / 255.0
    # マスクを使った画像合成
    dst = back * mask + src * (1.0 - mask)
    dst = dst.astype(np.uint8)
    # 色相環と範囲の描画
    img_hue2 = img_hue1.copy()
    cv2.ellipse(img_hue2, (150, 150), (130, 130), -90,
                2 * h_min, 2 * h_max + 2, (255, 255, 255), 16)

    cv2.imshow('win_hue', img_hue2)
    cv2.imshow('win_mask', mask)
    cv2.imshow('win_dst', dst)
    if cv2.waitKey(10) == 27:
        break

cv2.destroyAllWindows()
