from web3 import Web3
import time

endpoint = "http://localhost:8080/?exit-provider=https://primary.gnosis-chain.rpc.hoprtech.net"
timeout = 5
web3 = Web3(Web3.HTTPProvider(endpoint, request_kwargs={'timeout': timeout}))

while True:
    start = time.time()
    try:
        blockNo = web3.eth.get_block_number()
    except:
        blockNo = 0
    end = time.time()
    latency = end - start
    print(f"block number: {blockNo}, took {latency:.2f}s")
    time.sleep(2)
