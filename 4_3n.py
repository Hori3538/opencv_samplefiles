# Section 4.3 Introduction.

import cv2
import numpy as np

# 注: Python 3.7 から dict は順序つき動作をするようになった
images = {
    'apple': cv2.imread('data/apple.png'),
    'book': cv2.imread('data/book.png'),
    'mask': cv2.imread('data/apple_mask.png')
}

# マスク画像を用いた合成
images['appleMasked'] = images['apple'] * (1 - images['mask'] / 255)
images['bookMasked'] = images['book'] * (images['mask'] /255)
images['synthesized'] = images['appleMasked'] + images['bookMasked']

# 順番に表示
for key in images.keys():
    dst = images[key].astype(np.uint8)   # 小数型から整数型にキャスト
    cv2.putText(dst, key, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255))
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    
