import cv2

# カメラを開く
cap = cv2.VideoCapture(0)
# 保存ビデオファイルの幅と高さ
size_rec = (800, 600)
rec = cv2.VideoWriter('data/video_dst.mp4',
                      cv2.VideoWriter_fourcc(* 'H264'),
                      30, size_rec)

while True:
    ret, src = cap.read()
    if not ret:
        break
    # 平滑化
    tmp = cv2.blur(src, (100, 5))
    # 画像の拡大縮小
    moving = cv2.resize(tmp, size_rec)
    # ガウス関数平滑化
    tmp = cv2.GaussianBlur(src, (15, 15), 5.0)
    # 画像の拡大縮小
    gaussian = cv2.resize(tmp, size_rec)
    # 入力と出力を1フレーム表示
    cv2.imshow('win_src', src)
    cv2.imshow('win_moving', moving)
    cv2.imshow('win_gaussian', gaussian)
    # 出力（moving）を1フレーム書き込み
    rec.write(moving)

    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()
# カメラを閉じる
cap.release()
# ビデオ書き込みオブジェクトを閉じる
rec.release()
