from backend import get_data
import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.io import show
from bokeh.resources import CDN
from bokeh.embed import file_html

# Streamlit app layout
st.title("OHLC-10s Open Plot")

df = get_data()

# Ensure timestamp is in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp_ms_str'])
df.sort_values('timestamp', inplace=True)

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# Create a Bokeh plot
source = ColumnDataSource(df)
p = figure(x_axis_type="datetime", title="OHLC-10s Open Plot", height=350, width=800)
p.line(x='timestamp', y='open', source=source, line_width=2)

# Add hover tool
hover = HoverTool()
hover.tooltips = [("Time", "@timestamp{%F %T}"), ("Open", "@open")]
hover.formatters = {"@timestamp": "datetime"}
p.add_tools(hover)

# Display the plot in Streamlit
st.bokeh_chart(p)




