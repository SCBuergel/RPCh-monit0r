from web3 import Web3
import time

endpoint = "http://localhost:8080/?exit-provider=https://primary.gnosis-chain.rpc.hoprtech.net"
timeout = 5
web3 = Web3(Web3.HTTPProvider(endpoint, request_kwargs={'timeout': timeout}))
results = []

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
    numTimeouts = len([r["latency"] for r in results if r["blockNumber"] == 0])
    numOverThreshold = len([r["latency"] for r in results if r["blockNumber"] > 0 and r["latency"] > timeout])
    print(f"number of requests that didn't time out: {len(latencies)}")
    print(f"number of timeouts: {numTimeouts}")
    print(f"number of requests that didn't time out book took over {timeout}s: {numOverThreshold}")
    time.sleep(2)
