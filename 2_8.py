import cv2
import numpy as np

# ビデオファイルを開く
cap = cv2.VideoCapture('data/campus.mp4')
# 映像の横幅と高さ
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# 総フレーム数
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# フレームレート
fps = int(cap.get(cv2.CAP_PROP_FPS))
# 周期（待ち時間）
period = int(1000 / fps)

print('W×H: {}'.format(size))
print('fps: {}, Period: {} (ms)'.format(fps, period))
print('#Frame: {}, Total  time: {} (s)'
      .format(frame_count, round(frame_count/fps, 2)))

loop = True

while loop:
    # 再生位置の初期値をランダムに決定
    pos = np.random.randint(frame_count)
    # 再生方向をランダムに決定
    direction = np.random.randint(2) * 2 - 1
    # 再生フレーム数をランダムに決定
    frames = np.random.randint(30) + 10

    print('POS: {}, Direction: {}, #Frame: {}'
          .format(pos, direction, frames))

    for frame in range(frames):
        # 再生位置を指定
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, src = cap.read()
        cv2.imshow('win_src', src)
        # 再生位置の更新
        pos += direction
        # 先頭と末尾での処理
        pos = max(pos, 0)
        pos = min(pos, frame_count - 1)

        if cv2.waitKey(period) == 27:
            loop = False
            break

cv2.destroyAllWindows()
