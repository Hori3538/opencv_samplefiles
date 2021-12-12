import cv2
import numpy as np
import sys

file = 'data/cars.mp4'
if len(sys.argv) > 1:
    file = sys.argv[1]
cap = cv2.VideoCapture(file)

# ネットワークの構造と重みファイルを読み込む
proto = 'model/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
weight = 'model/frozen_inference_graph.pb'
net = cv2.dnn.readNet(proto, weight)

# クラス名を読み込む
label_file = 'model/object_detection_classes_coco.txt'
class_names = np.loadtxt(label_file, dtype='str', delimiter='\n')

while True:
    ret, src = cap.read()
    if not ret:
        break
    # 画像をblobに変換
    blob = cv2.dnn.blobFromImage(src, size=(300, 300))
    # blobを入力層にセット
    net.setInput(blob)
    # 入力に対する出力を計算
    pred = net.forward()

    # 値を読み込むループ
    for i in range(pred.shape[2]):
        # クラスの信頼度
        conf = pred[0, 0, i, 2]
        if conf > 0.2:
            # 推定された座標に枠を描画
            x0 = int(pred[0, 0, i, 3] * src.shape[1])
            y0 = int(pred[0, 0, i, 4] * src.shape[0])
            x1 = int(pred[0, 0, i, 5] * src.shape[1])
            y1 = int(pred[0, 0, i, 6] * src.shape[0])
            cv2.rectangle(src, (x0, y0), (x1, y1), (255, 255, 255), 2)
            # クラス名を描画
            id = int(pred[0, 0, i, 1])
            cv2.putText(src, class_names[id-1], (x0+10, y0+20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    pos = '{:3.0f}%'.format(
            cap.get(cv2.CAP_PROP_POS_FRAMES) / \
            cap.get(cv2.CAP_PROP_FRAME_COUNT) *100)
    cv2.putText(src, pos, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, \
                1, (0, 0, 0), 2)
    cv2.imshow('win_src', src)
    key = cv2.waitKey(5)
    if key == 27:
        break
    elif key == 32:
        cv2.waitKey()

cv2.destroyAllWindows()


"""
ネットワークの構造ファイル
https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt
ネットワークの重みファイル　（tar.gz圧縮の展開が必要）
http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
クラス名ファイル
https://github.com/opencv/opencv/blob/master/samples/data/dnn/object_detection_classes_coco.txt
"""
