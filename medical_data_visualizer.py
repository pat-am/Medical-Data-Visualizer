import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")
df.dropna(how = 'any')

# Add 'overweight' column
df['overweight'] = ''
df['overweight'] = df['weight'] / (df['height']/100)**2
df['overweight'] = np.where(df['overweight'] > 25, 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df['cholesterol'] = np.where(df['cholesterol'] > 1, 1, 0)

df['gluc'] = np.where(df['gluc'] > 1, 1, 0)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df_cat = pd.melt(df, id_vars = ['cardio'], value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).agg(total=pd.NamedAgg(column='value', aggfunc='count'))

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x = 'variable', y = 'total', col = 'cardio', hue = 'value', kind = 'bar',  data = df_cat)


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    fig = fig.fig
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & #keep only diastolic is lower the systolic BP
             (df['height'] >= df['height'].quantile(0.025)) & #keep only height is higher then 2.5th percentile
             (df['height'] <= df['height'].quantile(0.975)) & #keep only height is lower than 97.5th perecentile
             (df['weight'] >= df['weight'].quantile(0.025)) & #keep only weight is higher than 2.5th percentile
             (df['weight'] <= df['weight'].quantile(0.975))] #keep only weight is lower than 97.5th perecentile

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)


    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(7, 5))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, square=True, annot=True, fmt='.1f').get_figure()


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
