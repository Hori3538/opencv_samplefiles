import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.optimizers import RMSprop
from tensorflow.python.framework.convert_to_constants\
    import convert_variables_to_constants_v2

# 1. MNISTデータを読込む
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print('Handwritten data read: Train {}, Test {}'.
      format(len(x_train), len(x_test)))

# MNISTデータを入力形式に合わせる
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
x_train = x_train.astype(np.float32) / 255
x_test = x_test.astype(np.float32) / 255
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

# 2. 確認用にMNISTデータをいくつか表示
for i in range(20):
    cv2.imshow('win_img', x_train[i])
    cv2.waitKey(200)
cv2.destroyWindow('win_img')

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
model.add(Dense(10, activation='softmax'))

# 3. モデルのコンパイルと訓練実行
model.compile(RMSprop(), 'categorical_crossentropy', metrics=['acc'])
model.fit(x_train, y_train, batch_size=64, epochs=10,
          validation_data=(x_test, y_test))

# 4. ネットワークの構造と重みを保存（Tensorflowのpb形式）
full_model = tf.function(lambda x: model(x))
full_model = full_model.get_concrete_function(
    tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype))
frozen_func = convert_variables_to_constants_v2(full_model)
frozen_func.graph.as_graph_def()
tf.io.write_graph(frozen_func.graph,
                  'model/', 'mnist_model.pb', as_text=False)

'''
tensorflowのインストールが必要（macOSはpip3）
pip install tensorflow==2.3.1
'''
