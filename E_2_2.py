import cv2
import numpy as np


def on_mouse(event, x, y, flags, param):
    """ マウス描画関数 """
    if flags == cv2.EVENT_FLAG_LBUTTON:
        # 左ボタンで描画
        cv2.circle(img, (x, y), 15, 255, -1)
    if event == cv2.EVENT_RBUTTONDOWN:
        # 右ボタンで消去
        img.fill(0)
    # 左上の推定数字の背景を白で塗る
    cv2.rectangle(img, (0, 0), (60, 60), 255, -1)


cv2.namedWindow('win_img')
cv2.setMouseCallback('win_img', on_mouse)
img = np.zeros((300, 300), np.uint8)

# ネットワークの構造と重みファイルを読み込む
net = cv2.dnn.readNet('model/mnist_model.pb')

while True:
    # 画像をblobに変換
    blob = cv2.dnn.blobFromImage(img, 1/255, size=(28, 28))
    # blobを入力層にセット
    net.setInput(blob)
    # 入力に対する出力を計算
    pred = net.forward()
    # 出力の最大値を求める
    _, max_val, _, max_loc = cv2.minMaxLoc(pred)
    # 推定した数字を描画
    cv2.putText(img, str(max_loc[0]), (10, 50),
                cv2.FONT_HERSHEY_TRIPLEX, 2, 0, 2)
    cv2.imshow('win_img', img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
