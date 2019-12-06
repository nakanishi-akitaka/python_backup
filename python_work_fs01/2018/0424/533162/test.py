#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set foldmethod=marker:

# modules
# {{{
import numpy as np
import pandas as p
from sklearn.svm import SVR
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.externals import joblib
# }}}
#
# function read X, y from file (short)
# {{{
def read_file(name): 
    data = np.array(p.read_csv(filepath_or_buffer=name,header=None,sep=','))[:,:]
    y=data[:,0]
    X=data[:,1:]
    return X, y
# }}}
#
# function print score of learning and prediction 
# {{{
def print_score(mod, X, y_test):
    y_pred = mod.predict(X)
    rmse =  np.sqrt(mean_squared_error(y_test, y_pred))
    mae  = mean_absolute_error(y_test, y_pred)
    rmae  = np.sqrt(mean_squared_error(y_test, y_pred))/mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test,y_pred)
    print("RMSE, MAE, RMSE/MAE, R^2 = %.3f, %.3f, %.3f, %.3f" % (rmse, mae, rmae, r2))
# }}}
#
# function print score of grid search
# {{{
def print_search_score(grid_search):
    print('search score')
    print('best_score  :', grid_search.best_score_)
    print('best_params :', grid_search.best_params_)
# }}}

train_file = input('train_file = \n')
test_file = input('test_file = \n')
X_train, y_train = read_file(train_file)
X_test,  y_test  = read_file(test_file)
#
# parameter optimization (Grid Search)
# {{{
print('')
print('# SVR with GridSearched hyper parameters')
# step 1. model
svr = SVR()

# step 2. learning with optimized parameters and save model
# search range
range_c =  [i*10**j for j in range(-2,2) for i in range(1,10)]
range_g =  [i*10**j for j in range(-2,2) for i in range(1,10)]
range_d =  [i for i in range(1,3)]
param_grid = [
{'kernel':['linear'], 'C': range_c},
{'kernel':['rbf'],    'C': range_c, 'gamma': range_g},
{'kernel':['sigmoid'],'C': range_c, 'gamma': range_g}]
# {'kernel':['poly'],   'C': range_c, 'gamma': range_g, 'degree':range_d}]

grid_search = GridSearchCV(svr,param_grid, n_jobs=-1, scoring='r2')
grid_search.fit(X_train, y_train)
print_search_score(grid_search)
joblib.dump(grid_search,'model.pkl')

# step 3. load model and predict
mod = joblib.load('model.pkl')
y_pred = mod.predict(X_test)

# step 4. score
print("learning   score: ",end="")
print_score(mod, X_train, y_train)
print("prediction score: ",end="")
print_score(mod, X_test, y_test)
