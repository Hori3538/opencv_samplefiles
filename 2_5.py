import cv2

# ビデオファイルを開く
cap = cv2.VideoCapture('data/sample2.mp4')
# ビデオファイルの保存設定
rec = cv2.VideoWriter('data/video_dst.mp4',
                      cv2.VideoWriter_fourcc(*'H264'),
                      30, (640, 480))

# ループ開始
while True:
    # 1フレーム読み込み
    ret, src = cap.read()
    if not ret:
        break
    # グレースケールに変換
    dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # 2値化
    ret, dst = cv2.threshold(dst, 128, 255, cv2.THRESH_BINARY)
    # 3チャンネルに変換
    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    # 1フレーム表示
    cv2.imshow('win_src', src)
    cv2.imshow('win_dst', dst)
    # 1フレーム書き込み
    rec.write(dst)
    # キー入力待機（30 ms）。Escキーで中断。
    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()
# ビデオ書き込みオブジェクトを閉じる
rec.release()
