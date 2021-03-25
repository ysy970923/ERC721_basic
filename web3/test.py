from web3 import Web3
import json
import boto3
import hashlib
import io

ganache_url = 'http://127.0.0.1:7545'

contractAddress = '0x4803b5fE98A301C108e8b1db3ACADb7aa4F27097'

web3 = Web3(Web3.HTTPProvider(ganache_url, request_kwargs={'timeout': 120}))

accounts = web3.eth.accounts

truffleFile = json.load(open('../build/contracts/UniqueAsset.json', encoding='utf-8'))

abi = truffleFile['abi']

contract = web3.eth.contract(address=contractAddress, abi=abi)

file_name = 'digital_assets/dpr.png'
bucket = 'nft-testing-ysy'
key = 'digital_assets/dpr.png'

s3 = boto3.client('s3')
res = s3.upload_file(file_name, bucket, key)

f = open(file_name, 'rb')
data = f.read()
f.close()

filehash = hashlib.md5(data).hexdigest()
print(filehash)

tx_hash = contract.functions.createToken(filehash, web3.toWei(5, 'ether')).transact({'from': accounts[0]})
web3.eth.waitForTransactionReceipt(tx_hash)

tx_hash = contract.functions.buyToken(1).transact({'from': accounts[1], 'value':web3.toWei(80, "ether")})
web3.eth.waitForTransactionReceipt(tx_hash)

owner = contract.functions.ownerOf(1).call({'from':accounts[0]})
print(owner)


