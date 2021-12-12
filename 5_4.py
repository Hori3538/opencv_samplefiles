import cv2
import numpy as np

src = cv2.imread('data/seed.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('win_src', src)

filters = {
    # グラディエントフィルタ
    'grad': [
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ],
    #  ガウスフィルタ
    'gaussian': [
        [1, 4, 6, 4, 1],
        [4,16,24,16, 4],
        [6,24,36,24, 6],
        [4,16,24,16, 4],
        [1, 4, 6, 4, 1]
    ],
    #  ラプラスフィルタ(3x3)
    'laplace3': [
        [1, 1, 1],
        [1,-9, 1],
        [1, 1, 1]
    ],
    #  ラプラスフィルタ(5×5)
    'laplace5': [
        [-1,-3,-4,-3,-1],
        [-3, 0, 6, 0,-3],
        [-4, 6,20, 6,-4],
        [-3, 0, 6, 0,-3],
        [-1,-3,-4,-3,-1]
    ],
    #  先鋭化フィルタ
    'sharpen': [
        [-1,-1,-1],
        [-1, 9,-1],
        [-1,-1,-1]
    ]
}

for filter in filters.keys():
    kernel = np.array(filters[filter], np.float32)
    if filter == 'gaussian':
        kernel = kernel / 256.0
    dst = cv2.filter2D(src, -1, kernel)
    cv2.putText(dst, filter, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 128)
    cv2.imshow('win_dst', dst)
    if cv2.waitKey(0) == 27:
        break

cv2.destroyAllWindows()