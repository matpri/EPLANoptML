# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 15:19:44 2023

@author: MPrina
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np
import seaborn as sns


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler


# ex_hist10 = pd.ExcelFile("pareto2050.xlsx")
# df_hist = ex_hist10.parse("history")
# df_P = ex_hist10.parse("Pareto")

df_hist = pd.read_csv('history_csv.csv')#, sheet_name='history_csv'
# df_hist = pd.read_csv('history_csv_random_sim.csv')#, sheet_name='history_csv_random_sim')

df_hist = df_hist.loc[df_hist['Total annual costs [Meuro]'] < 500000]

# del df_hist['Unnamed: 0']

del df_hist['Unnamed: 12']

print(len(df_hist))

Npop=200
Ngen_list=[i for i in range(1, 13)]

models_out = {
    # 'Linear Regression': [],
    # 'Decision Tree': [],
    # 'Random Forest': [],
    # 'XGBoost': [],
    # 'Neural Network': [],
    # 'Neural Network hidden_layer_sizes=(100, 100), max_iter=500': [],
    # 'Neural Network hidden_layer_sizes=(200, 200), max_iter=500': [],
    'Neural Network hidden_layer_sizes=(500, 500), max_iter=500': [],
    
    # 'Neural Network hidden_layer_sizes=(100, 100), max_iter=1000': [],
    # 'Neural Network hidden_layer_sizes=(200, 200), max_iter=1000': [],
    # 'Neural Network hidden_layer_sizes=(500, 500), max_iter=1000': [],

    # 'Neural Network hidden_layer_sizes=(100, 100), max_iter=1000': [],
    # 'Neural Network hidden_layer_sizes=(200, 200), max_iter=2000': [],
    # 'Neural Network hidden_layer_sizes=(500, 500), max_iter=5000': [],
}

# Create a scatter plot of the errors
fig, ax = plt.subplots(nrows=3, ncols=4, figsize=(14, 9))

ROW=0
COL=0

for a in range(len(Ngen_list)):

    Ngen= Ngen_list[a]
    print('-------------------', Ngen)
    
    # X_train=df_hist.iloc[0:Ngen*Npop, :12]
    # X_test=df_hist.iloc[Ngen*Npop:, :12]

    X_train=df_hist.iloc[0:Ngen*Npop, :10]
    X_test=df_hist.iloc[Ngen*Npop:, :10]
    
    Y_train=df_hist.iloc[0:Ngen*Npop, -2:]
    Y_test=df_hist.iloc[Ngen*Npop:, -2:]
    
    X_test1=X_test
    # print('X_test', X_test)
    
    # Normalize the data
    scaler_X = StandardScaler()
    X_train = scaler_X.fit_transform(X_train)
    X_test = scaler_X.transform(X_test)
    
    scaler_Y = StandardScaler()
    Y_train = scaler_Y.fit_transform(Y_train)
    Y_test = scaler_Y.transform(Y_test)
    
    # Define different models
    models = {
        # 'Linear Regression': LinearRegression(),
        # 'Decision Tree': DecisionTreeRegressor(),
        # 'Random Forest': RandomForestRegressor(),
        # 'XGBoost': XGBRegressor(),
        # 'Neural Network': MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=500, random_state=42),
        # 'Neural Network hidden_layer_sizes=(100, 100), max_iter=500': MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=500, random_state=42),
        # 'Neural Network hidden_layer_sizes=(200, 200), max_iter=500': MLPRegressor(hidden_layer_sizes=(200, 200), max_iter=500, random_state=42),
        'Neural Network hidden_layer_sizes=(500, 500), max_iter=500': MLPRegressor(hidden_layer_sizes=(500, 500), max_iter=500, random_state=42),
        # 'Neural Network hidden_layer_sizes=(100, 100), max_iter=1000': MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=1000, random_state=42),
        # 'Neural Network hidden_layer_sizes=(200, 200), max_iter=1000': MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=1000, random_state=42),
        # 'Neural Network hidden_layer_sizes=(500, 500), max_iter=1000': MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=1000, random_state=42),
        # 'Neural Network hidden_layer_sizes=(100, 100), max_iter=1000': MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=1000, random_state=42),
        # 'Neural Network hidden_layer_sizes=(200, 200), max_iter=2000': MLPRegressor(hidden_layer_sizes=(200, 200), max_iter=2000, random_state=42),
        # 'Neural Network hidden_layer_sizes=(500, 500), max_iter=5000': MLPRegressor(hidden_layer_sizes=(500, 500), max_iter=5000, random_state=42),
    }
    
    # Train and evaluate models
    best_model = None
    highest_r2 = float("-inf")
    
    for name, model in models.items():
        # print(name, model)
        # Since there are two outputs, we need to fit the model for each output and combine the results
        predictions = pd.DataFrame()
        for col in range(Y_train.shape[1]):
            model.fit(X_train, Y_train[:, col])
            predictions[col] = model.predict(X_test)
        
        # Calculate the R² score as an accuracy indicator (constrained between 0 and 100%)
        r2 = max(0, min(r2_score(Y_test, predictions), 1)) * 100
        
        models_out[name].append(r2)
        
        # Display the results
        # print(f'{name} R² Score: {r2}%')
        
        # Check if this model performs better
        if r2 > highest_r2:
            best_model = name
            highest_r2 = r2




        # Convert the predictions and actual values back to the original scale
        Y_test_orig = scaler_Y.inverse_transform(Y_test)
        predictions_orig = scaler_Y.inverse_transform(predictions)
        
        # Calculate the errors as a percentage of the real values
        errors = (Y_test_orig - predictions_orig) / Y_test_orig * 100
        
        # Separate errors for each output
        errors_x = errors[:, 0]
        errors_y = errors[:, 1]
        
        # Calculate percentiles
        perc_25_x = np.percentile(errors_x, 25)
        perc_75_x = np.percentile(errors_x, 75)
        perc_25_y = np.percentile(errors_y, 25)
        perc_75_y = np.percentile(errors_y, 75)
        
        # Calculate the average error
        avg_error_x = np.mean(errors_x)
        avg_error_y = np.mean(errors_y)
        
        # Prepare data for seaborn
        data = pd.DataFrame({
            'Error in first output (%)': errors_x,
            'Error in second output (%)': errors_y
        })
        

        
        # plt.figure(figsize=(10, 7))
        kde = sns.kdeplot(data=data, x='Error in first output (%)', y='Error in second output (%)', cmap="Reds", fill=True,ax=ax[ROW][COL])

        # ax[ROW][COL].set_title('Prediction Errors')
        ax[ROW][COL].set_xlim([-2, 2])
        ax[ROW][COL].set_ylim([-2, 2])
        
        name_title='Generation '+str(Ngen)
        ax[ROW][COL].set_title(name_title)
        
        ax[ROW][COL].spines['top'].set_visible(False)
        ax[ROW][COL].spines['right'].set_visible(False)
        # ax[ROW][COL].spines['bottom'].set_visible(False)
        # ax[ROW][COL].spines['left'].set_visible(False)        
        # plt.grid(True)
        plt.show()
        
        if COL>=1:
            ax[ROW][COL].set_ylabel('')
        else:
            ax[ROW][COL].set_ylabel('Error in annual Costs [%]')
        if ROW<2:
            ax[ROW][COL].set_xlabel('')
        else:
            ax[ROW][COL].set_xlabel('Error in CO2 emissions [%]')

        # ax[ROW][COL].scatter([0], [0], color='black', marker='o')
        # ax[ROW][COL].text(0+0.15, 0+0.15, 'Ideal output')

        # Plot two orthogonal dashed lines intersecting at (0,0)
        ax[ROW][COL].axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax[ROW][COL].axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        
        COL=COL+1
        if COL==4:
            COL=0
            ROW=ROW+1
        print('row, col ',  ROW, COL)


        # # Create a dummy plot
        # dummy_fig, dummy_ax = plt.subplots(figsize=(8, 1))
        # dummy_plot = dummy_ax.imshow(np.array([[0, 1]]), cmap="Reds")
        # dummy_ax.set_visible(False)
        # # Add colorbar legend outside the loop
        # cbar = fig.colorbar(dummy_plot, ax=ax.ravel().tolist(), location='right', shrink=0.5)
        # cbar.ax.set_title('Density', fontsize=12)
        # cbar.ax.tick_params(labelsize=10)  # Set tick label size
        # # cbar.set_ticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])  # Set tick positions
        # # cbar.set_ticklabels(['Low', '', '', '', '', 'High'])  # Set tick labels
        # cbar.ax.yaxis.set_label_position('left')  # Adjust label position

# Import ScalarMappable
from matplotlib.cm import ScalarMappable
# Create a ScalarMappable object
cbar_map = ScalarMappable(cmap="Reds")

# Normalize the colorbar
cbar_map.set_array(np.linspace(0, 1, 5))  # Adjust the number of steps as needed
cbar_ax = fig.add_axes([0.85, 0.25, 0.02, 0.5])
# Add colorbar legend
cbar = fig.colorbar(cbar_map, cax=cbar_ax, location='right', shrink=0.5)
cbar.ax.set_title('Density', fontsize=12)
cbar.ax.tick_params(labelsize=11)  # Set tick label size



# fig.colorbar(im, cax=cbar_ax)

plt.subplots_adjust(hspace=0.35, wspace=0.2)
# Adjust layout to make space for the colorbar on the right
plt.subplots_adjust(right=0.8)  # Adjust the value as needed


pylab.savefig('Errors.png', bbox_inches="tight", dpi=300)


dff=pd.DataFrame(models_out)
dff['Ngen']=Ngen_list

# name_excel='output.xlsx'
name_excel='output_random_more_models2.xlsx'

with pd.ExcelWriter(name_excel) as writer:
    dff.to_excel(writer, sheet_name='Sheet1')
