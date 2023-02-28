from web3 import Web3
import time

endpoint = "http://localhost:8080/?exit-provider=https://primary.gnosis-chain.rpc.hoprtech.net"
web3 = Web3(Web3.HTTPProvider(endpoint))

while True:
    start = time.time()
    blockNo = web3.eth.get_block_number()
    end = time.time()
    latency = end - start
    print(f"block number: {blockNo}, took {latency:.2f}s")
    time.sleep(1)
