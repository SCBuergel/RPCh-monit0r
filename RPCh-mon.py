import matplotlib.pyplot as plt
from web3 import Web3
import time
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.ticker
import datetime

exitProvider = "https://primary.gnosis-chain.rpc.hoprtech.net"
endpoint = "http://localhost:8080/?exit-provider=" + exitProvider
timeout = 5
web3 = Web3(Web3.HTTPProvider(endpoint, request_kwargs={'timeout': timeout}))
results = []

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
ax.set_ylim(0.5, 30)

while True:
    start = time.time()
    try:
        blockNo = web3.eth.get_block_number()
    except:
        blockNo = 0
    end = time.time()
    latency = end - start
    print(f"block number: {blockNo}, took {latency:.2f}s")
    result = {
            "time": start,
            "latency": latency,
            "blockNumber": blockNo
            }
    results.append(result)
    latencies = [r["latency"] for r in results if r["blockNumber"] > 0]
    times = [r["time"] for r in results if r["blockNumber"] > 0]
    
    if len(times) == 0:
        continue

    dfAll = pd.DataFrame({
        "times": times,
        "latencies": latencies
        }, columns=["times", "latencies"])
    dfAll["times"] = dfAll["times"].astype("datetime64[s]")
    dfAll = dfAll.set_index("times")

    dfLast24h = dfAll[dfAll.index > dfAll.index[-1] - datetime.timedelta(hours=24)]
    dfLast1h = dfAll[dfAll.index > dfAll.index[-1] - datetime.timedelta(hours=1)]

    numTimeouts = len([r["latency"] for r in results if r["blockNumber"] == 0])
    numOverThreshold = len([r["latency"] for r in results if r["blockNumber"] > 0 and r["latency"] > timeout])
    
    print(f"number of requests that didn't time out: {len(latencies)}")
    print(f"number of timeouts: {numTimeouts}")
    print(f"number of requests that didn't time out book took over {timeout}s: {numOverThreshold}")
    
    plt.plot(dfAll["latencies"], "bo")
    plt.savefig("latencies-all.png")

    plt.plot(df24h["latencies"], "bo")
    plt.savefig("latencies-24h.png")

    plt.plot(df1h["latencies"], "bo")
    plt.savefig("latencies-1h.png")

    time.sleep(2)
