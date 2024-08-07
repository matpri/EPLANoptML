# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:09:15 2024

@author: MPrina
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler

df_hist = pd.read_csv('history_csv_random_sim.csv')
df_hist = df_hist.loc[df_hist['Total annual costs [Meuro]'] < 500000]
del df_hist['Unnamed: 12']

Npop = 200
Ngen_list = [i for i in range(1, 30)]

# Define the number of runs for each model
num_runs = 5

models_out = {
    'Linear Regression Avg': [],
    'Linear Regression CI': [],
    'Decision Tree Avg': [],
    'Decision Tree CI': [],
    'Random Forest Avg': [],
    'Random Forest CI': [],
    # 'XGBoost Avg': [],
    # 'XGBoost CI': [],
    'Neural Network, Hidden Layer=50 Avg': [],
    'Neural Network, Hidden Layer=50 CI': [],
    'Neural Network, Hidden Layer=100 Avg': [],
    'Neural Network, Hidden Layer=100 CI': [],
    'Neural Network, Hidden Layer=200 Avg': [],
    'Neural Network, Hidden Layer=200 CI': [],
    'Neural Network, Hidden Layer=500 Avg': [],
    'Neural Network, Hidden Layer=500 CI': [],
}

for a in range(len(Ngen_list)):
    Ngen = Ngen_list[a]
    print('-------------------', Ngen)

    X_train = df_hist.iloc[0:Ngen * Npop, :10]
    X_test = df_hist.iloc[Ngen * Npop:, :10]
    Y_train = df_hist.iloc[0:Ngen * Npop, -2:]
    Y_test = df_hist.iloc[Ngen * Npop:, -2:]

    scaler_X = StandardScaler()
    X_train = scaler_X.fit_transform(X_train)
    X_test = scaler_X.transform(X_test)

    scaler_Y = StandardScaler()
    Y_train = scaler_Y.fit_transform(Y_train)
    Y_test = scaler_Y.transform(Y_test)

    # Define different models
    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(),
        'Random Forest': RandomForestRegressor(),
        # 'XGBoost': XGBRegressor(random_state=42),
        'Neural Network, Hidden Layer=50': MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=500, random_state=42),
        'Neural Network, Hidden Layer=100': MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=500, random_state=42),
        'Neural Network, Hidden Layer=200': MLPRegressor(hidden_layer_sizes=(200, 200), max_iter=500, random_state=42),
        'Neural Network, Hidden Layer=500': MLPRegressor(hidden_layer_sizes=(500, 500), max_iter=500, random_state=42),
    }

    for name, model in models.items():
        r2_scores = []
        for run in range(num_runs):
            model.random_state = run + 1  # Set different random states for each run
            model.fit(X_train, Y_train)
            predictions = model.predict(X_test)
            r2 = max(0, min(r2_score(Y_test, predictions), 1)) * 100
            r2_scores.append(r2)
        average_r2 = np.mean(r2_scores)
        confidence_range = np.std(r2_scores) * 2  # 95% confidence interval
        models_out[name + ' Avg'].append(average_r2)
        models_out[name + ' CI'].append(confidence_range)

# Create DataFrame to store the results
dff = pd.DataFrame(models_out)
dff['Ngen'] = Ngen_list

# Save to Excel
name_excel = 'output_random_more_models_new2.xlsx'
with pd.ExcelWriter(name_excel) as writer:
    dff.to_excel(writer, sheet_name='Sheet1')

