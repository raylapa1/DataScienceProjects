import pandas as pd

url = "https://coinmarketcap.com"

html = pd.read_html(url, header=0)

df = html[0]

print(df)