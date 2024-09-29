import streamlit as st
import pandas as pd
import numpy as np

# Streamlit app layout
st.title("Simple Streamlit App")

st.write("This is a simple Streamlit app that displays a line chart of random data.")

# Generate random data
data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=['A', 'B', 'C']
)

# Display the data as a line chart
st.line_chart(data)