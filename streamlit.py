
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 20:54:11 2021

@author: Nishant Nayar

Created as part of the Hackathon 2023
Additional authors

Johnson Bam

"""

# =============================================================================
# # Load basic libraries
# =============================================================================

import streamlit as st
import pandas as pd
#import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
           





# =============================================================================
# Setting global options
# =============================================================================

st.set_page_config(layout="wide", page_title='Hackathon 2023: Group 2',
                   initial_sidebar_state='collapsed')
st.set_option('deprecation.showPyplotGlobalUse', False)


# =============================================================================
# # Color pallete
# =============================================================================

enmax_palette = ["#FFD966", "#434343" , "#fff2cc", '#fafafa', '#FF0000']
color_codes_wanted = ['cream', 'black', 'lightcream', 'lightblue', 'red']
c = lambda x: enmax_palette[color_codes_wanted.index(x)]

# this is where we will create a CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


local_css(".\config\CustomStyle.css")

# =============================================================================
# Load Data
# =============================================================================

@st.cache_data
def load_data_meta():
    df = pd.read_pickle('./data/meta_plot_data.pkl')
    return df

df=load_data_meta()

def load_data_nvda():
    df = pd.read_pickle('./data/nvda_plot_data.pkl')
    return df

df2=load_data_nvda()

# =============================================================================
# Create App title:
# =============================================================================
st.title("Introduction")
st.write(
    """
    **Here we will dispaly prices - 2023 with priyank**
    """)   


# =============================================================================
# create sidebar
# =============================================================================

st.sidebar.subheader("Hackathon App")
st.sidebar.write("Display stock prices")


# =============================================================================
# Create App layout:
# ============================================================================= 

with st.container():
   st.write("This is inside the container1")

   # You can call any Streamlit command, including custom components:


st.write("This is outside the container")
    

with st.container():

   #st.write("This is inside the container2")

   # You can call any Streamlit command, including custom components:
   row0_1,  row0_2, = st.columns((5, 5))
   with row0_1:
                      
       fig=go.Figure()
       fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.05,
                    row_heights=[100,50])
       
       # fig = go.Figure(data=[go.Candlestick(x=df.index,
       #              open=df['open'], high=df['high'],
       #              low=df['low'], close=df['close'])
       #                   ])
       fig.add_trace(go.Candlestick(x=df.index,  
                                    open=df['open'],
                                    high=df['high'],
                                    low=df['low'],
                                    close=df['close'],
                                    name = 'OHLC'))
       # add moving average traces
       fig.add_trace(go.Scatter(x=df.index,
                                 y=df['MA5'],
                                 opacity=0.7,
                                 line=dict(color='blue', width=2),
                                 name='MA 5'))
       fig.add_trace(go.Scatter(x=df.index,
                                 y=df['MA20'],
                                 opacity=0.7,
                                 line=dict(color='orange', width=2),
                                 name='MA 20'))
       # Plot MACD trace on 2nd row

       fig.add_trace(go.Scatter(x=df.index,
                         y=df['macd'],
                         line=dict(color='black', width=2),
                       name='MACD' ), row=2, col=1)

       fig.add_trace(go.Scatter(x=df.index,
                         y=df['macd_signal'],
                         line=dict(color='skyblue', width=2),
                       name='MACD Signal' ), row=2, col=1)

       colors = ['green' if val >= 0
          else 'red' for val in df['macd_hist']]

       fig.add_trace(go.Bar(x=df.index,
                     y=df['macd_hist'],
                     marker_color=colors,
                     name='Histogram'
                    ), row=2, col=1)
       # hide weekends and xaxes
       fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])], showgrid=False)
       fig.update_xaxes(visible=True, showticklabels=False)
       
       fig.update_yaxes(title_text="OHLC" ,  showgrid=True, row=1, col=1, 
                 title_font_color="#444", title_font_size = 20)
       fig.update_yaxes(title_text="MACD/Signal/Hist", showgrid=True, row=2, col=1,  
                 title_font_color="#444", title_font_size = 15 )

       
       fig.update_layout(xaxis_rangeslider_visible=False)
       
       fig.update_layout(height=700, 
                title="Meta<br><sup>H2 2023</sup>",
                 title_font_color="#f00", title_font_size = 24)
       
       st.plotly_chart(fig, theme="streamlit", use_container_width=True)

   
with row0_2:
                   
    fig=go.Figure()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                 vertical_spacing=0.05,
                 row_heights=[100,50])
    
    # fig = go.Figure(data=[go.Candlestick(x=df.index,
    #              open=df['open'], high=df['high'],
    #              low=df['low'], close=df['close'])
    #                   ])
    fig.add_trace(go.Candlestick(x=df2.index,  
                                 open=df2['open'],
                                 high=df2['high'],
                                 low=df2['low'],
                                 close=df2['close'],
                                 name = 'OHLC'))
    # add moving average traces
    fig.add_trace(go.Scatter(x=df2.index,
                              y=df2['MA5'],
                              opacity=0.7,
                              line=dict(color='blue', width=2),
                              name='MA 5'))
    fig.add_trace(go.Scatter(x=df2.index,
                              y=df2['MA20'],
                              opacity=0.7,
                              line=dict(color='orange', width=2),
                              name='MA 20'))
    # Plot MACD trace on 2nd row

    fig.add_trace(go.Scatter(x=df2.index,
                      y=df2['macd'],
                      line=dict(color='black', width=2),
                    name='MACD' ), row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index,
                      y=df2['macd_signal'],
                      line=dict(color='skyblue', width=2),
                    name='MACD Signal' ), row=2, col=1)

    colors = ['green' if val >= 0
       else 'red' for val in df['macd_hist']]

    fig.add_trace(go.Bar(x=df.index,
                  y=df2['macd_hist'],
                  marker_color=colors,
                  name='Histogram'
                 ), row=2, col=1)
    # hide weekends and xaxes
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])], showgrid=False)
    fig.update_xaxes(visible=True, showticklabels=False)
    
    fig.update_yaxes(title_text="OHLC" ,  showgrid=True, row=1, col=1, 
              title_font_color="#444", title_font_size = 20)
    fig.update_yaxes(title_text="MACD/Signal/Hist", showgrid=True, row=2, col=1,  
              title_font_color="#444", title_font_size = 15 )

    
    fig.update_layout(xaxis_rangeslider_visible=False)
    
    fig.update_layout(height=700, 
             title="NVDA<br><sup>H2 2023</sup>",
              title_font_color="#f00", title_font_size = 24)
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)       

