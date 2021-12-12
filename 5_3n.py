import cv2

cap = cv2.VideoCapture('data/campus.mp4')
bs = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, src = cap.read()
    dst = bs.apply(src)
    cv2.imshow('win_dst', dst)
    if cv2.waitKey(30) == 27:
        break
   
cv2.destroyAllWindows()
