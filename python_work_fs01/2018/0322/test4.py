#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy  import array
from sklearn.datasets import load_boston
from pymatgen import Composition, Element
from numpy import zeros, mean
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn import linear_model, metrics, ensemble
trainFile = open("tc.csv","r").readlines()

materials = []
tc        = []
pf3= []

for line in trainFile:
    split = str.split(line, ',')
    material = Composition(split[0])
    pressure = float(split[4])
    tc.append(float(split[8]))
    features = []
    atomicNo = []
    natom = []

    for element in material:
        natom.append(material.get_atomic_fraction(element)*material.num_atoms)
        atomicNo.append(float(element.Z))

    features.extend(atomicNo)
    features.extend(natom)
    features.append(pressure)
    pf3.append(features[:])

# sklearn NO random forest KAIKI
rfr = ensemble.RandomForestRegressor(n_estimators=10)

# KOUSA KENSHO SIMASU
cv = ShuffleSplit(n_splits=10, test_size=0.1, random_state=0)
sp = cross_val_score(rfr,pf3,tc, cv=cv, scoring='neg_mean_absolute_error')
print("MAE by RF with physical 3 data: "+ str(round(abs(mean(sp)), 3)) + " K")


X = pf3[:]
y = tc[:]

# from sklearn.model_selection import train_test_split
# (X_train, X_test, y_train, y_test) = train_test_split(X,y,test_size = 0.3,random_state = 666)
X_train = X[:]
y_train = y[:]

X_test = [ \
[57.0, 1.0, 1.0,10.0, 210.0], \
[12.0, 1.0, 1.0, 6.0, 300.0],  \
[39.0, 1.0, 1.0, 6.0, 120.0], \
[20.0, 1.0, 1.0, 6.0, 150.0],  \
[14.0, 1.0, 1.0, 8.0, 250.0], \
[82.0, 1.0, 1.0, 8.0, 230.0],  \
[33.0, 1.0, 1.0, 8.0, 450.0], \
[51.0, 1.0, 1.0, 4.0, 150.0],  \
[83.0, 1.0, 1.0, 5.0, 300.0], \
[83.0, 1.0, 1.0, 6.0, 300.0],  \
]
y_test =[ 286, 271, 264, 235, 107, 107, 151, 118, 119, 113]
# LaH10 210GPa 286 K
# MgH6  300GPa 271 K
#  YH6  120GPa 264 K
# CaH6  150GPa 235 K
# SiH8  250GPa 107 K
# PbH8  230GPa 107 K
# AsH8  450GPa 151 K
# SbH4  150GPa 118 K
# BiH5  300GPa 119 K
# BiH6  300GPa 113 K


from sklearn.ensemble import RandomForestRegressor
forest = RandomForestRegressor(n_estimators=16,max_depth=11)
forest.fit(X_train,y_train)
# print("X_train",X_train)
# print("y_train",y_train)

# from sklearn.model_selection import GridSearchCV
# params = {'n_estimators' : [3, 10, 100, 1000, 10000], 'n_jobs': [-1]}
# 
# mod = RandomForestRegressor()
# cv = GridSearchCV(mod, params, cv = 10, scoring = 'neg_mean_squared_error', n_jobs = 1)
# cv.fit(X_train, y_train)

y_train_pred = forest.predict(X_train)
y_test_pred = forest.predict(X_test)
print("X_test",X_test)
print("y_test",y_test)
print("y_test_pred",y_test_pred)

from sklearn.metrics import mean_squared_error
print('MSE train : %.3f, test : %.3f' % (mean_squared_error(y_train,y_train_pred),mean_squared_error(y_test,y_test_pred)))
from sklearn.metrics import r2_score
print('R^2 train : %.3f, test : %.3f' % (r2_score(y_train,y_train_pred),r2_score(y_test,y_test_pred)))
