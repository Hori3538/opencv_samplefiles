import cv2

def draw_grid(img, num):
    """ グリッド模様とフレーム数を描画 """
    for x in range(30, img.shape[1], 30):
        for y in range(30, img.shape[0], 30):
            cv2.circle(img, (x, y), 1, (255, 255, 255))
    cv2.putText(img, str(num), (20, 40),
                cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 255, 255), 2)
    return img


# カメラ入力映像
cap = cv2.VideoCapture(0)
# カメラ入力映像の幅と高さのサイズ
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# ビデオ出力ファイル設定
rec = cv2.VideoWriter('data/komadori.mp4', cv2.VideoWriter_fourcc(*'H264'),
                      5, frame_size)

print('Space key: Write frame, Esc key: Exit')
count = 0

while True:
    # 現在フレームを取得
    _, src = cap.read()

    if count > 0:
        # 現在フレームと前フレームを半々で合成
        dst = cv2.addWeighted(src, 0.5, prev, 0.5, 0)
    else:
        dst = src

    # グリッド模様とフレーム数を描画
    dst = draw_grid(dst, count)
    cv2.imshow('win_dst', dst)
    key = cv2.waitKey(30)

    # スペースキーを押したとき
    if key == ord(' '):
        # 1フレーム書き込み
        rec.write(src)
        # 現在フレームを前フレームに複製
        prev = src.copy()
        count += 1
    elif key == 27:
        break

cv2.destroyAllWindows()
rec.release()
