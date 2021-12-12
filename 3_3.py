import cv2
import numpy as np

# 明るさ調節のコールバック関数
brightness = 1.0
def brightness_cb(position):
    global brightness
    # 明るさ倍率計算
    brightness = position / 100.0

# コントラスト調整のコールバック関数
def nothing(x):
    pass


cap = cv2.VideoCapture('data/campus.mp4')
winname = 'Window'
cv2.namedWindow(winname)

#  トラックバー生成
cv2.createTrackbar('brightness', winname, 100, 200, brightness_cb)
cv2.createTrackbar('contrast', winname, 0, 100, nothing)

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # ビデオ繰り返し
        continue
    dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # 明るさ変換（brightnessはコールバック関数から）
    dst = cv2.multiply(dst, brightness)

    # 値を取得してコントラスト調整
    contrast = cv2.getTrackbarPos('contrast', winname)
    dst = (dst * (255.0 - contrast*2)/255.0 + contrast).astype(np.uint8)

    cv2.imshow(winname, dst)
    if cv2.waitKey(30) == 27:
        break

cv2.destroyWindow(winname)
