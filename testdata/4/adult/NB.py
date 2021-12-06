# -*- coding: utf-8 -*-

from numpy import median
import numpy as np
import sys
import importlib
importlib.reload(sys)

characters = ["age", "type_employer", "fnlwgt", "education", "education_num", "marital", "occupation", "relationship",
              "race", "sex", "capital_gain", "capital_loss", "hr_peer_week", "country", "income"]

simplified_map = {"Never-worked": "not-working", "Without-pay": "not-working",
                  # 字段2，职业类型
                  "Local-gov": "other-govt", "State-gov": "other-govt",
                  # 字段2，职业类型
                  "Self-emp-inc": "self-employed", "Self-emp-not-inc": "self-employed",
                  # 字段7，职业
                  "Craft-repair": "blue-collar", "Farming-fishing": "blue-collar", "Handlers-cleaners": "blue-collar",
                  "Machine-op-inspct": "blue-collar", "Transport-moving": "blue-collar",
                  # 字段7，职业
                  "Other-service": "service", "Priv-house-serv": "service",
                  # 字段14，国籍
                  "Cambodia": "SE-Asia", "Laos": "SE-Asia", "Philippines": "SE-Asia", "Thailand": "SE-Asia",
                  "Vietnam": "SE-Asia",
                  # 字段14，国籍
                  "Canada": "British-Commonwealth", "England": "British-Commonwealth", "India": "British-Commonwealth",
                  "Ireland": "British-Commonwealth", "Scotland": "British-Commonwealth",
                  # 字段14，国籍
                  "China": "China", "Hong": "China", "Taiwan": "China",
                  # 字段14， 国籍
                  "Columbia": "South-America", "Ecuador": "South-America", "El-Salvador": "South-America",
                  "Peru": "South-America",
                  # 字段14，国籍
                  "Cuba": "other", "Iran": "other", "Japan": "other",
                  # 字段14， 国籍
                  "Dominican-Republic": "Latin-America", "Guatemala": "Latin-America", "Haiti": "Latin-America",
                  "Honduras": "Latin-America", "Jamaica": "Latin-America", "Mexico": "Latin-America",
                  "Nicaragua": "Latin-America", "Outlying-US(Guam-USVI-etc)": "Latin-America",
                  "Puerto-Rico": "Latin-America", "Trinadad&Tobago": "Latin-America",
                  # 字段14，国籍
                  "France": "Euro_1", "Germany": "Euro_1", "Holand-Netherlands": "Euro_1", "Italy": "Euro_1",
                  # 字段14，国籍
                  "Greece": "Euro_2", "Hungary": "Euro_2", "Poland": "Euro_2", "Portugal": "Euro_2",
                  "Yugoslavia": "Euro_2",
                  # 字段4， 学历
                  "10th": "dropout", "11th": "dropout", "12th": "dropout", "1st-4th": "dropout", "5th-6th": "dropout",
                  "7th-8th": "dropout", "9th": "dropout", "Preschool": "dropout",
                  # 字段4，学历
                  "Assoc-acdm": "Assoc", "Assoc-voc": "Assoc",
                  # 字段6，婚姻状况
                  "Married-AF-spouse": "Married", "Married-civ-spouse": "Married",
                  # 字段6，婚姻状况
                  "Married-spouse-absent": "not-married", "Separated": "not-married", "Divorced": "not-married"}

# 字段13，每周工作时长
hour_map = {"1": "10s", "2": "10s", "3": "10s", "4": "10s", "5": "10s", "6": "10s", "7": "10s", "8": "10s", "9": "10s",
            "10": "10s",    # [1-10]映射成10小时
            # [11-20]映射成20小时
            "11": "20s", "12": "20s", "13": "20s", "14": "20s", "15": "20s", "16": "20s", "17": "20s", "18": "20s",
            "19": "20s", "20": "20s",
            # [21-30]映射成30小时
            "21": "30s", "22": "30s", "23": "30s", "24": "30s", "25": "30s", "26": "30s", "27": "30s", "28": "30s",
            "29": "30s", "30": "30s",
            # [31-40]映射成40小时
            "31": "40s", "32": "40s", "33": "40s", "34": "40s", "35": "40s", "36": "40s", "37": "40s", "38": "40s",
            "39": "40s", "40": "40s",
            # [41-50]映射成50小时
            "41": "50s", "42": "50s", "43": "50s", "44": "50s", "45": "50s", "46": "50s", "47": "50s", "48": "50s",
            "49": "50s", "50": "50s",
            # [51-60]映射成60小时
            "51": "60s", "52": "60s", "53": "60s", "54": "60s", "55": "60s", "56": "60s", "57": "60s", "58": "60s",
            "59": "60s", "60": "60s",
            # [61-70]映射成70小时
            "61": "70s", "62": "70s", "63": "70s", "64": "70s", "65": "70s", "66": "70s", "67": "70s", "68": "70s",
            "69": "70s", "70": "70s",
            # [71-80]映射成80小时
            "71": "80s", "72": "80s", "73": "80s", "74": "80s", "75": "80s", "76": "80s", "77": "80s", "78": "80s",
            "79": "80s", "80": "80s",
            # [81-90]映射成90小时
            "81": "90s", "82": "90s", "83": "90s", "84": "90s", "85": "90s", "86": "90s", "87": "90s", "88": "90s",
            "89": "90s", "90": "90s",
            # [91-100]映射成100小时
            "91": "100s", "92": "100s", "93": "100s", "94": "100s", "95": "100s", "96": "100s", "97": "100s",
            "98": "100s", "99": "100s", "100": "100s"}

# 字段1，年龄
age_map = {"1": "5s", "2": "5s", "3": "5s", "4": "5s", "5": "5s",
           "6": "10s", "7": "10s", "8": "10s", "9": "10s", "10": "10s",
           "11": "15s", "12": "15s", "13": "15s", "14": "15s", "15": "15s",
           "16": "20s", "17": "20s", "18": "20s", "19": "20s", "20": "20s",
           "21": "25s", "22": "25s", "23": "25s", "24": "25s", "25": "25s",
           "26": "30s", "27": "30s", "28": "30s", "29": "30s", "30": "30s",
           "31": "35s", "32": "35s", "33": "35s", "34": "35s", "35": "35s",
           "36": "40s", "37": "40s", "38": "40s", "39": "40s", "40": "40s",
           "41": "45s", "42": "45s", "43": "45s", "44": "45s", "45": "45s",
           "46": "50s", "47": "50s", "48": "50s", "49": "50s", "50": "50s",
           "51": "55s", "52": "55s", "53": "55s", "54": "55s", "55": "55s",
           "56": "60s", "57": "60s", "58": "60s", "59": "60s", "60": "60s",
           "61": "65s", "62": "65s", "63": "65s", "64": "65s", "65": "65s",
           "66": "70s", "67": "70s", "68": "70s", "69": "70s", "70": "70s",
           "71": "75s", "72": "75s", "73": "75s", "74": "75s", "75": "75s",
           "76": "80s", "77": "80s", "78": "80s", "79": "80s", "80": "80s",
           "81": "85s", "82": "85s", "83": "85s", "84": "85s", "85": "85s",
           "86": "90s", "87": "90s", "88": "90s", "89": "90s", "90": "90s",
           "91": "95s", "92": "95s", "93": "95s", "94": "95s", "95": "95s",
           "96": "100s", "97": "100s", "98": "100s", "99": "100s", "100": "100s"}


class DataSet(object):
    def __init__(self):
        self.data = []
        self.loss_mid = 0    # 支出中位数
        self.gain_mid = 0    # 收益中位数
        self.len_data = 0


# 读取训练数据，并按收入是否大于50k分类
def classfy_traindata():
    dataset_low = DataSet()    # 收入<50k
    dataset_high = DataSet()   # 收入>50k

    # 数据处理,将数据按照收入分成两类，同时计算连续值的中位数
    gain = []
    loss = []
    with open("adult.data", "r") as f:
        line = f.readline()
        while line:
            line = line.replace("\n", "")
            if line:
                line = line.split(", ")
                if line[len(line) - 1] == ">50K":
                    dataset_high.data.append(line)
                    if int(line[10]) != 0:
                        gain.append(int(line[10]))
                    if int(line[11]) != 0:
                        loss.append(int(line[11]))
                else:
                    dataset_low.data.append(line)
                    if int(line[10]) != 0:
                        gain.append(int(line[10]))
                    if int(line[11]) != 0:
                        loss.append(int(line[11]))
            line = f.readline()

    # 获取部分中位数
    dataset_high.gain_mid = median(np.array(gain))
    dataset_high.loss_mid = median(np.array(loss))
    dataset_low.gain_mid = median(np.array(gain))
    dataset_low.loss_mid = median(np.array(loss))

    # 大于50k和小于50k样本数目
    dataset_high.len_data = len(dataset_high.data)
    dataset_low.len_data = len(dataset_low.data)

    return dataset_low, dataset_high


# 统计每一个特征每一个取值下的样本数目
def statistics(data):
    classfiled_data = {}     # 每一个特征下每一个取值分别的样本数目
    for character in characters:
        classfiled_data[character] = {}      # 赋初值
    for line in data.data:
        if len(line) < 10:
            continue
        for character in characters:
            if line[characters.index(character)] in classfiled_data[character]:
                classfiled_data[character][line[characters.index(character)]] += 1
            else:
                classfiled_data[character][line[characters.index(character)]] = 1

    return classfiled_data


# 将相似的多个特征值映射为1个
def tiny(a_list, character, new_name, data):
    if new_name not in data[character]:
        data[character][new_name] = 0
    for key in list(data[character]):
        if key in a_list and key != new_name:
            data[character][new_name] += data[character][key]
            del data[character][key]


# 对收益和支出进行离散化，分成none、high、low三类
def income_classfy(category, mid_value, data):
    data[category]["low"] = 0
    data[category]["high"] = 0
    data[category]["none"] = 0
    for key in list(data[category]):
        if key in ["none", "high", "low"]:
            continue
        if int(key) <= 0:
            data[category]["none"] += data[category][key]
        elif int(key) < mid_value:
            data[category]["low"] += data[category][key]
        else:
            data[category]["high"] += data[category][key]
        del data[category][key]


def tiny_hour(data):
    # 工作时长离散化
    for x in range(10):
        a_set = []
        for y in range(10 * (x + 1)):
            a_set.append(str(y + 1))
        tiny(a_set, "hr_peer_week", str(10 * (x + 1)) + "s", data)


def tiny_age(data):
    # 年龄离散化
    for x in range(20):
        a_set = []
        for y in range(5 * (x + 1)):
            a_set.append(str(y + 1))
        tiny(a_set, "age", str(5 * (x + 1)) + "s", data)


def test(line, dataset_low, dataset_high, classfiled_data_low, classfiled_data_high):
    p_low = dataset_low.len_data / (dataset_low.len_data + dataset_high.len_data)
    p_high = dataset_high.len_data / (dataset_high.len_data + dataset_low.len_data)

    gain = int(line[-5])
    loss = int(line[-4])

    for character in characters[: -1]:
        i = characters.index(character)
        if character in ["fnlwgt", "education_num"]:
            continue
        if line[i] in simplified_map:
            line[i] = simplified_map[line[i]]
        # 年龄
        if i == 0:
            line[i] = age_map[line[i]]
        # 工作时长
        if i == 12:
            line[i] = hour_map[line[i]]
        # 收益
        if character == "capital_gain":
            line[i] = get_level(gain, dataset_low.gain_mid)
        # 支出
        if character == "capital_loss":
            line[i] = get_level(loss, dataset_low.loss_mid)

        p_low *= classfiled_data_low[character][line[i]] / dataset_low.len_data    # 收入小于50k的概率

        if character == 'capital_gain':
            line[i] = get_level(gain, dataset_high.gain_mid)
        if character == 'capital_loss':
            line[i] = get_level(loss, dataset_high.loss_mid)

        p_high *= classfiled_data_high[character][line[i]] / dataset_high.len_data   # 收入大于50k的概率

    if p_low > p_high:
        return "<=50k"
    else:
        return ">50k"


def get_level(value, mid_value):
    if value <= 0:
        return "none"
    elif value < mid_value:
        return "low"
    else:
        return "high"


if __name__ == '__main__':
    dataset_low, dataset_high = classfy_traindata()
    print("训练数据的总数：\n >50k\t%d\n<=50k\t%d" % (len(dataset_high.data), len(dataset_low.data)))
    # 处理收入小于50k
    classfiled_data_low = statistics(dataset_low)

    # 工作类别上的合并
    tiny(['Never-worked', 'Without-pay'], 'type_employer', 'not-working', classfiled_data_low)
    tiny(['Local-gov', 'State-gov'], 'type_employer', 'other-govt', classfiled_data_low)
    tiny(['Self-emp-inc', 'Self-emp-not-inc'], 'type_employer', 'self-employed', classfiled_data_low)
    # 职业上的合并
    tiny(["Craft-repair", "Farming-fishing", "Handlers-cleaners", "Machine-op-inspct", "Transport-moving"],
         "occupation", 'blue-collar', classfiled_data_low)
    tiny(['Other-service', 'Priv-house-serv'], 'occupation', 'service', classfiled_data_low)
    # 国籍上的合并
    tiny(["Cambodia", "Laos", "Philippines", "Thailand", "Vietnam"], 'country', 'SE-Asia', classfiled_data_low)
    tiny(["Canada", "England", "India", "Ireland", "Scotland", ], 'country', 'British-Commonwealth',
         classfiled_data_low)
    tiny(['China', 'Hong', 'Taiwan'], 'country', 'China', classfiled_data_low)
    tiny(["Columbia", "Ecuador", "El-Salvador", "Peru"], 'country', 'South-America', classfiled_data_low)
    tiny(["Cuba", "Iran", "Japan"], 'country', 'other', classfiled_data_low)
    tiny(["Dominican-Republic", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua",
          "Outlying-US(Guam-USVI-etc)", "Puerto-Rico", "Trinadad&Tobago", ], 'country', 'Latin-America',
         classfiled_data_low)
    tiny(["France", "Germany", "Holand-Netherlands", "Italy", ], 'country', 'Euro_1', classfiled_data_low)
    tiny(["Greece", "Hungary", "Poland", "Portugal", "Yugoslavia", ], 'country', 'Euro_2', classfiled_data_low)
    # 学历上的合并
    tiny(["10th", "11th", "12th", "1st-4th", "5th-6th", "7th-8th", "9th", "Preschool", ], 'education', 'dropout',
         classfiled_data_low)
    tiny(['Assoc-acdm', 'Assoc-voc'], 'education', 'Assoc', classfiled_data_low)
    # 婚姻状况的合并
    tiny(["Married-AF-spouse", "Married-civ-spouse"], 'marital', "Married", classfiled_data_low)
    tiny(["Married-spouse-absent", "Separated", "Divorced"], 'marital', 'not-married', classfiled_data_low)

    del classfiled_data_low["education_num"]  # 删除多余属性
    del classfiled_data_low["fnlwgt"]

    income_classfy('capital_gain', dataset_low.gain_mid, classfiled_data_low)
    income_classfy('capital_loss', dataset_low.loss_mid, classfiled_data_low)

    tiny_hour(classfiled_data_low)
    tiny_age(classfiled_data_low)

    for key in classfiled_data_low:
        print(key)
        print(classfiled_data_low[key])

    # 处理收入大于50k
    classfiled_data_high = statistics(dataset_high)

    # 工作类别上的合并
    tiny(['Never-worked', 'Without-pay'], 'type_employer', 'not-working', classfiled_data_high)
    tiny(['Local-gov', 'State-gov'], 'type_employer', 'other-govt', classfiled_data_high)
    tiny(['Self-emp-inc', 'Self-emp-not-inc'], 'type_employer', 'self-employed', classfiled_data_high)
    # 职业上的合并
    tiny(["Craft-repair", "Farming-fishing", "Handlers-cleaners", "Machine-op-inspct", "Transport-moving"],
         "occupation", 'blue-collar', classfiled_data_high)
    tiny(['Other-service', 'Priv-house-serv'], 'occupation', 'service', classfiled_data_high)
    # 国籍上的合并
    tiny(["Cambodia", "Laos", "Philippines", "Thailand", "Vietnam"], 'country', 'SE-Asia', classfiled_data_high)
    tiny(["Canada", "England", "India", "Ireland", "Scotland", ], 'country', 'British-Commonwealth',
         classfiled_data_high)
    tiny(['China', 'Hong', 'Taiwan'], 'country', 'China', classfiled_data_high)
    tiny(["Columbia", "Ecuador", "El-Salvador", "Peru"], 'country', 'South-America', classfiled_data_high)
    tiny(["Cuba", "Iran", "Japan"], 'country', 'other', classfiled_data_high)
    tiny(["Dominican-Republic", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua",
          "Outlying-US(Guam-USVI-etc)", "Puerto-Rico", "Trinadad&Tobago", ], 'country', 'Latin-America',
         classfiled_data_high)
    tiny(["France", "Germany", "Holand-Netherlands", "Italy", ], 'country', 'Euro_1', classfiled_data_high)
    tiny(["Greece", "Hungary", "Poland", "Portugal", "Yugoslavia", ], 'country', 'Euro_2', classfiled_data_high)
    # 学历上的合并
    tiny(["10th", "11th", "12th", "1st-4th", "5th-6th", "7th-8th", "9th", "Preschool", ], 'education', 'dropout',
         classfiled_data_high)
    tiny(['Assoc-acdm', 'Assoc-voc'], 'education', 'Assoc', classfiled_data_high)
    # 婚姻状况的合并
    tiny(["Married-AF-spouse", "Married-civ-spouse"], 'marital', "Married", classfiled_data_high)
    tiny(["Married-spouse-absent", "Separated", "Divorced"], 'marital', 'not-married', classfiled_data_high)

    del classfiled_data_high["education_num"]  # 删除多余属性
    del classfiled_data_high["fnlwgt"]

    income_classfy('capital_gain', dataset_high.gain_mid, classfiled_data_high)
    income_classfy('capital_loss', dataset_high.loss_mid, classfiled_data_high)

    tiny_hour(classfiled_data_high)
    tiny_age(classfiled_data_high)

    for key in classfiled_data_high:
        print(key)
        print(classfiled_data_high[key])

    with open('adult.test', 'r') as f:
        line = f.readline()
        right = 0
        wrong = 0
        while line:
            if len(line) < 25:
                line = f.readline()
                continue
            line = line.replace("\n", "")
            # line = line[: -1]  # 去除数据最后面的.
            line = line.split(", ")
            ans = test(line, dataset_low, dataset_high, classfiled_data_low, classfiled_data_high).upper()
            # print(ans)
            # print(line[-1])
            if line[-1] == ans:
                right += 1
            else:
                wrong += 1
            line = f.readline()

    print("模型的判断正确的次数：\t%d\n错误的次数\t%d\n正确率:\t%f" % (right, wrong, (right / (right + wrong))))



