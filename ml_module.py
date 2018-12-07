from sklearn.svm import SVR
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error
import numpy as np

#TRAIN SVR MODULE WITH TRAINING CORPUS AND TEST THAT MODULE WITH TEST CORPUS
def svr(X_test,y_test,X_train,y_train):
	svr = SVR(kernel='rbf', C=1e3, gamma=0.1)
	svr.fit(X_train, y_train)
	results = []
	for i in range(len(X_test)):
		results.append(svr.predict([X_test[i]])[0])
	return [y_test, results]