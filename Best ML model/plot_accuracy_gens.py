# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:53:01 2024

@author: MPrina
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel('output_random_more_models_new.xlsx')

# List of models to plot
models_to_plot = [
    'Linear Regression',
    'Decision Tree',
    'Random Forest',
    # 'XGBoost',
    'Neural Network, Hidden Layer=50',
    'Neural Network, Hidden Layer=100',
    'Neural Network, Hidden Layer=200',
    'Neural Network, Hidden Layer=500'
]

# Create a figure and two subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

# Plot each model in the first subplot
for model in models_to_plot:
    axs[0].plot(df['Ngen'], df[model+' Avg'], label=model)
    axs[0].fill_between(df['Ngen'], df[model+' Avg'] - df[model+' CI'], df[model+' Avg'] + df[model+' CI'], alpha=0.3)

# Zoom into the 90-100% accuracy area in the second subplot
for model in models_to_plot:
    axs[1].plot(df['Ngen'], df[model+' Avg'], label=model)
    axs[1].fill_between(df['Ngen'], df[model+' Avg'] - df[model+' CI'], df[model+' Avg'] + df[model+' CI'], alpha=0.3)

# Add labels and legend to the first subplot
axs[0].set_ylabel('Accuracy [%]')
axs[0].set_title('Accuracy progression of various machine learning models')
# axs[0].grid(True)
axs[0].grid(True, linestyle=':', linewidth=0.5)

# Add labels to the second subplot
axs[1].set_xlabel('Generation')
axs[1].set_ylabel('Accuracy [%]')
axs[1].set_title('Zoomed-in (95-100%)')
axs[1].grid(True, linestyle=':', linewidth=0.5)
axs[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=len(models_to_plot)//2)

# Set y-axis limits to zoom into 90-100% accuracy area in the second subplot
axs[1].set_ylim(95, 100)

# Remove frame of the subplots
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    
# Adjust layout
plt.tight_layout()

# Show plot
plt.show()
plt.savefig('accuracy_vs_generation_plot.png', bbox_inches='tight', dpi=300)









