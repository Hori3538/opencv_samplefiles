import cv2
import numpy as np

def drawNames(images, texts):
	for i in range(0, 4):
		cv2.putText(images[i], texts[i], (20, 40), \
					cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))

def showMe(images, colorspace):
	names = ['ALL', '0', '1', '2']
	for i, name in enumerate(names):
		cv2.imshow('Channel-{}'.format(name), images[i])

	average = cv2.mean(images[0])
	display = ['{:<7}'.format(colorspace)]
	for i in range(0, len(average)-1):
		display.append('Ch-{}: {:<10.1f}'.format(i, average[i]))
	print(''.join(display))


def convert(imgOrig, spec):
	img0 = cv2.cvtColor(imgOrig, spec['conv']) if spec['conv'] >= 0 else np.copy(imgOrig)
	images = [ img0 ]
	channels = cv2.split(img0)
	for plain in spec['blend']:
		for idx, c in enumerate(plain):
			plain[idx] = channels[c] if isinstance(c, int) else c
		images.append(cv2.merge(plain))

	drawNames(images, spec['text'])
	showMe(images, spec['text'][0])

# Source
img = cv2.imread('data/apple.png')
black = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)

# 変換仕様
# blendはグレースケールからカラーを作成するときの混合順序。
#  整数ならそのチャンネルの画像を使用。それ以外はblackをそのまま使用。
# convはカラー変換定数。-1ならオリジナルのまま。
colorSpace = 'b'
specs = {
	'b': {
		'text': ['BGR', 'B', 'G', 'R'],
		'blend': [[0, black, black], [black, 1, black], [black, black, 2]],
		'conv': -1
	},
	'r': {
		'text': ['RGB', 'R', 'G', 'B'],
		'blend': [ [black, black, 0], [black, 1, black], [2, black, black] ],
		'conv': cv2.COLOR_BGR2RGB
	},
	'h': {
		'text': ['HSV', 'H', 'S', 'V'],
		'blend': [ [0, 0, 0], [1, 1, 1], [2, 2, 2] ],
		'conv': cv2.COLOR_BGR2HSV
	},
	'y': {
		'text': ['YCrCb', 'Y', 'Cr', 'Cb'],
		'blend': [ [0, 0, 0], [black, black, 1], [2, black, black] ],
		'conv': cv2.COLOR_BGR2YCrCb
	}
}

while True:
	try:
		convert(img, specs[colorSpace])
	except:
		print('key "{}" not defined.'.format(colorSpace))

	key = cv2.waitKey(0)
	if key == 27:
		break
	else:
		colorSpace = chr(key)

cv2.destroyAllWindows()
