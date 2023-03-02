import matplotlib.pyplot as plt
from web3 import Web3
import time
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.ticker
import datetime

def newFig():
    plt.title("RPCh request latency over time")
    plt.xlabel("Time")
    plt.ylabel("Latency [s]")
    plt.yscale("log")
    plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20])
    ax = plt.gca()
    fig = plt.gcf()
    fig.set_size_inches(7, 7)
    xfmt = mdates.DateFormatter('%d-%m-%y %H:%M:%S')
    fig.autofmt_xdate(rotation=45)
    ax.xaxis.set_major_formatter(xfmt)
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_ylim(0.4, 30)

exitProvider = "https://primary.gnosis-chain.rpc.hoprtech.net"
endpoint = "http://localhost:8080/?exit-provider=" + exitProvider
timeout = 5
web3 = Web3(Web3.HTTPProvider(endpoint, request_kwargs={'timeout': timeout}))
results = []

dfAll = pd.read_csv("output/latencies.csv", compression="zip")
dfAll["time"] = dfAll["time"].astype("datetime64[s]")
dfAll = dfAll.set_index("time")

while True:
    start = datetime.datetime.now()
    try:
        blockNo = web3.eth.get_block_number()
    except:
        blockNo = 0
    end = datetime.datetime.now()
    latency = end - start
    print(f"block number: {blockNo}, took {latency}")
    dfAll.loc[start] = [latency.total_seconds(), blockNo]

    df24h = dfAll[dfAll.index > dfAll.index[-1] - datetime.timedelta(hours=24)]
    df1h = dfAll[dfAll.index > dfAll.index[-1] - datetime.timedelta(hours=1)]

    dfAllGotResponse = dfAll[dfAll["blockNumber"] > 0]
    dfAllNoResponse = dfAll[dfAll["blockNumber"] == 0]

    df24hGotResponse = df24h[df24h["blockNumber"] > 0]
    df24hNoResponse = df24h[df24h["blockNumber"] == 0]

    df1hGotResponse = df1h[df1h["blockNumber"] > 0]
    df1hNoResponse = df1h[df1h["blockNumber"] == 0]

    plt.figure(0)
    newFig()
    plt.plot(dfAllGotResponse["latency"], "bx")
    plt.plot(dfAllNoResponse["latency"], "rx")
    plt.savefig("output/latencies-all.png")

    plt.figure(1)
    newFig()
    plt.plot(df24hGotResponse["latency"], "bx")
    plt.plot(df24hNoResponse["latency"], "rx")
    plt.savefig("output/latencies-24h.png")

    plt.figure(2)
    newFig()
    plt.plot(df1hGotResponse["latency"], "bx")
    plt.plot(df1hNoResponse["latency"], "rx")
    plt.savefig("output/latencies-1h.png")

    dfAll.to_csv("output/latencies.csv", compression="zip")

    time.sleep(2)
