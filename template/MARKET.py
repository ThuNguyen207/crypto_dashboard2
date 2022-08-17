## import library
import streamlit as st
# from PIL import Image
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import cryptocompare as cc
#### USe for CoinmarketCap:
from bs4 import BeautifulSoup
import requests
import json
import base64
import os
# import matplotlib.pyplot as plt
# from requests import Request, Session
# import time
# import plotly.express as px
# from datetime import datetime

# from io import BytesIO
# response = requests.get(listcoin[coin]['ImageUrl'])
# img = Image.open(BytesIO(response.content))



# API CryptoCompare infor
coinlist=np.array(['BTC','ETH','BUSD','USDC','SOL','USDT','XRP','BNB','MATIC','ADA'])
# api_key="631999bf0b5310a37e876c6773310f46c097dddcb6fdeb252ca3c17e25f0bf81"
api_key = "3ad6c9b5d03a59cc3c76d3dce0e851ab1884f79949ae13ecd2fc3a1155ebd96b"

ccobj=cc.cryptocompare._set_api_key_parameter(api_key)

#data coinmarketcap
newlist='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/new'


### For downloading data from CoinMarketCap
cmc = requests.get('https://coinmarketcap.com')
soup = BeautifulSoup(cmc.content, 'html.parser')

cmc_exch = requests.get('https://coinmarketcap.com/rankings/exchanges/')
soup_exch = BeautifulSoup(cmc_exch.content, 'html.parser')

cmc_gain_lose = requests.get('https://coinmarketcap.com/gainers-losers/')
soup_gain_lose = BeautifulSoup(cmc_gain_lose.content, 'html.parser')

def render_diff(diff, is_pct):
  if diff > 0:
    if is_pct:
      return f'''<td class='text-success'><i class="fa-solid fa-caret-up mr-1"></i>{abs(diff)}%</td>'''
    else:
      return f'''<td class='text-success'><i class="fa-solid fa-caret-up mr-1"></i>{abs(diff)}</td>'''
  if diff < 0:
    if is_pct:
      return f'''<td class='text-danger'><i class="fa-solid fa-caret-down mr-1"></i>{abs(diff)}%</td>'''
    else:
      return f'''<td class='text-danger'><i class="fa-solid fa-caret-down mr-1"></i>{abs(diff)}</td>'''
  return f"<td>{diff}</td>"


def market():
  margin_setup = dict(l=20, r=20, t=40, b=20)
  icon_folder = os.path.join(os.path.dirname(__file__), "../coin-icons/")

  # title----------------------#
  # st.title('Crypto Analysis Dashboard')
  st.markdown(
    """
      <div id="Logo">
        Crypto Analysis Dashboard
      </div>
    """
    , unsafe_allow_html=True)
  

  # crypto market summary------#
  st.markdown(
    """
      <h1>Market Summary</h1>
    """
    , unsafe_allow_html=True)
  
  ### download data from CoinMarketCap
  data = soup.find('script', id='__NEXT_DATA__', type='application/json')
  coin_data = json.loads(data.contents[0])
  market_info = coin_data['props']['pageProps']['globalMetrics']

  crypto, marketNo, exchange, marketcap, volumne, dominance = st.columns([1,1,1,1.5,1.5,1.5])
  crypto.metric(label='Cryptos', value= str(f"{(market_info['numCryptocurrencies']):,}"))
  marketNo.metric(label='Markets', value= str(f"{(market_info['numMarkets']):,}"))
  exchange.metric(label='Active exchanges', value= str(f"{(market_info['activeExchanges']):,}"))
  
  marketcap_value = '$'+str(f"{round(market_info['marketCap']/1e9,3):,}" + 'B')
  marketcap_delta = f"{round(market_info['marketCapChange'],3)}"+'%'
  totalVolme_value = '$'+str(f"{round(market_info['totalVol']/1e6,3):,}" + 'M')

  marketcap.metric(label='Market cap', value=marketcap_value, delta=marketcap_delta)
  volumne.metric(label='Volume 24h', value=totalVolme_value)

  dominance_value = 'BTC: ' + f"{round(market_info['btcDominance'],1)}"+"%"
  dominance_value+= ', ' + 'ETH: '+ f"{round(market_info['ethDominance'],1)}"+"%"
  dominance.metric(label='Dominance', value=dominance_value)


  # coin list------------------#
  st.markdown(
      """
      <h1>Coin List</h1>
      """
  , unsafe_allow_html=True)
  price=[]
  change24h=[]
  change24hpct=[]
  Directvol=[]
  high=[]
  low=[]

  count = 0
  for coin in coinlist:
    price.append('$'+str(f"{cc.get_price(coin,currency='USD')[coin]['USD']:,}"))
    Directvol.append('$'+ str(f"{round(cc.get_avg(coin, currency='USD')['TOPTIERVOLUME24HOURTO']/1e6,2):,}")+ ' M')
    high.append('$'+str(f"{cc.get_avg(coin, currency='USD')['HIGH24HOUR']:,}"))
    low.append('$'+ str(f"{cc.get_avg(coin, currency='USD')['LOW24HOUR']:,}"))
    change24h.append(round(cc.get_avg(coin, currency='USD')['CHANGE24HOUR'], 4))
    change24hpct.append(round(cc.get_avg(coin, currency='USD')['CHANGEPCT24HOUR'], 2))
    
    count+=1

  table_html = """<table class="table table-striped table-hover table-borderless text-right">
      <thead>
          <tr>
              <th scope="col">#</th>
              <th class="text-left pl-5" scope="col">Coin</th>
              <th scope="col">Price</th>
              <th scope="col">Direct Vol</th>
              <th scope="col">High price 24h</th>
              <th scope="col">Low price 24h</th>
              <th scope="col">Change 24h</th>
              <th scope="col">% Change 24h</th>
          </tr>
      </thead>
      <tbody>
  """

  for idx, coin in enumerate(coinlist):
      icon = open(icon_folder + coin + ".png", "rb")
      icon_data = base64.b64encode(icon.read()).decode("utf-8")
      icon.close()

      table_html += f"""<tr>
              <th scope="row">{idx + 1}</th>
              <td class="text-left pl-5">
                  <a href='/?coin={coin}' target='_self'>
                    <img src='data:image/png;base64,{icon_data}' class='coin-icon'>
                    <label>{coin}</label>
                  </a>
              </td>
              <td>{price[idx]}</td>
              <td>{Directvol[idx]}</td>
              <td>{high[idx]}</td>
              <td>{low[idx]}</td>
              {render_diff(change24h[idx], False)}
              {render_diff(change24hpct[idx], True)}
          </tr>
      """
  table_html += """</tbody>
  </table>"""

  st.markdown(table_html, unsafe_allow_html=True)

  # trending
  st.markdown(
      """
      <h1>Spotlights</h1>
      """
  , unsafe_allow_html=True)

  ##### 3 newly added coins
  new_coin_syms = []
  new_coin_prices = []
  new_coin_Change24h = []
  for i in range(3):
    new_coini = json.loads(coin_data['props']['initialState'])['cryptocurrency']['spotlight']['data']['recentlyAddedList'][i]
    new_coin_syms.append(new_coini['symbol'])
    new_coin_prices.append('$' + f"{round(new_coini['priceChange']['price'],5)}")
    new_coin_Change24h.append(f"{round(new_coini['priceChange']['priceChange24h'],2)}" + '%')
  
  new, gain, loser=st.columns(3)
  newcoin={'Coin':new_coin_syms, 'Price':new_coin_prices, 'Change24h':new_coin_Change24h}
  new.subheader('Newly added coins')
  new.table(newcoin)

  ### Top 3 gainers and losers Coins
  data_gain_lose0 = soup_gain_lose.find('script', id='__NEXT_DATA__', type='application/json')
  data_gain_lose = json.loads(data_gain_lose0.contents[0])

  gainers= json.loads(data_gain_lose['props']['initialState'])['cryptocurrency']['gainersLosers']['gainers']
  gainer_prices = ["$" + f"{round(gainers[0]['priceChange']['price'],4)}",
                  "$" + f"{round(gainers[1]['priceChange']['price'],4)}",
                  "$" + f"{round(gainers[2]['priceChange']['price'],4)}"]
  gainer_chag24h = [f"{round(gainers[0]['priceChange']['priceChange24h'],2)}" + "%",
                  f"{round(gainers[1]['priceChange']['priceChange24h'],2)}" + "%",
                  f"{round(gainers[2]['priceChange']['priceChange24h'],2)}" + "%"]
  gainerdict={'Coin':[gainers[0]['symbol'],gainers[1]['symbol'],gainers[2]['symbol']],
              'Price':gainer_prices,
              'Change24h':gainer_chag24h}

  gain.subheader('Top 3 Gainers')
  gain.table(gainerdict)

  losers= json.loads(data_gain_lose['props']['initialState'])['cryptocurrency']['gainersLosers']['losers']
  loser_prices = ["$" + f"{round(losers[0]['priceChange']['price'],4)}",
                  "$" + f"{round(losers[1]['priceChange']['price'],4)}",
                  "$" + f"{round(losers[2]['priceChange']['price'],4)}"]
  loser_chag24h = [f"{round(losers[0]['priceChange']['priceChange24h'],2)}" + "%",
                  f"{round(losers[1]['priceChange']['priceChange24h'],2)}" + "%",
                  f"{round(losers[2]['priceChange']['priceChange24h'],2)}" + "%"]
  loserdict={'Coin':[losers[0]['symbol'],losers[1]['symbol'],losers[2]['symbol']],
              'Price':loser_prices,
              'Change24h':loser_chag24h}
  loser.subheader('Top 3 losers')
  loser.table(loserdict)

# Exchange Platforms
  st.markdown(
      """
      <h1>Top Exchange Platforms</h1>
      """
  , unsafe_allow_html=True)
  # str(f"{():,}")
  ### Table of top exchanges
  data = soup_exch.find('script', id='__NEXT_DATA__', type='application/json')
  exchange_data0 = json.loads(data.contents[0])
  exchange_data = exchange_data0['props']['pageProps']['exchange']

  table_html = """<table class="table table-striped table-hover table-borderless text-right">
      <thead>
          <tr>
              <th scope="col">#</th>
              <th scope="col">Exchange</th>
              <th scope="col">Score</th>
              <th scope="col">Markets</th>
              <th scope="col">Coins</th>
              <th scope="col">Vol24h</th>
              <th scope="col">Visits7d</th>
          </tr>
      </thead>
      <tbody>
  """
  ##### select top 20 exchanges to display in the table
  exchange_vol24h = []
  exchange_name = []
  for i in range(20):#range(len(exchange_data)):
    exchange_vol24h.append(exchange_data[i]['spotVol24h'])

    if 'Exchange' in exchange_data[i]['name']:
      name = exchange_data[i]['name'].replace('Exchange','')
    else:
      name = exchange_data[i]['name']
    exchange_name.append(name)

    table_html += f"""<tr>
              <th scope="row">{i + 1}</th>
              <td>{name}</td>
              <td>{round(exchange_data[i]['score'],2)}</td>
              <td>{exchange_data[i]['numMarkets']}</td>
              <td>{exchange_data[i]['numCoins']}</td>
              <td>{'$' + str(f"{(round(exchange_data[i]['spotVol24h'],1)):,}")}</td>
              <td>{str(f"{(exchange_data[i]['visits']):,}")}</td>
          </tr>
      """
  table_html += """</tbody>
  </table>"""

  st.markdown(table_html, unsafe_allow_html=True)




  ###### plot market cap percentages by coins
  listings = json.loads(coin_data['props']['initialState'])['cryptocurrency']['listingLatest']['data']
  market_cap = []
  coin_symbol = []
  market_cap_name = []

  for i in listings[1:10]:
      coin_symbol.append(i[[k for k, j in enumerate(listings[0]['keysArr']) if j == 'symbol'][0]])

      market_cap_name = 'quote.USD.marketCap'
      market_cap.append(i[[k for k, j in enumerate(listings[0]['keysArr']) if j == market_cap_name][0]])
  market_cap_pct = []
  sum_pct = 0
  for i in market_cap:
    market_cap_pct.append(i/market_info['marketCap'])
    sum_pct += i/market_info['marketCap']
  
  market_cap_pct.append(1-sum_pct)
  coin_symbol.append('others')

  df_market_cap_pct = pd.DataFrame(list(zip(coin_symbol, market_cap_pct)), columns =['Coin', 'Percentages'])
  fig_market_cap_pct = go.Figure(data = [go.Pie(labels=df_market_cap_pct['Coin'], 
                                                values=df_market_cap_pct['Percentages'], hole=.3)])
  fig_market_cap_pct.update_layout(margin=margin_setup)

  #### plot market cap percentages by exchanges
  exchange_vol24h_pct = []
  for i in exchange_vol24h:
      exchange_vol24h_pct.append(i/market_info['totalVol']*100)

  sort_index = np.argsort(np.asarray(exchange_vol24h_pct))
  top_exchange_vol24h_pct = []

  top_exchange_vol24h = []
  for i in range(-5,0):
      top_exchange_vol24h_pct.append(exchange_vol24h_pct[sort_index[i]])
      top_exchange_vol24h.append(exchange_name[sort_index[i]])

  df_vol24h_pct_exch = pd.DataFrame(list(zip(top_exchange_vol24h, top_exchange_vol24h_pct)),
                                    columns =['Exchanges', 'Percentages of market volume'])

  fig_top_exch_vol24h = px.bar(df_vol24h_pct_exch, y='Percentages of market volume', x='Exchanges', text='Percentages of market volume',
                                color="Exchanges", orientation='v',
                                labels=dict(top_exchange_vol24h_pct="Percentages of market volume", top_exchange_vol24h="Exchange"))
  
  fig_top_exch_vol24h.update_traces(texttemplate='%{text:.4s}', textposition='outside')
  fig_top_exch_vol24h.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', showlegend=False)

  st.markdown(
    """
    <h1>Dominance</h1>
    """
  , unsafe_allow_html=True)
  marketcappct_coin, marketcappct_exch=st.columns(2)
  marketcappct_coin.subheader('Market caps by cryptos')
  marketcappct_coin.plotly_chart(fig_market_cap_pct, use_container_width=True)

  marketcappct_exch.subheader('Volume24h by exchanges')
  marketcappct_exch.plotly_chart(fig_top_exch_vol24h, use_container_width=True)

  
