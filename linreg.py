import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df_state = pd.read_csv('state-date-total-data.csv')
arr_state = df_state.to_numpy() # still reversed
arr_state = np.flipud(arr_state) # now taken data from day-1 to day-52; but still daily cases
arr_state = np.cumsum(arr_state, axis=0) # now cumulative cases till day 52
np.savetxt("state-date-total-data-cumulative.csv", arr_state.astype(int), fmt='%i', delimiter=",")

X = np.arange(1,53)
X = np.reshape(X, (52,1))

for i in range(len(arr_state[0])):

	y = arr_state[:,i]
	y = np.reshape(y, (52,1))
	reg = LinearRegression().fit(X, y)
	x_test = np.arange(1,56).reshape(55,1)
	y_test = reg.predict(x_test)
	plt.scatter(X, y, color='black')
	plt.plot(x_test,y_test)
	plt.show()



############ EXAMPLE CODE ##########################
# X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
# y = 1 * x_0 + 2 * x_1 + 3
# y = np.dot(X, np.array([1, 2])) + 3
# reg = LinearRegression().fit(X, y)
# reg.score(X, y)

# reg.coef_

# reg.intercept_

# a =reg.predict(np.array([[3, 5]]))

# print(a)



