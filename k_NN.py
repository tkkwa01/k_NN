import math
import sys
import random


# 2つの特徴点間の直線距離を計算する関数
def calcDistance(v1, v2):
    sum2 = 0
    dim = len(v1)
    for i in range(dim):
        sum2 += ((v1[i] - v2[i]) ** 2)
    return math.sqrt(sum2)


# データを読み込む関数
def loadData(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    data = []
    for line in lines:
        items = line.strip().split()
        prefecture = items[0]
        region = int(items[1])
        lat = float(items[2])
        lon = float(items[3])
        data.append((prefecture, region, [lat, lon]))
    return data


# k-NN法で分類
success_count = 0  # 識別成功数
k = 3

# データを読み込む
all_data = loadData('/Users/aoi/pj/sizen_gengo/projects/report2_projects/data2.txt')

# 地方名
regionNames = ['東北・北海道', '関東', '中部', '近畿', '中国', '四国', '九州・沖縄']

# ランダムに5つのデータを選択して分類データとし、残りを学習データとする
random.shuffle(all_data)
test_data = all_data[:5]
training_data = all_data[5:]

for i, (test_pref, test_region, test_coords) in enumerate(test_data):
    print(f"\n{test_pref}：", end="")

    distances = [(calcDistance(test_coords, coords), pref, region) for pref, region, coords in training_data]
    sorted_distances = sorted(distances)
    topk = sorted_distances[:k]

    # 多数決
    vote_count = [0] * 7  # 地方名の数だけ初期化
    for _, _, region in topk:
        vote_count[region] += 1

    estimated_region = vote_count.index(max(vote_count))

    # トップ3と識別結果の表示
    print(f"（トップ3）{' '.join([pref for _, pref, _ in topk])}→", end="")
    print(f"（識別結果）{regionNames[estimated_region]}", end="")

    # 識別成功か失敗かを表示
    if estimated_region == test_region:
        print(" 識別成功")
        success_count += 1
    else:
        print(" 識別失敗")

# 識別成功率の表示
print(f"\n識別成功率：{success_count}/5")
