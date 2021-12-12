import cv2

img = cv2.imread('data/lena.png')

orb = cv2.ORB_create(nfeatures=30)
# cv2.KeyPointのリストとNumPy画像
keypoints, descriptors = orb.detectAndCompute(img, None)
print('Found {} keypoints.'.format(len(keypoints)))
print('Descriptor: ndim {}, shape {}, dtype {}'.format(descriptors.ndim, descriptors.shape, descriptors.dtype))
print(descriptors)
print(len(descriptors[0]))

for idx, kp in enumerate(keypoints):
	x, y = int(kp.pt[0]), int(kp.pt[1])     # 座標
	size = int(kp.size)
	desc = ''.join(['%02x' % h for h in descriptors[idx]])
	cv2.circle(img, (x, y), size, (255, 255, 255), 1)
	print('({}, {}), r={}, desc={}'.format(x, y, size, desc))


cv2.imshow('ORB', img)
cv2.waitKey()
cv2.destroyAllWindows()