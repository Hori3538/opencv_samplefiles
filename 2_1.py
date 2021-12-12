import sys
import cv2

# 画像ファイルの読み込み
img = cv2.imread('data/fruits.png')

# 画像ファイルが読み込めなかったとき
if img is None:
    sys.exit('Can not read image')

# 表示ウィンドウに画像を表示
cv2.imshow('win_img', img)

# キー入力待機
cv2.waitKey(0)

# 表示ウィンドウを削除
cv2.destroyWindow('win_img')
