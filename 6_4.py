import cv2
import numpy as np

# 分割サイズ（ピクセル）
bs = 8
cap = cv2.VideoCapture('data/sample1.mp4')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
ws = int(width / bs)
hs = int(height / bs)


def get_flow(src, prev):
    """ オプティカルフロー取得 """
    curr = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    curr = cv2.resize(curr, (ws, hs))
    prev = cv2.cvtColor(prev, cv2.COLOR_RGB2GRAY)
    prev = cv2.resize(prev, (ws, hs))
    # オプティカルフロー計算手法（Farneback法）
    flow = cv2.calcOpticalFlowFarneback(
        prev, curr, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    return flow


def draw_arrow(flow):
    """ オプティカルフロー矢印描画 """
    # フローをx成分とy成分に分離
    flow_x, flow_y = cv2.split(flow)
    # 矢印描画
    flow_arrow = np.ones((height, width, 1), np.uint8) * 255
    for py in range(0, flow_arrow.shape[0], bs):
        for px in range(0, flow_arrow.shape[1], bs):
            dx = int(flow_x[int(py / bs), int(px / bs)] * 8)
            dy = int(flow_y[int(py / bs), int(px / bs)] * 8)
            cv2.arrowedLine(flow_arrow, (px, py), (px + dx, py + dy), 0)
    # 中心の大きい矢印を描画
    arrow_x = int(flow_arrow.shape[1] / 2)
    arrow_y = int(flow_arrow.shape[0] / 2)
    mean_h = int(cv2.mean(flow_x)[0] * 100)
    mean_v = int(cv2.mean(flow_y)[0] * 100)
    cv2.arrowedLine(flow_arrow, (arrow_x, arrow_y),
                    (arrow_x + mean_h, arrow_y + mean_v),
                    (128), 10, cv2.LINE_8, 0, 0.5)
    return flow_arrow


def draw_color(flow):
    """ オプティカルフロー色相描画 """
    # フローをx成分とy成分に分離
    flow_x, flow_y = cv2.split(flow)
    # フローを長さと角度に変換
    length, angle = cv2.cartToPolar(flow_x, flow_y, angleInDegrees=True)
    # 長さを彩度（0～255）に変換
    length = length * 255
    length[length > 255] = 255
    length = length.astype(np.uint8)
    # 角度（0～360度）を色相（0～180）に変換
    angle = (angle / 2 + 45).astype(np.uint8)
    # 角度をH、長さをS、明るさVを255として合成
    value = np.ones((hs, ws), np.uint8) * 255
    hsv = cv2.merge((angle, length, value))
    hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    # 入力サイズに拡大
    flow_color = cv2.resize(hsv, (width, height))
    return flow_color


prev = np.zeros((height, width, 3), np.uint8)
while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        prev = np.zeros((height, width, 3), np.uint8)
        continue
    # フロー取得
    flow = get_flow(src, prev)
    # フロー矢印描画
    flow_arrow = draw_arrow(flow)
    # フロー色相描画
    flow_color = draw_color(flow)
    # 現在画像を事前画像に保存
    prev = src
    cv2.imshow('win_src', src)
    cv2.imshow('win_arrow', flow_arrow)
    cv2.imshow('win_color', flow_color)
    key = cv2.waitKey(10)
    if key == 27:
        break
    elif key == 32:
        cv2.waitKey()

cv2.destroyAllWindows()
