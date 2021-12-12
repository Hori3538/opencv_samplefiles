import cv2


def on_mouse(event, x, y, flags, param):
    """ マウスコールバック関数（矩形指定） """
    if event == cv2.EVENT_LBUTTONDOWN:
        # 左ボタン押下時、始点座標を更新
        param['x0'] = x
        param['y0'] = y
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        # マウス移動 & 左ボタン押下中、終点座標を更新（追随）
        param['x1'] = x
        param['y1'] = y


def nothing(x):
    pass


cap = cv2.VideoCapture('data/campus.mp4')
cv2.namedWindow('win_dst')
cv2.createTrackbar('Brightness', 'win_dst', 20, 50, nothing)
cv2.createTrackbar('Blur', 'win_dst', 12, 30, nothing)
cv2.createTrackbar('Wait', 'win_dst', 5, 50, nothing)
# 矩形領域の座標を辞書に格納
param = {'x0': 40, 'y0': 100, 'x1': 600, 'y1': 320}
# マウスコールバック関数と受け渡しパラメータの割り当て
cv2.setMouseCallback('win_dst', on_mouse, param)

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    # トラックバー値（明るさ、ぼかしサイズ、待機時間）の取得
    brightness = cv2.getTrackbarPos('Brightness', 'win_dst') / 10.0
    blur_size = cv2.getTrackbarPos('Blur', 'win_dst')
    wait_time = cv2.getTrackbarPos('Wait', 'win_dst')
    # 明るさ変換
    src = cv2.addWeighted(src, brightness, src, 0, 0)
    # ぼかし
    dst = cv2.blur(src, (blur_size + 1, blur_size + 1))
    # 辞書からパラメータ取得
    x0, y0, x1, y1 = param.values()
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    # 画像の一部の矩形領域をコピー
    dst[y0:y1, x0:x1] = src[y0:y1, x0:x1]
    cv2.imshow('win_dst', dst)
    # 待機時間（再生速度）
    if cv2.waitKey(wait_time + 1) == 27:
        break

cv2.destroyAllWindows()
