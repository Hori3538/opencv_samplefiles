import cv2
import numpy as np

cap1 = cv2.VideoCapture('data/campus.mp4')
cap2 = cv2.VideoCapture('data/sample2.mp4')
width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
mode, pos = 0, 0


def transition(mode, pos):
    """ トランジション用マスク生成 """
    mask = np.ones((height, width, 3), np.float32)
    if mode == ord('w'):
        # 左右ワイプ
        boundary = int(min(width, width * pos/30))
        cv2.rectangle(
            mask, (0, 0), (boundary, height), (0, 0, 0), cv2.FILLED)
    elif mode == ord('d'):
        # ディゾルブ
        density = max(0, 1 - pos/30)
        mask.fill(density)
    elif mode == ord('c'):
        # 円形ワイプ
        radius = int(min(width, width * pos/30))
        cv2.circle(mask, (int(width/2), int(height/2)),
                   radius, (0, 0, 0), cv2.FILLED)
        mask = cv2.blur(mask, (100, 100))

    return mask


while True:
    ret1, src1 = cap1.read()
    ret2, src2 = cap2.read()
    if not ret1 or not ret2:
        cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    src2 = cv2.resize(src2, (width, height))
    # トランジション用マスク生成
    mask = transition(mode, pos)
    # マスク合成
    src1 = src1.astype(np.float32) / 255
    src2 = src2.astype(np.float32) / 255
    dst = src1 * mask + src2 * (1-mask)

    cv2.imshow('win_mask', mask)
    cv2.imshow('win_dst', dst)
    key = cv2.waitKey(10)
    if key == 27:
        break
    elif key == ord('w') or key == ord('d') or key == ord('c'):
        pos = 0
        mode = key
    pos += 1

cv2.destroyAllWindows()
