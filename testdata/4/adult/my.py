import sys
import os
import time
import numpy as np
import sklearn as sk
import pandas as pd
from sklearn.metrics import roc_auc_score

cnt=1
if __name__ == "__main__":
    strin = input()
    data=np.array(strin.split( )).astype('float')
    while True:
        try:
            cnt=cnt+1
            strin = input()
            if '?' in strin:
                strin=strin.replace('?','0')
            strnp=np.array(strin.split( )).astype('float')
            data=np.vstack((data, strnp))
        except Exception as e:
            break

    #print(cnt)
    #print(data.shape)

    from sklearn import preprocessing
    """
    公式为：(X-mean)/std  计算时对每个属性/每列分别进行。
    将数据按期属性（按列进行）减去其均值，并处以其方差。得到的结果是，对于每个属性/每列来说所有数据都聚集在0附近，方差为1。
    """

    # X = np.array(data)
    # X_scaled = preprocessing.scale(X)
    X_train=data[:,:-1]
    y_train=data[:,14:15]
    X_train = preprocessing.scale(X_train)

    #print(X_train.shape)
    #print(y_train.shape)

    from sklearn import tree

    clf = tree.DecisionTreeClassifier(criterion='gini')
    clf = clf.fit(X_train, y_train)
    result=clf.predict_proba(X_train)
    #print(result.shape)
    for re in result:
        print(re)

    #print(roc_auc_score(actual, y_score))
    print(clf.score(X_train, y_train))
