# -*- coding: utf-8 -*-

"""
Create on 12.13.2017
@author: zouxi
"""

import numpy as np
import copy
import sys
import importlib
importlib.reload(sys)


# return the majority of the label
def majority(data, attributes, target):
    """
    return the majority of the label
    :param data: 数据集
    :param attributes: 特征属性列表
    :param target: 目标值
    :return: 集合中占多数的类别
    """
    target_index = attributes.index(target)      # 目标值对应的下标
    valFreq = {}    # 每个目标值对应的样本数目

    for i in range(data.shape[0]):
        if data[i, target_index] in valFreq:
            valFreq[data[i, target_index]] += 1
        else:
            valFreq[data[i, target_index]] = 1

    maxLabel = 0
    major = ""
    for label in valFreq.keys():
        if valFreq[label] > maxLabel:
            maxLabel = valFreq[label]
            major = label

    return major


# 计算信息熵
def get_entropy_data(data, attributes, target, rows):
    """
    计算信息熵
    :param data: 数据集
    :param attributes: 特征属性列表
    :param target: 目标值
    :param rows:
    :return:信息熵
    """
    data_len = data.shape[0]
    target_index = attributes.index(target)
    target_list = [data[i, target_index] for i in range(data_len) if rows[i] == 1]
    target_set = set(target_list)   # 目标值类别数
    len_of_each_target_value = []
    for target_val in target_set:
        len_of_each_target_value.append(target_list.count(target_val))

    entropy_data = 0.0
    for target_count in len_of_each_target_value:
        entropy_data += -target_count * 1.0 / sum(len_of_each_target_value) * np.log(target_count * 1.0 / sum(len_of_each_target_value))

    return entropy_data * sum(rows) * 1.0 / len(rows)


# 计算按某个属性划分后的信息熵
def get_excepted_entropy_data(data, attributes, attri, target):
    """
    计算按某个属性划分后的信息熵
    :param data: 数据集
    :param attributes: 特征属性列表
    :param attri: 选择的划分属性
    :param target: 目标值
    :return: 计算按某个属性划分后的信息熵
    """
    attri_index = attributes.index(attri)
    attri_value_set = set(data[:, attri_index])    # 选择的划分属性的类别数
    data_len = data.shape[0]
    sum_excepted_entropy = 0.0

    for attri_value in attri_value_set:
        attri_selected_rows = np.zeros(data_len)
        for i in range(data_len):
            if data[i, attri_index] == attri_value:
                attri_selected_rows[i] = 1
        sum_excepted_entropy += get_entropy_data(data, attributes, target, attri_selected_rows)

    return sum_excepted_entropy


# 信息增益
def infoGain(data, attributes, attri, target):
    entropy_data = get_entropy_data(data, attributes, target, rows=np.ones(data.shape[0]))
    excepted_entropy_data = get_excepted_entropy_data(data, attributes, attri, target)
    return entropy_data - excepted_entropy_data


# ID3算法
def best_split(data, attributes, target):
    max_info = 0.000001
    best_attri = ""
    print("include attriburtes:")
    print(attributes)
    print("data_len:", data.shape[0])

    for attri in attributes:
        if attri != target:
            attri_infoGain = infoGain(data, attributes, attri, target)
            if attri_infoGain > max_info:
                max_info = attri_infoGain
                best_attri = attri

    print("max info_Gain:", max_info)
    print("split attri:", best_attri)

    return best_attri


# 最优划分属性对应的类别集合
def get_value(data, attributes, best_attri):
    """
    :param data:
    :param attributes:
    :param best_attri:
    :return:
    """
    best_attri_index = attributes.index(best_attri)
    return set(data[:, best_attri_index])


# 在最优划分属性下“类别=val”的样本数据集合
def get_example(data, attributes, best_attri, val):
    best_attri_index = attributes.index(best_attri)
    data_len = data.shape[0]
    subset_data = []
    for i in range(data_len):
        if data[i, best_attri_index] == val:
            subset_data.append(np.concatenate([data[i, 0:best_attri_index], data[i, (best_attri_index+1):]]))

    return np.array(subset_data)


# 构造决策树
def make_tree(data, attributes, target, depth):
    """
    构造决策树
    :param data:数据集
    :param attributes:特征属性列表
    :param target: 目标值
    :param depth: 树的深度
    :return:
    """
    print("depth:", depth)
    depth += 1
    target_index = attributes.index(target)
    val = [record[target_index] for record in data]     # 目标值
    label_prediction = majority(data, attributes, target)

    if len(data) <= 1:
        return label_prediction
    # 第一种情况，当前集合中的元素都属于同一类
    elif val.count(val[0]) == len(val):
        return val[0]
    else:
        best_attri = best_split(data, attributes, target)
        print("best attri:", best_attri)
        # 第二种情况，没有特征可以选择了
        if best_attri == "":
            return label_prediction
        # 否则创建一棵新的子决策树
        tree = {best_attri: {}}     # 根节点
        for val in get_value(data, attributes, best_attri):
            examples = get_example(data, attributes, best_attri, val)
            # 第三种情况，当前特征值对应的集合为空，创建叶节点，并标记为父节点中较多者的那一类
            if examples.shape[0] == 0:
                return label_prediction
            else:
                newAttri = copy.copy(attributes)
                newAttri.remove(best_attri)
                subTree = make_tree(examples, newAttri, target, depth)
                tree[best_attri][val] = subTree

    return tree
