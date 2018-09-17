from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error
import numpy as np


#X,y = make_regression(n_features=20, n_informative=2, random_state=0, shuffle=False)

#print(X)
#print('\n')
#print(y)
#
#regr = RandomForestRegressor(max_depth=1000, random_state=0)
#regr.fit(X, y)
#print(regr.predict([X[0]]))

def random_forests(X_test,y_test,X_train,y_train):
	regr = RandomForestRegressor(max_depth=1000, random_state=0)
	regr.fit(X_train, y_train)
	results = []
	for i in range(len(X_test)):
		#print("Score: ", y_test[i], " | Predicition: ", regr.predict([X_test[i]])[0])
		results.append(regr.predict([X_test[i]])[0])
	print(pearsonr(y_test, results))
	print(mean_squared_error(y_test, results))