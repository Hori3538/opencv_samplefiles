import cv2

cap = cv2.VideoCapture('data/sample2.mp4')
# 最初は200フレーム目（ロボ）を対象画像objとする
cap.set(cv2.CAP_PROP_POS_FRAMES, 200)
ret, obj = cap.read()

while True:
    ret, src = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    # 入力と対象の特徴抽出
    orb = cv2.ORB_create()
    key_src, desc_src = orb.detectAndCompute(src, None)
    key_obj, desc_obj = orb.detectAndCompute(obj, None)
    # 特徴量マッチング
    matcher = cv2.BFMatcher_create(cv2.NORM_HAMMING)
    all_matches = matcher.match(desc_src, desc_obj)
#    dist_list = list([m.distance for m in all_matches])
#    if len(dist_list) != 0:
#    	print('num: {}, max {}, min {}' \
#			.format(len(all_matches), max(dist_list), min(dist_list)))
    # 似ている特徴ペアをピックアップ
    good_matches = [[good] for good in all_matches if good.distance < 30]
    # 比較画像描画
    compare = cv2.drawMatchesKnn(
        src, key_src, obj, key_obj, good_matches, None)
    # 類似度計算
    similarity = len(good_matches) / len(key_obj)
    # 類似度表示
    cv2.putText(compare, f'{similarity:.3f}', (src.shape[1]+8, 24),
                cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
    if similarity > 0.01:
        # 類似度が0.01より大きければ'Detect'と表示
        cv2.putText(compare, 'Detect', (8, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, 4)

    cv2.imshow('win_compare', compare)
    key = cv2.waitKey(10)

    if key == ord('r'):
        # rキーで対象画像更新
        obj = src.copy()
    elif key == 27:
        break
    elif key == 32:
    	cv2.waitKey()

cv2.destroyAllWindows()
