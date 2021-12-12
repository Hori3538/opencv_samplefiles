import cv2

# クラス名
class_names = ['apple', 'ballpoint pen', 'laptop computer']
# ネットワークの構造と重みを読み込む
net = cv2.dnn.readNet('model/imagenet_model.pb')

cap = cv2.VideoCapture('data/apple_pen.mp4')

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # 画像をblobに変換
    blob = cv2.dnn.blobFromImage(img, 1/255, size=(28, 28))
    # blobを入力層にセット
    net.setInput(blob)
    # 入力に対する出力を計算
    pred = net.forward()
    # 出力の最大値を求める
    _, max_val, _, max_loc = cv2.minMaxLoc(pred)
    # 推定したクラス名を描画
    cv2.rectangle(src, (0, 0), (320, 40), (255, 255, 255), -1) 
    cv2.putText(src, class_names[max_loc[0]], (5, 30),
                cv2.FONT_HERSHEY_TRIPLEX, 1, 0, 1)
    cv2.imshow('win_src', src)
    key = cv2.waitKey(30)
    if key == 27:
        break

cv2.destroyAllWindows()
