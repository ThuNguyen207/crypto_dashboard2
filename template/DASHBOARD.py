# setup
# from matplotlib.pyplot import margins
import streamlit as st
import pandas as pd
import numpy as np
import cryptocompare as cc
from datetime import datetime
import plotly.graph_objects as go
from datetime import date
from PIL import Image
import plotly.express as px
from requests import Request, Session
from bs4 import BeautifulSoup
import requests
import json


#set variable
coinlist=np.array(['BTC','ETH','BUSD','USDC','SOL','USDT','XRP','BNB','MATIC','ADA'])
api_key="631999bf0b5310a37e876c6773310f46c097dddcb6fdeb252ca3c17e25f0bf81"
# api_key = "3ad6c9b5d03a59cc3c76d3dce0e851ab1884f79949ae13ecd2fc3a1155ebd96b"####
ccobj=cc.cryptocompare._set_api_key_parameter(api_key)

#url coinmarketcap:
cmc = requests.get('https://coinmarketcap.com')
soup = BeautifulSoup(cmc.content, 'html.parser')


#1h
def plot_1h(coin, margin_setup, C):
    ## C = chart type
    df1h=pd.DataFrame(cc.get_historical_price_minute(coin,'USD',limit=59, exchange='CCCAGG',toTs=datetime.now()))
    minute1h=[]
    for i in range(df1h.shape[0]):
        minute1h.append(datetime.fromtimestamp(df1h.iloc[i,0]))
    
    if C=='Candlestick chart':
        ##candelstick-price
        fig1hprice = go.Figure(data=[go.Candlestick(x=minute1h, open=df1h['open'], high=df1h['high'],low=df1h['low'], close=df1h['close'])])
        fig1hprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)
    elif C=='Line chart':
        ##linechart-price
        fig1hprice=go.Figure([go.Scatter(x=minute1h, y=df1h['close'])])
        fig1hprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)

    ##barchar-volumn
    fig1hb=px.bar(df1h, x=minute1h, y=df1h['volumeto'])
    fig1hb.update_layout(xaxis_rangeslider_visible=False,width=1000, height=300,hovermode='x unified', margin=margin_setup)
    return fig1hprice, fig1hb



#1day
def plot_1day(coin, margin_setup, C):
    ### C = chart type
    df1d=pd.DataFrame(cc.get_historical_price_minute(coin,'USD',limit=1440, exchange='CCCAGG',toTs=datetime.now()))
    time1d=[]
    for i in range(df1d.shape[0]):
        time1d.append((datetime.fromtimestamp(df1d.iloc[i,0])))
    minute1d=[]
    for i in range (df1d.shape[0]):
        minute1d.append(time1d[i].minute)
    df1d['time']=time1d
    df1d['minute']=minute1d
    df1d=df1d[df1d['minute']%10==0]
    if C=='Candlestick chart':
        ##candelstick-price
        fig1dprice = go.Figure(data=[go.Candlestick(x=df1d['time'], open=df1d['open'], high=df1d['high'],low=df1d['low'], close=df1d['close'])])
        fig1dprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)
    elif C=='Line chart':
        ##linechart-price
        fig1dprice=go.Figure([go.Scatter(x=df1d['time'], y=df1d['close'])])
        fig1dprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)
    ##barchar-volumn
    fig1db=px.bar(df1d, x=df1d['time'], y=df1d['volumeto'])
    fig1db.update_layout(xaxis_rangeslider_visible=False, width=1000, height=300,hovermode='x unified', margin=margin_setup)
    return fig1dprice, fig1db



#1week
def plot_1week(coin, margin_setup, C):
    ## C = chart type
    df1w=pd.DataFrame(cc.get_historical_price_hour(coin,'USD',limit=167, exchange='CCCAGG',toTs=datetime.now()))
    hour1w=[]
    for i in range(df1w.shape[0]):
        hour1w.append((datetime.fromtimestamp(df1w.iloc[i,0])))
    
    if C=='Candlestick chart':
        ##candelstick-price
        fig1wprice = go.Figure(data=[go.Candlestick(x=hour1w, open=df1w['open'], high=df1w['high'],low=df1w['low'], close=df1w['close'])])
        fig1wprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)
    elif C=='Line chart':
        ###linechart-price
        fig1wprice=go.Figure([go.Scatter(x=hour1w, y=df1w['close'])])
        fig1wprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)

    ##barchar-volumn
    fig1wb=px.bar(df1w, x=hour1w, y=df1w['volumeto'])
    fig1wb.update_layout(xaxis_rangeslider_visible=False, width=1000, height=300,hovermode='x unified', margin=margin_setup)
    return fig1wprice, fig1wb


#1month
def plot_1month(coin, margin_setup, C):
    ## C = chart type
    df1m=pd.DataFrame(cc.get_historical_price_hour(coin,'USD',limit=720, exchange='CCCAGG',toTs=datetime.now()))
    time1m=[]
    for i in range(df1m.shape[0]):
        time1m.append((datetime.fromtimestamp(df1m.iloc[i,0])))
    hour1m=[]
    for i in range (df1m.shape[0]):
        hour1m.append(time1m[i].hour)
    df1m['time']=time1m
    df1m['hour']=hour1m
    df1m=df1m[df1m['hour']%6==0]
    
    if C=='Candlestick chart':
        ##candelstick-price
        fig1mprice = go.Figure(data=[go.Candlestick(x=df1m['time'], open=df1m['open'], high=df1m['high'],low=df1m['low'], close=df1m['close'])])
        fig1mprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)
    elif C=='Line chart':
        ##linechart-price
        fig1mprice=go.Figure([go.Scatter(x=df1m['time'], y=df1m['close'])])
        fig1mprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)

    ##barchar-volumn
    fig1mb=px.bar(df1m, x=df1m['time'], y=df1m['volumeto'])
    fig1mb.update_layout(xaxis_rangeslider_visible=False, width=1000, height=300,hovermode='x unified', margin=margin_setup)

    return fig1mprice, fig1mb


#6month
def plot_6months(coin, margin_setup, C):
    ## C = chart type
    df6m=pd.DataFrame(cc.get_historical_price_day(coin,'USD',limit=181,exchange='CCCAGG',toTs=datetime.now()))
    day6m = []
    for i in range(df6m.shape[0]):
        day6m.append(date.fromtimestamp(df6m.iloc[i, 0]))
    
    if C=='Candlestick chart':
        ##candelstick-price
        fig6mprice = go.Figure(data=[go.Candlestick(x=day6m, open=df6m['open'], high=df6m['high'],low=df6m['low'], close=df6m['close'])])
        fig6mprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)
    elif C=='Line chart':
        ###linechart-price
        fig6mprice=go.Figure([go.Scatter(x=day6m, y=df6m['close'])])
        fig6mprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500, hovermode='x unified', margin=margin_setup)
    ##barchar-volumn
    fig6mb=px.bar(df6m, x=day6m, y=df6m['volumeto'])
    fig6mb.update_layout(xaxis_rangeslider_visible=False, width=1000, height=300,hovermode='x unified', margin=margin_setup)

    return fig6mprice, fig6mb


#1year
def plot_1year(coin, margin_setup, C):
    ## C = chart type
    df1y=pd.DataFrame(cc.get_historical_price_day(coin,'USD',limit=364,exchange='CCCAGG',toTs=datetime.now()))
    day1y=[]
    for i in range(df1y.shape[0]):
        day1y.append((date.fromtimestamp(df1y.iloc[i,0])))
    
    if C=='Candlestick chart':
        #candelstick-price:
        fig1yprice=go.Figure(data=[go.Candlestick(x=day1y, open=df1y['open'], high=df1y['high'],low=df1y['low'], close=df1y['close'])])
        fig1yprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)
    elif C=='Line chart':
        #linechart-price:
        fig1yprice=go.Figure([go.Scatter(x=day1y, y=df1y['close'])])
        fig1yprice.update_layout(xaxis_rangeslider_visible=False, width=1000, height=500,hovermode='x unified', margin=margin_setup)
    ##barchar-volumn
    fig1yb=px.bar(df1y, x=day1y, y=df1y['volumeto'])
    fig1yb.update_layout(xaxis_rangeslider_visible=False, width=1000, height=300,hovermode='x unified', margin=margin_setup)

    return fig1yprice, fig1yb


def dashboard(coin: str):
    #### download data from coinmarketcap
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coin_data = json.loads(data.contents[0])

    # market_info = coin_data['props']['pageProps']['globalMetrics']
    listings = json.loads(coin_data['props']['initialState'])['cryptocurrency']['listingLatest']['data']
    market_cap_name = 'quote.USD.marketCap'
    for i in listings[1:]:
        coin_symbol = i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'symbol'][0]]
        if coin_symbol==coin:
            coin_price = '$' + f"{round(i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'quote.USD.price'][0]],3)}"
            coin_priceCh24h = f"{round(i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'quote.USD.percentChange24h'][0]],3)}"+'%'
            
            coin_vol24h = '$' + f"{round(i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'quote.USD.volume24h'][0]],1)}"        
            coin_cap = i[[k for k, j in enumerate(listings[0]['keysArr']) if j == market_cap_name][0]]
            coin_cap_pct = round(i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'quote.USD.dominance'][0]],3)
            break
    coin_cap_pct=str(f"{coin_cap_pct}" + "%")
    coin_cap='$'+str(f"{round(coin_cap/1e9,3):,}" + 'B')

    # Introduction:
    icon, sym_alg, price, vol, cap, cap_pct = st.columns([1,1,1,1,1,1])
    img_path = './icons/'+ coin + '.jpg'
    icon.image(Image.open(img_path))
    
    sym_alg.text('Symbol:' + coin)
    
    coin_list=cc.get_coin_list()
    sym_alg.text('Algo:' + coin_list[coin]['Algorithm'])
    

    price.metric(label='Price', value=coin_price, delta=coin_priceCh24h)
    vol.metric(label='Volume 24h', value=coin_vol24h)

    cap.metric(label='Coin market cap', value=coin_cap)
    cap_pct.metric(label='Market cap proportion', value=coin_cap_pct)

    Description = st.checkbox('Description')
    if Description:
        st.write(coin_list[coin]['Description'])

    
    #Summary column a1 : information
    st.markdown(
      """
      <h1>Coin price statistics and pairs</h1>
      """
    , unsafe_allow_html=True)

    infor, pair = st.columns(2)
    #----infor part
    pricecoin='$'+str(f"{cc.get_price(coin,currency='USD')[coin]['USD']:,}")
    change24h=str(f"{round(cc.get_avg(coin, currency='USD')['CHANGEPCT24HOUR'], 2):,}") + ' %'
    highprice='$'+str(f"{cc.get_avg(coin, currency='USD')['HIGH24HOUR']:,}")
    lowprice='$'+ str(f"{cc.get_avg(coin, currency='USD')['LOW24HOUR']:,}")
    volume24h ='$'+ str(f"{round(cc.get_avg(coin, currency='USD')['TOPTIERVOLUME24HOURTO']/1e6,2):,}")+ ' M'
    
    infordata=pd.DataFrame({'Information':['Price','Change 24h','Highest price 24h','Lowest price 24h','Volume 24h','Coin market cap','Total market cap proportion'],
    'Value':[pricecoin,change24h,highprice,lowprice,volume24h,coin_cap,coin_cap_pct]})
    infor.subheader(coin + ' Price Statistics')
    infor.table(infordata)
    
    #----pair part:
    currencyunit=np.setdiff1d(coinlist, coin)
    Pairs=[]
    Prices=[]
    for i in range(7):
        Pairs.append(coin+'/'+currencyunit[i])
        Prices.append(f"{round(cc.get_price(coin,currency=currencyunit[i])[coin][currencyunit[i]],2):,}")
    pairprice=pd.DataFrame({'Pairs':Pairs,'Price':Prices})
    pair.subheader(coin + ' Price Pairs')
    pair.table(pairprice)

    # Chart
    title="Historical Data of " + coin
    st.title(title)
    
    Time,Chart=st.columns(2)
    T = Time.selectbox('Select time',('1 Hour','1 Day','1 Week','1 Month','6 Months','1 Year'))
    C = Chart.selectbox('Select chart type',('Candlestick chart','Line chart'))


    margin_setup = dict(l=20, r=20, t=40, b=20)
    if T == '1 Hour':
        fig1hprice, fig1hb = plot_1h(coin, margin_setup, C)
        st.markdown(
            """
            <h2>Historical Price</h2>
            """
        , unsafe_allow_html=True)

        st.plotly_chart(fig1hprice, use_container_width=True)

        st.markdown(
            """
            <h2>Volume</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig1hb,use_container_width=True)

    elif T=='1 Day':
        fig1dprice, fig1db = plot_1day(coin, margin_setup, C)
        st.markdown(
            """
            <h2>Historical Price</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig1dprice, use_container_width=True)

        st.markdown(
            """
            <h2>Volume</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig1db,use_container_width=True)

    elif T=='1 Week':
        fig1wprice, fig1wb = plot_1week(coin, margin_setup, C)
        st.markdown(
            """
            <h2>Historical Price</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig1wprice, use_container_width=True)

        st.markdown(
            """
            <h2>Volume</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig1wb, use_container_width=True)

    elif T=='1 Month':
        fig1mprice, fig1mb = plot_1month(coin, margin_setup, C)
        st.markdown(
            """
            <h2>Historical Price</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig1mprice, use_container_width=True)

        st.markdown(
            """
            <h2>Volume</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig1mb, use_container_width=True)

    elif T=='6 Months':
        fig6mprice, fig6mb = plot_6months(coin, margin_setup, C)

        st.markdown(
            """
            <h2>Historical Price</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig6mprice, use_container_width=True)

        st.markdown(
            """
            <h2>Volume</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig6mb, use_container_width=True)

    else:
        fig1yprice, fig1yb = plot_1year(coin, margin_setup, C)
        st.markdown(
            """
            <h2>Historical Price</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig1yprice, use_container_width=True)

        st.markdown(
            """
            <h2>Volume</h2>
            """
        , unsafe_allow_html=True)
        st.plotly_chart(fig1yb, use_container_width=True)
