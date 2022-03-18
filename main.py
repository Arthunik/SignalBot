import os
from get_ticker import Get_Tickers 
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
from discord.ext import commands, tasks 
import pytz
import datetime as dt
import pandas as pd
import json

gt = Get_Tickers()

# tickers = gt.penny_stocks()

tz_pacific = pytz.timezone('US/Pacific')
datetime_pacific = dt.datetime.now(tz_pacific)
current_time = datetime_pacific.strftime("%H:%M:%S")
now = dt.datetime.now()
market_open = now.replace(hour=6, minute=30, second=0, microsecond=0, tzinfo=tz_pacific) # 6:30 am 
market_close = now.replace(hour=13, minute=0, second=0, microsecond=0, tzinfo=tz_pacific) # 1:00 pm  

bot = commands.Bot(command_prefix='!')
channel = int(os.environ['CHANNEL'])


@bot.event
async def on_ready():
  print("The bot is ready!")
  if datetime_pacific > market_open and datetime_pacific < market_close:
    print('market open')
    await bot.get_channel(channel).send("The market is open")

# shows current stocks
@bot.command(name='show_stocks')
async def stock(ctx,arg,arg1):
  # tickers_dataframe = pd.DataFrame({'Tickers' : tickers})
  try: 
    if arg1 == "us":
      current_ticker = TA_Handler(
        symbol="{}".format(arg),
        screener="america",
        exchange="NASDAQ",
        interval=Interval.INTERVAL_5_MINUTES,
      )
      print(pd.DataFrame.from_dict(current_ticker.get_analysis().moving_averages).iloc[10])
    elif arg1 == "cyb":
      current_ticker = TA_Handler(
        symbol="{}".format(arg),
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_5_MINUTES,
      )
    elif arg1 == "cyp":
      current_ticker = TA_Handler(
        symbol="{}".format(arg),
        screener="crypto",
        exchange="POLONIEX",
        interval=Interval.INTERVAL_5_MINUTES,
      )
    else:
      current_ticker = TA_Handler(
        symbol="{}".format(arg),
        screener="america",
        exchange="NASDAQ",
        interval=Interval.INTERVAL_5_MINUTES,
      )
    
    current_ticker_s = current_ticker.get_analysis().summary

    # print(gt.penny_stocks())
    await ctx.send('You passed {} Answer is {}'.format(arg,current_ticker_s["RECOMMENDATION"]))
  except (RuntimeError, Exception):
    await ctx.send('You passed {} it is INCORRECT Symbols'.format(arg))

# shows current time
@bot.command(name='show_time')
async def time(ctx):
  await ctx.send(current_time)
# shows current time
@bot.command(name='show_list')
async def list(ctx, arg, arg2):
  if str(arg2) == "index":
    data = pd.DataFrame(gt.index_stock())
  elif str(arg2) == "market":
    data = pd.DataFrame(gt.penny_stocks())
  else:
    data = pd.DataFrame(gt.symbols_stocks(str(arg2)))
  data = data.head(int(arg))
  for x,row in data.iterrows():
    print(row)
    await ctx.send(row[0]+"->"+row[1]+" ("+row[2]+")")


@tasks.loop(hours=1)
async def show_signal(arg):
  message_channel = bot.get_channel(channel)
  data = []
  # for ticker in tickers:
  #   print(ticker)
  
  current_ticker = TA_Handler(
    symbol="{}".format(arg),
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_5_MINUTES,
        # proxies={'http': 'http://0.0.0.0:8080', 'https': 'https://0.0.0.0:443'}
  )

    #     try:
    #         current_ticker = TA_Handler(
    #             symbol=ticker,
    #             screener="america",
    #             exchange="NASDAQ",
    #             interval=Interval.INTERVAL_5_MINUTES
    #         )
    #       # current_ticker = pd.DataFrame.from_dict(current_ticker.get_analysis().moving_averages)
  current_ticker = current_ticker.get_analysis().summary
    #         print(current_ticker)
    #         data.append({
    #             'ticker' : ticker,
    #             'signal' : current_ticker['RECOMMENDATION']
    #         })
    #       # signals.append(‘{} : {}’.format(ticker, current_ticker[‘RECOMMENDATION’]))
    #       # await message_channel.send(‘{} : {}’.format(ticker, current_ticker[‘RECOMMENDATION’]))
    #     except (RuntimeError, Exception) as e:
    #        # signals.append(‘{} : {}’.format(ticker, e))
    #         print('{} : {}'.format(ticker, e))
    # # signals = pd.DataFrame(data)
  # tesla = TA_Handler(
  #   symbol="TSLA",
  #   screener="america",
  #   exchange="NASDAQ",
  #   interval=Interval.INTERVAL_5_MINUTES,
  #     # proxies={'http': 'http://0.0.0.0:8080', 'https': 'https://0.0.0.0:443'}
  # )
  # print(current_ticker)
  data.append({'ticker' : "{}".format(arg),
               'signal' :current_ticker['RECOMMENDATION']})
  # signals = pd.DataFrame(data)
    # print(pd.DataFrame(data))
  await message_channel.send(data)
       # await message_channel.send(data)
@show_signal.before_loop
async def before():
  await bot.wait_until_ready()


show_signal.start("AAPL")
token = os.environ['TOKEN']
bot.run(token)