import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR

df_state = pd.read_csv('state-date-total-data.csv')
arr_state = df_state.to_numpy() # still reversed
arr_state = np.flipud(arr_state) # now taken data from day-1 to day-52; but still daily cases
arr_state = np.cumsum(arr_state, axis=0) # now cumulative cases till day 52
np.savetxt("state-date-total-data-cumulative.csv", arr_state.astype(int), fmt='%i', delimiter=",")

X = np.arange(1,53)
X = np.reshape(X, (52,1))

for i in range(len(arr_state)):
	y = arr_state[:,i]
	x_test = np.arange(1,56).reshape(55,1)
	clf = SVR(C=1.0, epsilon=0.2)
	clf.fit(X, y)
	y_test = clf.predict(x_test)

	plt.scatter(X, y, color='black')
	plt.plot(x_test,y_test)
	plt.show()



