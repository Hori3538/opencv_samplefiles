import cv2
import numpy as np


def on_mouse(event, x, y, flags, param):
    """ マウスコールバック関数 """
    if flags == cv2.EVENT_FLAG_LBUTTON:
        cv2.circle(mask, (x, y), 32, (0.0), -1)
    elif event == cv2.EVENT_RBUTTONDOWN:
        mask.fill(1.0)
    else:
        return

    dft_idft()


def dft_idft():
    """ 周波数フィルタリング """
    dst_freq = src_freq * mask                         # フィルタリング
    dst_freq_real, _ = cv2.split(dst_freq)             # 表示用
    cv2.imshow('win_real', dst_freq_real/10)           # DFT後の画像表示

    dst_freq = np.fft.ifftshift(dst_freq)              # 対角を戻す
    dst_space = cv2.idft(dst_freq)                     # 逆DFT
    dst, _ = cv2.split(dst_space)                      # 分離
    dst = cv2.normalize(dst, None, 0.0, 1.0,           # 正規化
                        cv2.NORM_MINMAX)
    cv2.imshow('win_dst', dst)


src = cv2.imread('data/fruits.png', cv2.IMREAD_GRAYSCALE) \
                 .astype(np.float32) / 255.0
mask = np.ones((src.shape[0], src.shape[1], 2), np.float32)

src_freq = cv2.dft(src, None, cv2.DFT_COMPLEX_OUTPUT)  # DFT
src_freq = np.fft.fftshift(src_freq)                   # 対角の入れ替え

cv2.namedWindow('win_real')
cv2.setMouseCallback('win_real', on_mouse)
dft_idft()
cv2.waitKey(0)
cv2.destroyAllWindows()