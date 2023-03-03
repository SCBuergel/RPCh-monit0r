import matplotlib.pyplot as plt
from web3 import Web3
import time
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import matplotlib.ticker
import datetime

def newFig():
    plt.title("RPCh request latency over time")
    plt.xlabel("Time (UTC)")
    plt.ylabel("Latency [s]")
    plt.yscale("log")
    plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5, 10, 20])
    ax = plt.gca()
    fig = plt.gcf()
    fig.set_size_inches(8, 8)
    xfmt = mdates.DateFormatter('%d-%m-%y %H:%M:%S')
    fig.autofmt_xdate(rotation=45)
    ax.xaxis.set_major_formatter(xfmt)
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_ylim(0.06, 30)

def newHist():
    plt.title("Distribution of RPCh response latency")
    plt.xlabel("Latency [s]")
    ax = plt.gca()
    fig = plt.gcf()
    fig.set_size_inches(7, 7)
    plt.yscale("log")
    ax.set_ylim(0.06, 30)
    plt.yticks([0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5, 10, 20])
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

exitProvider = "https://primary.gnosis-chain.rpc.hoprtech.net"
endpoint = "http://localhost:8080/?exit-provider=" + exitProvider
timeout = 5
web3 = Web3(Web3.HTTPProvider(endpoint, request_kwargs={'timeout': timeout}))

dfAll = pd.read_csv("output/latencies.csv", compression="zip")
dfAll["time"] = dfAll["time"].astype("datetime64[s]")
dfAll = dfAll.set_index("time")
logbins = np.geomspace(0.06, 30, 10)

while True:
    start = datetime.datetime.utcnow()
    try:
        blockNo = web3.eth.get_block_number()
    except:
        blockNo = 0
    end = datetime.datetime.utcnow()
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
    plt.figure(0).clear()
    newFig()
    plt.plot(dfAllGotResponse["latency"], "bo", mfc='none', label="Got response")
    plt.plot(dfAllNoResponse["latency"], "rx", label="Timed out")
    plt.legend(loc="upper left")
    plt.savefig("output/latencies-all.png", bbox_inches='tight')

    plt.figure(1)
    plt.figure(1).clear()
    newHist()
    plt.hist(dfAllGotResponse["latency"], bins=logbins, color="blue", orientation="horizontal")
    plt.savefig("output/hist-lat-all.png", bbox_inches='tight')

    plt.figure(2)
    plt.figure(2).clear()
    newFig()
    plt.plot(df24hGotResponse["latency"], "bo", mfc='none', label="Got response")
    plt.plot(df24hNoResponse["latency"], "rx", label="Timed out")
    plt.legend(loc="upper left")
    plt.savefig("output/latencies-24h.png", bbox_inches='tight')

    plt.figure(3)
    plt.figure(3).clear()
    newHist()
    plt.hist(df24hGotResponse["latency"], bins=logbins, color="blue", orientation="horizontal")
    plt.savefig("output/hist-lat-24h.png", bbox_inches='tight')

    plt.figure(4)
    plt.figure(4).clear()
    newFig()
    plt.plot(df1hGotResponse["latency"], "bo", mfc='none', label="Got response")
    plt.plot(df1hNoResponse["latency"], "rx", label="Timed out")
    plt.legend(loc="upper left")
    plt.savefig("output/latencies-1h.png", bbox_inches='tight')

    plt.figure(5)
    plt.figure(5).clear()
    newHist()
    plt.hist(df1hGotResponse["latency"], bins=logbins, color="blue", orientation="horizontal")
    plt.savefig("output/hist-lat-1h.png", bbox_inches='tight')

    dfAll.to_csv("output/latencies.csv", compression="zip")

    time.sleep(2)
