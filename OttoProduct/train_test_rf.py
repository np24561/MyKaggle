
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")
from scipy.stats import randint as sp_randint

import xgboost as xgb
import sklearn.preprocessing as skpreprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import RandomizedSearchCV

def train(seed,criterion):
    # ------------------------ load and prepare the data
    train_csv = pd.read_csv("train.csv",index_col = "id")
    Xtrain = train_csv.iloc[:,xrange(93)]
    train_labels = train_csv.loc[:,"target"]

    labelencoder = skpreprocess.LabelEncoder()
    ytrain = labelencoder.fit_transform(train_labels)

    # ------------------------ prepare the estimator
    param_dist = {"n_estimators":  sp_randint(500,3000),              
                  "max_depth": [2,3, 4,5,6,None],
                  "min_samples_leaf": [5,10,20,30,40,50]}
    njobs = 4
    rf = RandomForestClassifier(oob_score=True,verbose=1,n_jobs=njobs,
                                random_state=seed,criterion=criterion)
    searchcv = RandomizedSearchCV(estimator=rf, param_distributions=param_dist,
                                  scoring = "log_loss",random_state=seed,                                  
                                  n_iter=200,n_jobs=njobs)

    # ------------------------ search the best parameters
    print "#################### search cv begins"
    searchcv.fit(Xtrain,ytrain)    
    print "#################### search cv ends"
    print "best score: ",searchcv.best_score_                                  
    print "best parameters: ",searchcv.best_params_

    # ------------------------ cross-validation to estimate generalization error
