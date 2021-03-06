# -*- coding: utf-8 -*-
"""Power.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h_LEQ4thcAfIedR2XHf3MXTVIGRlzEvf
"""

import pandas as pd
import numpy as np

train=pd.read_csv("train.csv")
test=pd.read_csv("test.csv")

train.drop(columns=["Unnamed: 0"],inplace=True)
test.drop(columns=["Unnamed: 0"],inplace=True)

x=train.drop(columns=["PE"])
y=train["PE"]

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_squared_error

import xgboost as xgb

import lightgbm

from sklearn.model_selection import KFold

kfold,scores=KFold(n_splits=10,shuffle=True,random_state=27),[]
Actual_preds=[]
i=1
for trainn, testt in kfold.split(x):
        x_train, x_test = x.iloc[trainn], x.iloc[testt]
        y_train, y_test = y.iloc[trainn], y.iloc[testt]
        
        model = xgb.XGBRegressor(n_estimators=1000,max_depth=6,colsample_bytree=1,subsample=1,learning_rate=0.1,min_child_weight=2)
        model.fit(x_train,y_train,eval_set=[(x_test,y_test)])

        preds =model.predict(x_test)
        score = (mean_squared_error(y_test, preds))**0.5
        scores.append(score)
        realpreds = model.predict(test.drop(columns=["PE"]))
        Actual_preds.append(realpreds)
        
        print(score)
print("AVERAGE SCORE: ", sum(scores)/len(scores))

pred=model.predict(test.drop(columns=["PE"]))

preds = np.mean(Actual_preds,0)
liv= pd.DataFrame(preds)

kfold,scores=KFold(n_splits=10,shuffle=True,random_state=27),[]
Actual_preds=[]
i=1
for trainn, testt in kfold.split(x):
        x_train, x_test = x.iloc[trainn], x.iloc[testt]
        y_train, y_test = y.iloc[trainn], y.iloc[testt]
        
        model = lightgbm.LGBMRegressor()
        model.fit(x_train,y_train)

        preds =model.predict(x_test)
        score = (mean_squared_error(y_test, preds))**0.5
        scores.append(score)
        realpreds = model.predict(test.drop(columns=["PE"]))
        Actual_preds.append(realpreds)
        
        print(score)
print("AVERAGE SCORE: ", sum(scores)/len(scores))

preds = np.mean(Actual_preds,0)
livlight= pd.DataFrame(preds)

test['PE']=(0.5*liv)+(0.5*livlight)

test['PE'].to_csv("lightxgb.csv",index=False)