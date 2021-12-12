import cv2
import numpy as np

# 定数
SW, SH = 480, 480        # 変換後のサイズ
CR = 16                  # クリック判定半径
P_INIT = np.array(       # ROI 初期位置
    [[150, 100], [250, 100], [250, 200], [150, 200]], np.float32)
P_DST = np.array(        # 変換後の四角形
    [[0, 0], [SW, 0], [SW, SH], [0, SH]], np.float32)

# 変数
p_src = np.copy(P_INIT)  # 変換元座標（初期値）
num_near_point = -1      # 最近傍の要素番号（最初は-1を入れておく）


def on_mouse(event, x, y, flags, params):
    """ マウスコールバック関数 """
    global num_near_point, p_src

    if event == cv2.EVENT_LBUTTONDOWN:
        # 左ボタンを押したとき、要素番号と距離最小値の初期化
        num_near_point = -1
        min_distance = CR
        # 4点から最近傍の要素番号を探す
        for i in range(4):
            # マウスと小円の距離
            distance = cv2.norm(np.array((x, y), np.float32), p_src[i])
            if distance < min_distance:
                # 距離最小値より小さいとき、要素番号と距離最小値の更新
                num_near_point = i
                min_distance = distance
    elif(event == cv2.EVENT_MOUSEMOVE and
         flags == cv2.EVENT_FLAG_LBUTTON and
         num_near_point >= 0):
        # マウス移動 & 左ボタン押下 & 近傍点取得済のとき、座標更新
        x = f_size[1] if x > f_size[1] else x
        x = 0 if x < 0 else x
        y = f_size[0] if y > f_size[0] else y
        y = 0 if y < 0 else y
        p_src[num_near_point] = (x, y)
    elif event == cv2.EVENT_RBUTTONDOWN:
        # 右ボタンを押したとき、4点リセット
        p_src = np.copy(P_INIT)


cap = cv2.VideoCapture('data/campus.mp4')
f_size = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
          int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
cv2.namedWindow('win_src')
cv2.setMouseCallback('win_src', on_mouse)

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    # 射影変換行列の取得
    h_mat = cv2.getPerspectiveTransform(p_src, P_DST)
    # 入力画像を射影変換
    dst = cv2.warpPerspective(src, h_mat, (SW, SH))
    # 4点を結ぶ線を描画
    points = np.array([p_src[0], p_src[1], p_src[2], p_src[3]], np.int32)
    cv2.polylines(src, [points], True, (255, 0, 0), 2)
    # 4点の円を描画
    for i in range(4):
        cv2.circle(src, (points[i, 0], points[i, 1]), CR, (0, 0, 0), 3)
    cv2.imshow('win_src', src)
    cv2.imshow('win_dst', dst)
    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()
