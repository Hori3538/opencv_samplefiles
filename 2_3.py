import cv2
import numpy as np


def image_info(img, winname, action):
    """ 属性の表示 """
    print(' --- {}: {} ---'.format(winname, action))
    print(' shape: {}'.format(img.shape))
    print(' WxH: ({}, {})'.format(img.shape[1], img.shape[0]))
    if img.ndim > 2:
        print(' channels: {}'.format(img.shape[2]))
    print(' ndim: {}, type: {}'.format(img.ndim, img.dtype))
    cv2.imshow(winname, img)
    cv2.waitKey(0)
    cv2.destroyWindow(winname)


# Action 1a: 3チャンネル画像を生成（初期化なし）
shape = (300, 400, 3)
img_1 = np.empty(shape, np.uint8)
image_info(img_1, 'img_1', 'Create 3-channel/uint8 image: No initialization')

# Action 1b: img_1の画像全体を白、一部を青で塗る
img_1[:] = (255, 255, 255)
img_1[100:200] = (255, 0, 0)
image_info(img_1, 'img_1', 'Paint it blue')

# Action 2: 1チャンネル画像をグレー（128）で塗る
img_2 = np.empty((300, 300), np.uint8)
img_2.fill(128)
image_info(img_2, 'img_2', 'Create 1-channel/uint8 image: Paint it gray')

# Action 3: 全体が黒（0）の画像を生成
img_3 = np.zeros((800, 400), np.uint8)
image_info(img_3, 'img_3', 'Create 1-channel/uint8 image: Paint it black')

# Action 4: 全体が1の画像からグレー（200）の画像を生成
img_4 = np.ones((400, 600), np.uint8) * 200
image_info(img_4, 'img_4', 'Create 1-channel/unit8 image: Start from 1, then 200')

# Action 5: 小数型画像の全体を黄色く塗る
img_5 = np.empty((200, 200, 3), np.float32)
img_5[:, :, 0] = 0.0  # blue
img_5[:, :, 1] = 1.0  # green
img_5[:, :, 2] = 1.0  # red
image_info(img_5, 'img_5', 'Create 3-channel/float32 image: Paint it yellow')

# Action 6: コピー
img_6 = img_1.copy()   # 値コピー
image_info(img_6, 'img_6', 'Copy of img_1')
