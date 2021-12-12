import cv2

videos = ['walker.mp4', 'office.mp4']
caps = [cv2.VideoCapture('data/' + v) for v in videos]

# ネットワークの構造と重みファイルを読み込む
proto = 'model/deploy.prototxt'
weight = 'model/res10_300x300_ssd_iter_140000_fp16.caffemodel'
net = cv2.dnn.readNet(proto, weight)

videoIdx = 0
while True:
    ret, src = caps[videoIdx].read()
    if not ret:
        caps[videoIdx].set(cv2.CAP_PROP_POS_FRAMES, 0)        
        videoIdx = 1 - videoIdx
        continue

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
        if conf > 0.5:
            # 推定された座標に枠を描画
            x0 = int(pred[0, 0, i, 3] * src.shape[1])
            y0 = int(pred[0, 0, i, 4] * src.shape[0])
            x1 = int(pred[0, 0, i, 5] * src.shape[1])
            y1 = int(pred[0, 0, i, 6] * src.shape[0])
            cv2.rectangle(src, (x0, y0), (x1, y1), (255, 255, 255), 2)

    pos = '{:3.0f}%'.format(
            caps[videoIdx].get(cv2.CAP_PROP_POS_FRAMES) / \
            caps[videoIdx].get(cv2.CAP_PROP_FRAME_COUNT) *100)
    cv2.putText(src, pos, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, \
                1, (0, 0, 0))
    cv2.imshow('win_src', src)
    if cv2.waitKey(5) == 27:
        break

cv2.destroyAllWindows()


"""
ネットワークの構造ファイル
https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
ネットワークの重みファイル
https://github.com/opencv/opencv_3rdparty/raw/19512576c112aa2c7b6328cb0e8d589a4a90a26d/res10_300x300_ssd_iter_140000_fp16.caffemodel
"""
