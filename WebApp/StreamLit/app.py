import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow

st.title("WIND POWER PREDICTION")

data = pd.DataFrame(
    np.random.randn(100, 1),
    columns=['a'])

st.area_chart(data)

st.date_input("Enter Date")

st.number_input("Enter Wind Speed")

st.number_input("Enter Wind Direction")

st.success("Predicted Power Output for next 5 Days is 16MW ")