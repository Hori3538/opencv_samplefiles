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


def doBGR():
    images = []
    texts = ['BGR', 'B', 'G', 'R']
    images.append(np.copy(img))
    channels = cv2.split(images[0])
    images.append(cv2.merge([channels[0], black, black]))
    images.append(cv2.merge([black, channels[1], black]))
    images.append(cv2.merge([black, black, channels[2]]))
    drawNames(images, texts)
    showMe(images, 'BGR')

def doRGB():
    images = []
    texts = ['RGB', 'R', 'G', 'B']
    images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    channels = cv2.split(images[0])
    images.append(cv2.merge([black, black, channels[0]]))
    images.append(cv2.merge([black, channels[1], black]))
    images.append(cv2.merge([channels[2], black, black]))
    drawNames(images, texts)
    showMe(images, 'RGB')

def doHSV():
    images = []
    texts = ['HSV', 'H', 'S', 'V']
    images.append(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
    channels = cv2.split(images[0])
    images.append(cv2.merge([channels[0], channels[0], channels[0]]))
    images.append(cv2.merge([channels[1], channels[1], channels[1]]))
    images.append(cv2.merge([channels[2], channels[2], channels[2]]))
    drawNames(images, texts)
    showMe(images, 'HSV')

def doYCrCb():
    images = []
    texts = ['YcrCb', 'Y', 'Cr', 'Cb']
    images.append(cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb))
    channels = cv2.split(images[0])
    images.append(cv2.merge([channels[0], channels[0], channels[0]]))
    images.append(cv2.merge([black, black, channels[1]]))
    images.append(cv2.merge([channels[2], black, black]))
    drawNames(images, texts)
    showMe(images, 'YCrCb')

# Source
img = cv2.imread('data/apple.png')
black = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)

# Keys
colorSpace = 'b'
funcs = {
    'b': doBGR,
    'r': doRGB,
    'h': doHSV,
    'y': doYCrCb
}

while True:
    try:
        funcs[colorSpace]()
    except:
        print('key "{}" not defined.'.format(colorSpace))

    key = cv2.waitKey(0)
    if key == 27:
        break
    else:
        colorSpace = chr(key)

cv2.destroyAllWindows()
