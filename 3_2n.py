import sys
import cv2
import numpy as np

src1 = cv2.imread('data/colorado.png')
src2 = cv2.imread('data/koma.png')

alpha = 0.4
if len(sys.argv) > 1:
    alpha = float(sys.argv[1])
beta = 1 - alpha
gamma = 0


dst = cv2.addWeighted(src1, alpha, src2, beta, gamma)
cv2.imshow('Add-Weight', dst)
cv2.waitKey(0)
