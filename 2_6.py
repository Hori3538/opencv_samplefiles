import sys
import cv2

# カメラを開く
cap = cv2.VideoCapture(0)
# カメラが開けなかったとき
if not cap.isOpened():
    print('Can not open camera')
    sys.exit()
# 表示ウィンドウの作成
cv2.namedWindow('win_dst', cv2.WINDOW_NORMAL)
# ウィンドウサイズを変更
cv2.resizeWindow('win_dst', 800, 600)

# ループ開始
while True:
    # 1フレーム読み込み
    ret, src = cap.read()
    # カメラからフレームが読み込めなかったら中断
    if not ret:
        break

    dst = cv2.flip(src, 1)                # 左右反転
    # dst = cv2.stylization(src)            # イラスト風
    # gray, dst = cv2.pencilSketch(src)     # 鉛筆画風

    # 入力と出力を1フレーム表示
    cv2.imshow('win_src', src)
    cv2.imshow('win_dst', dst)
    if cv2.waitKey(10) == 27:
        break

cv2.destroyAllWindows()
# カメラを閉じる
cap.release()
