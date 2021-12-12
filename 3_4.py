import cv2
import numpy as np


def on_mouse(event, x, y, flags, param):
    """ マウスコールバック関数 """
    # 右ボタンを押下したなら、画面クリア
    if event == cv2.EVENT_RBUTTONDOWN:
        img.fill(255)

    # 左ボタンを押下中なら、描画
    elif flags & cv2.EVENT_FLAG_LBUTTON:
        r = cv2.getTrackbarPos('R', win_name)
        g = cv2.getTrackbarPos('G', win_name)
        b = cv2.getTrackbarPos('B', win_name)
        radius = cv2.getTrackbarPos('Radius', win_name)
        cv2.circle(img, (x, y), radius, (b, g, r), -1)

    # それ以外はなにもしない
    else:
        return

    cv2.imshow(win_name, img)
    
    
def nothing(x):
    pass


win_name = 'win_paint'
file = 'data/paint.png'
cv2.namedWindow(win_name)

# マウスコールバック関数の割り当て
sat = cv2.setMouseCallback(win_name, on_mouse)

# トラックバー生成
cv2.createTrackbar('R',      win_name, 100, 255, nothing)
cv2.createTrackbar('G',      win_name, 200, 255, nothing)
cv2.createTrackbar('B',      win_name, 230, 255, nothing)
cv2.createTrackbar('Radius', win_name, 10, 50, nothing)

img = np.ones((480, 640, 3), np.uint8) * 255
cv2.imshow(win_name, img)

while True:
    key = cv2.waitKey(0)
    if key == 27:
        break
    elif key == ord('s'):
        cv2.imwrite(file, img)
        print('Written to {}'.format(file))


cv2.destroyWindow(win_name)
