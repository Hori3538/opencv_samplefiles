import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

all = list(cv2.__dict__.keys())
idNames = list(filter(lambda id: id.startswith('CAP_PROP'), all))
print('CAPS_PROPS: {}'.format(len(idNames)))

for idName in idNames:
    id = cv2.__dict__[idName]
    val = cap.get(id)
    print(idName, id, val)

cap.release()
