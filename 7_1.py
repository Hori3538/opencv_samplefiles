import cv2
import numpy as np

cap = cv2.VideoCapture('data/sample1.mp4')
objects = {
	'ball': cv2.imread('data/ball.png'),
	'car': cv2.imread('data/car.png')
}

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    # 対象物体2種類
    for name, obj in objects.items():
        #  テンプレートマッチング
        map_cc = cv2.matchTemplate(src, obj, cv2.TM_CCOEFF_NORMED)
        #  相互相関係数の最大値探索
        _, max_v, _, max_xy = cv2.minMaxLoc(map_cc)
        if max_v > 0.4:
            # 類似度が0.4より大きければ枠と名前描画
            to_xy = (max_xy[0]+obj.shape[1], max_xy[1]+obj.shape[0])
            cv2.rectangle(src, max_xy, to_xy, (255, 255, 255), 4)
            cv2.putText(src, name, (max_xy[0]+10, max_xy[1]+30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # map_cc = np.where(map_cc < 0.0, 0.0, map_cc)
        # map_cc = cv2.normalize(map_cc, None, 0.0, 1.0, cv2.NORM_MINMAX)
        # map_cc = map_cc ** 3
        cv2.imshow('win_map_' + name, map_cc)

    cv2.imshow('win_src', src)
    key = cv2.waitKey(30)
    if key == 27:
        break
    elif key == 32:
    	cv2.waitKey(0)

cv2.destroyAllWindows()
