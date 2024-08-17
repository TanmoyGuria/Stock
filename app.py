import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from stocknews import StockNews
import requests

st.markdown(
        """
        <style>
        .title {
            font-size: 48px;
            color: #490648; /* You can change the color code to your preference */
            text-align: center;
            font-weight: bold;
        }
        </style>""",
        unsafe_allow_html=True
    )

st.markdown('<h1 class="title">Stock Dashboard</h1>', unsafe_allow_html=True)





url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

table = pd.read_html(url)
sp500_tickers = table[0]['Symbol'].tolist()
sidebar_bg = """
    <style>
    [data-testid="stSidebar"] {
        background-image: url("https://img.freepik.com/premium-vector/gradient-abstract-background_23-2149154566.jpg");
        background-size: cover;
        background-position: center;
    }
    </style>
"""
st.markdown(sidebar_bg, unsafe_allow_html=True)
label_style = """
    <style>
    label {
        color: white !important;
        font-weight: bold !important;
        font-size: 20px !important;
    }
    </style>"""
st.markdown(label_style, unsafe_allow_html=True)
ticker=st.sidebar.selectbox('TICKER',sp500_tickers,index=None,placeholder="STOCKS")
start_date=st.sidebar.date_input('START DATE')
end_date=st.sidebar.date_input('END DATE')
my_stocks=st.sidebar.multiselect("WATCHLIST", sp500_tickers, default=None, max_selections=10, placeholder="My Stocks")

if ticker:
    stock = yf.Ticker(ticker)
    company_name = stock.info['longName']

    st.header(company_name)
    data = yf.download(ticker, start=start_date, end=end_date)
    pricing_data, fundamental_data, news=st.tabs(["PRICING","FUNDAMENTALS","NEWS"])
    with pricing_data:

        if not data.empty:

            col1, col2 = st.columns([5, 5])


            with col1:
                fig = px.line(data, x=data.index, y='Adj Close')
                st.plotly_chart(fig,use_container_width=True)

            with col2:
                fig1 = go.Figure(data=[go.Candlestick(x=data.index,
                                                      open=data['Open'],
                                                      high=data['High'],
                                                      low=data['Low'],
                                                      close=data['Close'])])

                fig1.update_layout(xaxis_rangeslider_visible=False)
                st.plotly_chart(fig1,use_container_width=True)
            st.subheader("Price Movement")
            f_date=f"{start_date.year}-01-01"
            e_date=f"{end_date.year}-12-31"
            data1 = stock.history(start=f_date, end=e_date)
            data1=data1.iloc[:,:-2]
            col5, col6 = st.columns([7, 3])
            with col5:
                data1
            with col6:
                if my_stocks:
                    st.subheader("WATCHLIST")
                    c_price=[]
                    for i in my_stocks:
                        ticker1 = yf.Ticker(i)
                        current_price = ticker1.history(period='1d')['Close'][0]
                        c_price.append(current_price)
                    df_stock = pd.DataFrame({'Stock': my_stocks, 'Current Price': c_price})
                    table_style = """
                        <style>
                        table {
                            width: 100%;
                            border-collapse: collapse;
                        }
                        th {
                            background-color: #fc3f2d;
                            color: white;
                            font-size: 18px;
                            padding: 8px;
                        }
                        td {
                            background-color: #ffffff;
                            color: black;
                            font-size: 16px;
                            padding: 8px;
                            text-align: center;
                        }
                        tr:nth-child(even) {
                            background-color: #F5DEB3;
                        }
                        </style>"""
                    st.write(table_style + df_stock.to_html(index=False), unsafe_allow_html=True)


        else:
            st.write(f"No data available for {ticker} and date range.")

    with fundamental_data:
        st.subheader("BALANCE SHEET")
        stock.balance_sheet
        st.subheader("INCOME STATEMENT")
        stock.income_stmt
        st.subheader("CASHFLOW")
        stock.cashflow
    with news:
        st.header(f"TOP NEWS OF {company_name}")
        sn=StockNews(ticker,save_news=False)
        df_news=sn.read_rss()
        for i in range(10):
            st.subheader(f'News {i+1}')
            st.markdown(f"<p style='font-size: 13px;'>{df_news['published'][i]}</p>",
                        unsafe_allow_html=True)

            st.markdown(f"<h2 style='color: Black;font-size: 20px'>{df_news['title'][i]}</h2>", unsafe_allow_html=True)
            st.write(df_news['summary'][i])
            title_sentiment=df_news['sentiment_title'][i]
            news_sentiment=df_news['sentiment_summary'][i]
            col3, col4 = st.columns([5, 5])
            with col3:
                st.markdown(f"<p style='color: orange; font-size: 16px;'>Title Sentiment: {title_sentiment}</p>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<p style='color: orange; font-size: 16px;'>News Sentiment: {news_sentiment}</p>", unsafe_allow_html=True)

else:
    st.write("Please enter correct Stock")