#!/usr/bin/env python
import cv2
import numpy as np

file = 'data/apple.png'
win_name = 'CastTest'
types = {
    'uint8': np.uint8,   # as is
    'int8': np.int8,
    'uint16': np.uint16,
    'float32': np.float32
}

src = cv2.imread(file)
cv2.namedWindow(win_name)

for type, val in types.items():
    dst = src.astype(val)
    # 表現範囲外はクリッピングされるので、255*255 でも赤と解釈される (uint16対策)
    cv2.putText(dst, type, (20, 50),  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255*255))
    cv2.imshow(win_name, dst)
    cv2.waitKey()

cv2.destroyWindow(win_name)


# おまけ。cv2.NORM_ 定数とその値のリスト
for k, v in cv2.__dict__.items():
    if k.startswith('NORM_'):
       print('{:20s} {:d}'.format(k, v))

