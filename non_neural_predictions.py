#!/usr/bin/env python
# coding: utf-8

# In[81]:


# Imports
import numpy as np
import pandas as pd
import importlib as imp
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import accuracy_score


# In[46]:


# User module imports
from utils import district_daily_data as dd
dd = imp.reload(dd)


# In[52]:


# Flags
linear_reg = False
sv_reg = True
episodes = True


# In[41]:


# Directory variables
data_dir = 'data/'


# In[32]:


# Read state data
df_state = pd.read_csv(data_dir + 'state-date-total-data.csv')
arr_state = df_state.to_numpy() # still reversed
arr_state = np.flipud(arr_state) # now taken data from day-1 to day-52; but still daily cases
arr_state = np.cumsum(arr_state, axis=0) # now cumulative cases till day 52
np.savetxt(data_dir + 'state-date-total-data-cumulative.csv', arr_state.astype(int), fmt='%i', delimiter=",")


# In[55]:


# Read district data
districts = dd.get_all_districts()
dist_series = []  # [(start_date, series), (start_date, series), ...]
# Note: start_date might itself be a feature
for d in districts:
    d_start_date = dd.get_infection_start(d)
    dist_series.append((d_start_date, dd.get_district_time_series(d, d_start_date)))


# In[39]:


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


# In[43]:


if sv_reg and not episodes:
    # Get x and y plots - SVRegression
    X = np.arange(1,53)
    X = np.reshape(X, (52,1))

    for i in range(len(arr_state[0])):
        y = arr_state[:,i]
        x_test = np.arange(1,56).reshape(55,1)
        clf = SVR(C=100.0, gamma=100)
        clf.fit(X, y)
        y_test = clf.predict(x_test)

        plt.scatter(X, y, color='black')
        plt.plot(x_test,y_test)
        plt.show()


# In[87]:


if episodes:
    # Construct train and test data and fit Support Vector Regression
    x = []
    y = []
    episode_length = 7
    count = 0
    for tup in dist_series:
        series = tup[1]
        num_episodes = len(series) - episode_length + 1
        if num_episodes < 2: continue
        for _in in range(num_episodes-1):
            x.append(series[_in:_in+episode_length])
            y.append(series[_in+episode_length])
    x = np.array(x)
    y = np.array(y)

    train_length = int(0.8*len(x))
    x_train = x[:train_length]
    y_train = y[:train_length]
    x_test = x[train_length:]
    y_true = y[train_length:]
    clf = SVR(C=1.0, gamma='auto')
    clf.fit(x_train, y_train)
    
    y_test = clf.predict(x_test)
    X = np.arange(len(y_test))
    X = np.reshape(X, (len(y_test), 1))
    plt.plot(X, y_true, color='black')
    plt.plot(X, y_test, color='red')


# In[ ]:




