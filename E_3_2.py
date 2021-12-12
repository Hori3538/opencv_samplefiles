import cv2
import numpy as np
import glob
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.optimizers import RMSprop
from sklearn.model_selection import train_test_split
from tensorflow.python.framework.convert_to_constants\
    import convert_variables_to_constants_v2

# クラス名
class_names = ['apple', 'ballpoint pen', 'laptop computer']
# 画像読み込みと前処理
x_data, y_data = [], []
for class_id, class_name in enumerate(class_names):
    files = glob.glob('data/' + class_name + '/*.jpg')
    for file in files:
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img = cv2.resize(img, (28, 28))
        img = img[:, :, np.newaxis]
        img = img.astype(np.float32) / 255.0
        x_data.append(img)
        y_data.append(class_id)

x_data = np.asarray(x_data)
y_data = np.asarray(y_data)
y_data = tf.keras.utils.to_categorical(y_data, len(class_names))
print('{} image files read.'.format(len(x_data)))

# データを訓練用とテスト用に分ける
x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, test_size=0.20)
print('Files: Train {}, Test {}'.format(len(x_train), len(x_test)))

# ネットワークの構造定義
tf.compat.v1.enable_eager_execution()
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu', input_shape=(28, 28, 1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(class_names), activation='softmax'))

# モデルのコンパイルと訓練実行
model.compile(RMSprop(), 'categorical_crossentropy', metrics=['acc'])
model.fit(x_train, y_train, batch_size=64, epochs=200,
          validation_data=(x_test, y_test))

# ネットワークの構造と重みを保存（Tensorflowのpb形式）
full_model = tf.function(lambda x: model(x))
full_model = full_model.get_concrete_function(
    tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype))
frozen_func = convert_variables_to_constants_v2(full_model)
frozen_func.graph.as_graph_def()
tf.io.write_graph(frozen_func.graph,
                  'model/', 'imagenet_model.pb', as_text=False)

'''
tensorflowとscikit-learnのインストールが必要（macOSはpip3）
pip install tensorflow==2.3.1
pip install scikit-learn
'''
