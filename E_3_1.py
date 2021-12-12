import os
from urllib import request

# クラス名とID (http://image-net.org/archive/words.txt)
class_names = {'apple': 'n07739125',
               'ballpoint pen': 'n02783161',
               'laptop computer': 'n03642806'}

# 1クラスあたりの最大ダウンロード画像数
item_max = 500

for class_name, id in class_names.items():
    # クラス名の保存フォルダを生成
    os.makedirs('data/' + class_name, exist_ok=True)
    # ImageNetから画像のURL一覧を取得
    response = request.urlopen(
        'http://www.image-net.org/api/text/'
        'imagenet.synset.geturls?wnid=' + id)
    urls = response.read().decode().split()
    print('{}: Found {} urls. Trim to {}.'\
        .format(class_name, len(urls), item_max))

    item_num = 0

    for url in urls:
        if item_num >= item_max:
            break
        try:
            # 画像をダウンロード
            response = request.urlopen(url)
            img = response.read()
            # 画像を保存
            file_name = os.path.split(url)[1]
            file = open('data/' + class_name + '/' + file_name, 'wb')
            file.write(img)
            file.close()
            print('{}'.format(item_num), end=' ', flush=True)
            item_num += 1
        except:
            print('.', end=' ')

    print('')
