# coding:utf8
import pandas as pd
from sklearn import linear_model
import numpy as np

if __name__ == '__main__':

    test_data = pd.read_csv('test.csv',index_col=0)
    test_data = test_data.fillna(test_data.mean())
    test_data = pd.get_dummies(test_data)

    raw_data = pd.read_csv('train.csv',index_col=0)
    raw_data = raw_data.fillna(raw_data.mean())
    train_data = pd.get_dummies(raw_data)

    # align the DataFrame
    for col in train_data:
        if col not in test_data and col != "SalePrice":
            del train_data[col]
    sale = train_data.pop("SalePrice")
    train_data.insert(train_data.shape[1],"SalePrice",sale)

    # train_col = train_data.columns
    # test_col = test_data.columns
    # for i in xrange(len(train_col)-1):
    #     if(train_col[i] == test_col[i]):
    #         print train_col[i]
    # test_data.to_csv('test_fix.csv')
    # train_data.to_csv('train_fix.csv')

    # train
    reg = linear_model.Ridge(alpha=1,normalize=True)
    reg.fit(train_data.iloc[:,:-1], train_data['SalePrice'])
    # print sorted(abs(reg.coef_))
    linear_model.RidgeCV(fit_intercept=True,normalize=True)
    # predict
    res = np.array(reg.predict(test_data))
    res_csv = pd.read_csv('sample_submission.csv')
    res_csv['SalePrice'] = res
    res_csv.to_csv('out.csv', index=None)

