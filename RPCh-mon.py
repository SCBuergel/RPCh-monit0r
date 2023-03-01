import matplotlib.pyplot as plt
from web3 import Web3
import time
import matplotlib.dates as mdates
import pandas as pd

endpoint = "http://localhost:8080/?exit-provider=https://primary.gnosis-chain.rpc.hoprtech.net"
timeout = 5
web3 = Web3(Web3.HTTPProvider(endpoint, request_kwargs={'timeout': timeout}))
results = []

plt.title("RPCh request latency over time")
plt.xlabel("Time")
plt.ylabel("Latency")
plt.yscale("log")
ax = plt.gca()
fig = plt.gcf()
fig.set_size_inches(7, 7)
xfmt = mdates.DateFormatter('%d-%m-%y %H:%M:%S')
fig.autofmt_xdate(rotation=45)
ax.xaxis.set_major_formatter(xfmt)

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
    df = pd.DataFrame({
        "times": times,
        "latencies": latencies
        }, columns=["times", "latencies"])
    df["times"] = df["times"].astype("datetime64[s]")
    df = df.set_index("times")

    numTimeouts = len([r["latency"] for r in results if r["blockNumber"] == 0])
    numOverThreshold = len([r["latency"] for r in results if r["blockNumber"] > 0 and r["latency"] > timeout])
    print(f"number of requests that didn't time out: {len(latencies)}")
    print(f"number of timeouts: {numTimeouts}")
    print(f"number of requests that didn't time out book took over {timeout}s: {numOverThreshold}")
    plt.plot(df["latencies"], "bo")
    plt.savefig("fig.png")

    time.sleep(2)
