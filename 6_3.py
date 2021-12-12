import cv2
import numpy as np

# グローバル変数（関数間で交換）
width = None           # 画像サイズ横（あとで設定）
height = None          # 画像サイズ縦（あとで設定）
bs = 80                # 分割ブロックサイズ（ピクセル）
channel = 0            # カットする成分（Y=0, Cr=1, Cb=2）
threshold = 80         # カット閾値 [0, 80]
win_freq = 'Frequency' # 周波数領域ウィンドウ名（変換後）
win_space = 'Space'    # 空間領域ウィンドウ名（変換後）
src_freq = None        # 周波数領域データ（変換前; あとで設定）


def on_channel(pos):
    """ チャンネル指定スライダコールバック関数 """
    global channel
    channel = pos
    idct()

def on_threhold(pos):
    """ 閾値指定スライダコールバック関数 """
    global threshold
    threshold = pos
    idct()

def idct():
    """ チャンネル・ブロック単位での逆DCT """
    global width, height, bs, threshold, channel, src_freq
    global win_freq, win_space

    dst_freq = np.zeros((height, width, 3), np.float32)
    dst_space = np.empty((height, width, 3), np.float32)
    pos = [bs] * 3             # コピー領域
    pos[channel] = threshold
    for c in [0, 1, 2]:
        for y in range(0, height, bs):
            for x in range(0, width, bs):
                roi = dst_freq[y:y+bs, x:x+bs, c]     # 変換対象のブロック
                roi[0:pos[c], 0:pos[c]] = src_freq[y:y+pos[c], x:x+pos[c], c]
                tmp = cv2.idct(roi)                   # 逆DCT
                dst_space[y:y+bs, x:x+bs, c] = tmp     # ブロックの入れ替え

    dst_freq_split = cv2.split(dst_freq)
    cv2.imshow(win_freq, dst_freq_split[channel] * 100)
    cv2.imshow(win_space, cv2.cvtColor(dst_space, cv2.COLOR_YCrCb2BGR))

# メイン
file = 'data/book.png'

# srcの変更
src_space = cv2.imread(file)
width = int(src_space.shape[1] / bs) * bs
height = int(src_space.shape[0] / bs) * bs
src_space = cv2.resize(src_space, (width, height))
src_space = cv2.cvtColor(src_space, cv2.COLOR_BGR2YCrCb) \
                .astype(np.float32) / 255.0

# チャンネル・ブロック単位でのDCT
src_freq = np.copy(src_space)
for c in range(0, 3):
    for y in range(0, height, bs):
        for x in range(0, width, bs):
            roi = src_freq[y:y+bs, x:x+bs, c]     # 変換対象のブロック
            tmp = cv2.dct(roi)                    # DCT
            src_freq[y:y+bs, x:x+bs, c] = tmp     # ブロックの入れ替え

cv2.namedWindow(win_freq)
cv2.createTrackbar('YCrCb', win_freq, channel, 2, on_channel)
cv2.createTrackbar('Threshold', win_freq, threshold, bs, on_threhold)
cv2.namedWindow(win_space)
idct()

cv2.waitKey(0)
cv2.destroyAllWindows()