#!/usr/bin/env python
# coding: utf-8

# In[19]:


# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR


# In[16]:


# Flags
linear_reg = True
sv_reg = True


# In[6]:


# Directory variables
data_dir = 'data/'


# In[8]:


# Read state data
df_state = pd.read_csv(data_dir + 'state-date-total-data.csv')
arr_state = df_state.to_numpy() # still reversed
arr_state = np.flipud(arr_state) # now taken data from day-1 to day-52; but still daily cases
arr_state = np.cumsum(arr_state, axis=0) # now cumulative cases till day 52
np.savetxt(data_dir + 'state-date-total-data-cumulative.csv', arr_state.astype(int), fmt='%i', delimiter=",")


# In[17]:


if linear_reg:
    # Get x and y plots - LinearRegression
    X = np.arange(1,53)
    X = np.reshape(X, (52,1))
    print (arr_state.shape)

    for i in range(len(arr_state[0])):
        y = arr_state[:,i]
        y = np.reshape(y, (52,1))
        reg = LinearRegression().fit(X, y)
        x_test = np.arange(1,56).reshape(55,1)
        y_test = reg.predict(x_test)
        plt.scatter(X, y, color='black')
        plt.plot(x_test,y_test)
        plt.show()


# In[21]:


if sv_reg:
    # Get x and y plots - SVRegression
    X = np.arange(1,53)
    X = np.reshape(X, (52,1))

    for i in range(len(arr_state[0])):
        y = arr_state[:,i]
        x_test = np.arange(1,56).reshape(55,1)
        clf = SVR(C=1.0, epsilon=0.2)
        clf.fit(X, y)
        y_test = clf.predict(x_test)

        plt.scatter(X, y, color='black')
        plt.plot(x_test,y_test)
        plt.show()


# In[ ]:




