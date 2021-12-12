import cv2
import numpy as np

# ネットワークの構造と重みファイルを読み込む
proto = 'model/bvlc_googlenet.prototxt'
weight = 'model/bvlc_googlenet.caffemodel'
net = cv2.dnn.readNet(proto, weight)

# クラス名を読み込む
label_file = 'model/classification_classes_ILSVRC2012.txt'
class_names = np.loadtxt(label_file, dtype='str', delimiter='\n')

# 入力画像
files = ['space_shuttle.jpg', 'cats.jpg', 'car.png']
imgs = [cv2.imread('data/' + f) for f in files]

for idx, src in enumerate(imgs):
    # 画像をblobに変換
    blob = cv2.dnn.blobFromImage(src, size=(224, 224))
    # blobを入力層にセット
    net.setInput(blob)
    # 入力に対する出力を計算
    pred = net.forward()
    # 出力の最大値を求める
    _, max_val, _, max_loc = cv2.minMaxLoc(pred)
    # 最大値のクラス名と信頼度を表示
    print('{} => {}, {:.3f}'
          .format(files[idx], class_names[max_loc[0]], max_val))
    cv2.imshow('win_src', src)
    if cv2.waitKey(3000) == 27:
        break

    # トップ10を表示（参考用 - コメントを外して使用）
    # for idx, val in [tup for tup in sorted(enumerate(pred[0]), key=lambda x:x[1])][-10:]:
    #    print('  {}({}): {:.3f}'.format(class_names[idx], idx, val))

cv2.destroyAllWindows()


"""
ネットワークの構造ファイル
https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/bvlc_googlenet.prototxt

ネットワークの重みファイル
http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel

クラス名ファイル
https://github.com/opencv/opencv/blob/master/samples/data/dnn/classification_classes_ILSVRC2012.txt
"""
