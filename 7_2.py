import cv2
import numpy as np


def hist_2d(src):
    """ 2次元ヒストグラム取得 """
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist(
        [hsv], [0, 1], None, [45, 64], [0, 180, 0, 256])
    # ヒストグラム高さ正規化 (0.0～1.0)
    hist = hist / float(src.shape[1] * src.shape[0])
    return hist


cap = cv2.VideoCapture('data/sample3.mp4')
hist_targets = {
    'chipmunk': hist_2d(cv2.imread('data/chipmunk.jpg')),
    'duckling': hist_2d(cv2.imread('data/duckling.jpg'))
}

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    # 入力フレームの2次元ヒストグラム取得
    hist_src = hist_2d(src)
    # 対象物体2種類
    for name, hist in hist_targets.items():
        # 対象と入力のヒストグラムの類似度計算
        similarity = cv2.compareHist(hist, hist_src, cv2.HISTCMP_INTERSECT)
        if similarity > 0.7:
            # 類似度が0.7より大きければ'Detect'と名前表示
            cv2.putText(src, 'Detect: ' + name, (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5, (0, 0, 0), 4)
    cv2.imshow('win_src', src)
    # 類似度マップを拡大して表示
    img_hist = cv2.resize(
        hist_src*30000, (64*4, 45*4),
        interpolation=cv2.INTER_AREA)
    cv2.imshow('win_hist', img_hist)
    key = cv2.waitKey(2000)
    if key == 27:
        break
    elif key == 32:
        cv2.waitKey()

cv2.destroyAllWindows()
