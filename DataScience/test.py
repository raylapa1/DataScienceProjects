import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('This is to test streamlit')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Nothing).
""")

# Web scraping of NBA player stats
@st.cache
def load_data():
    url = "https://crypto.com/price/"
    html = pd.read_html(url, header = 0)
    df = html[0]
    #raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    #raw = raw.fillna(0)
    #playerstats = raw.drop(['Rk'], axis=1)
    return html
playerstats = load_data()