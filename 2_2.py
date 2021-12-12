import cv2

src = cv2.imread('data/fruits.png')

# Cannyエッジ検出
dst = cv2.Canny(src, 50, 150)

cv2.imshow('win_src', src)
cv2.imshow('win_dst', dst)

# 出力画像の保存
cv2.imwrite('data/image_dst.jpg', dst)

cv2.waitKey(0)

# すべての表示ウィンドウを削除
cv2.destroyAllWindows()
