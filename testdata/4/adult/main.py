# -*- coding: utf-8 -*-

"""
Create on 12.14.2017
@author:zouxi
"""

from DecisionTrees import *
import numpy as np
import pandas as pd
import sys
import importlib
importlib.reload(sys)


# 数据预处理，主要是连续值处理成离散值
def prepareData(train_data_file_path, test_data_file_path):
    """
    数据预处理，主要是连续值处理成离散值
    :param train_data_file_path: 训练数据集路径
    :param test_data_file_path: 测试数据集路径
    :return:
    """
    print("prepare data......")
    continue_feature_list = [0, 2, 4, 10, 11, 12]    # 连续值特征对应的下标
    bins = [10, 12, 8, 12, 12, 12]    # 每一个连续值划分的区间数
    data = []
    training_size = 0
    with open(train_data_file_path, encoding="utf-8") as f:         # 训练集
        dataList = f.read().splitlines()
    for datai in dataList:
        training_size += 1
        datai_feature_list = datai.split(", ")
        data.append(np.array(datai_feature_list))

    with open(test_data_file_path, encoding="utf-8") as f:        # 测试集
        dataList = f.read().splitlines()
    for datai in dataList:
        datai_feature_list = datai.split(", ")
        data.append(np.array(datai_feature_list))

    data = np.array(data)
    print(data.shape)
    discretizedData = discretizeData(data, continue_feature_list, bins)

    # 返回训练集和测试集
    print("training_size:", training_size)
    return discretizedData[:training_size, :], discretizedData[training_size:, :]


# 离散化数据
def discretizeData(data, continue_feature_list, bins):
    """
    离散化数据
    :param data: 数据集
    :param continue_feature_list: 连续特征对应下标列表
    :param bins: # 每一个连续值划分的区间数
    :return:
    """
    for feature_i_index in range(len(continue_feature_list)):
        feature = continue_feature_list[feature_i_index]
        data_of_feature_i = np.array([float(rowi) for rowi in data[:, feature]])   # 注意将str转为float
        discretized_feature_i = discretizeFeature(data_of_feature_i, bins[feature_i_index])
        #print(discretized_feature_i)
        data[:, feature] = np.array(discretized_feature_i)    # 用离散值代替连续值

    return data


# 离散化某一特征
def discretizeFeature(data_of_feature, bin_num):
    """
    离散化某一特征
    :param data_of_feature: 某一特征对应的值
    :param bin_num: 划分的区间数
    :return:
    """
    return pd.cut(data_of_feature, bin_num, labels=False)


# 测试一条记录
def test_piece_of_data(apiece_of_data, tree, attributes, target):
    """
    测试一条记录
    :param apiece_of_data: 一条数据
    :param tree: 决策树
    :param attributes: 特征属性列表
    :param target: 目标值
    :return:
    """
    target_index = attributes.index(target)
    true_label = apiece_of_data[target_index]
    while isinstance(tree, dict):
        tree_key = list(tree.keys())[0]    # 根节点
        # print("tree key:", tree_key)
        # print(type(tree_key))
        tree_key_index = attributes.index(tree_key)
        data_value_of_key = apiece_of_data[tree_key_index]
        try:
            if data_value_of_key in tree[tree_key]:
                if isinstance(tree[tree_key][data_value_of_key], dict):
                    tree = tree[tree_key][data_value_of_key]
                else:
                    if tree[tree_key][data_value_of_key] == true_label:
                        return True
                    else:
                        return False
            else:    # 这种情况决策树不能预测
                return "<=50K" == true_label
        except:
            print("error here")


# 在测试集上测试模型准确率
def testing(test_data, tree, attributes, target):
    """
    在测试集上测试模型准确率
    :param test_data: 测试集
    :param tree: 决策树
    :param attributes: 特征属性列表
    :param target: 目标值
    :return:
    """
    all_count = 0.0
    right_count = 0.0
    data_len = test_data.shape[0]
    for i in range(data_len):
        all_count += 1
        if test_piece_of_data(test_data[i, :], tree, attributes, target):
            right_count += 1

    return right_count / all_count


def main():
    print("Begin")
    #
    #
    # rs = open('./adult1.data', 'w')
    #
    # with open('./adult.data') as file:
    #     for line in file:
    #         if '?' in line:
    #             continue
    #         else:
    #             rs.write(line)
    # rs.close()
    #
    #
    #
    # rs = open('./adult1.test', 'w')
    #
    # with open('./adult.test') as file:
    #     for line in file:
    #         if '?' in line:
    #             continue
    #         else:
    #             rs.write(line)
    # rs.close()




    train_data_file_path = "adult1.data"
    test_data_file_path = "adult1.test"
    train_data, test_data = prepareData(train_data_file_path, test_data_file_path)   # 处理后的训练集和测试集
    print(train_data)
    print(type(train_data))
    continue_feature_list = [0, 2, 4, 10, 11, 12]  # 连续值特征对应的下标
    dictt={}
    for i in range(15):
        if i not in continue_feature_list:
            dictt[str(i)] = []
            for row in range(train_data.shape[0]):

                if train_data[row,i] not in dictt[str(i)]:
                    dictt[str(i)].append(train_data[row,i])
                    train_data[row, i] = str(len(dictt[str(i)])-1)
                else:
                    train_data[row,i]=str(dictt[str(i)].index(train_data[row,i]))
            print(dictt[str(i)])
    print(train_data)
    print(train_data.shape)
    np.savetxt("1.in", train_data, fmt="%s", delimiter=" ")
    np.savetxt("1.out", train_data[:,14], fmt="%s", delimiter=" ")

    train_data=test_data
    for i in range(15):
        if i not in continue_feature_list:
            for row in range(train_data.shape[0]):

                if train_data[row,i] not in dictt[str(i)]:
                    dictt[str(i)].append(train_data[row,i])
                    train_data[row, i] = str(len(dictt[str(i)])-1)
                else:
                    train_data[row,i]=str(dictt[str(i)].index(train_data[row,i]))
            print(dictt[str(i)])

    print(train_data)
    print(train_data.shape)
    np.savetxt("2.in", train_data, fmt="%s", delimiter=" ")
    np.savetxt("2.out", train_data[:,14], fmt="%s", delimiter=" ")




    # M = 15    # 特征数+目标值
    # attributes = []
    # depth = 0
    # for i in range(M):
    #     attributes.append("#" + str(i + 1))
    # target = "#15"
    # print("attributes:", attributes)
    #
    # tree = make_tree(train_data, attributes, target, depth)   # 构建决策树
    # print("Finish making tree")
    # print(tree)
    #
    # # 测试
    # print("testing")
    # precision = testing(test_data, tree, attributes, target)
    # print("precision:", precision)


if __name__ == '__main__':
    main()
