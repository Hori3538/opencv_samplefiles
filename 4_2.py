import cv2

src = cv2.imread('data/fruits.png')
# BGRからHSVの3チャンネル画像に変換
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
# 減色数 (180の約数）
color = 180
colors = [180, 90, 60, 45, 36, 30, 20, 18, 15, 12, 10, 9, 6, 5, 4, 3, 2, 1]

for c in colors:
    # HSVの3チャンネル画像を1チャンネル画像に分離
    h1, s1, v1 = cv2.split(hsv)
    # 色相(h1)を飛び飛びの値に変換
    color_range = 180 // c
    h1 = h1 // color_range
    h1 = h1 * color_range
    # HSVの各1チャンネルを3チャンネルのHSV画像に合成
    dst = cv2.merge((h1, s1, v1))
    # HSVからBGRの3チャンネル画像に変換
    dst = cv2.cvtColor(dst, cv2.COLOR_HSV2BGR)

    cv2.putText(dst, 'C=' + str(c), (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.imshow('win_dst', dst)
    if cv2.waitKey(0) == 27:
        break

cv2.destroyAllWindows()
