import pandas as pd
import plotly
df = pd.read_csv("SP500.csv")

print(df)

print(df.tail())

print(df[2:5])

print('\n\nLast element of the dataframe')
print(df[-1:])

print('\n\nPrint the year the oldest company was founded')
print(df['Founded'].min())