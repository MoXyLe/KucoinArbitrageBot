from kucoin.client import Client
import kucoin
import config
import time
import methods

client = Client(config.api_key, config.api_secret)
#
# client2 = methods.New_client(client)
#
# print(client2.get_coin_balance('ETH'))
# startbalance = client.get_total_balance('USD')
#
# print(startbalance)\
#
# path = r'C:\Users\roofu\Desktop\KuCoin\New_Bot\coins_files\BPT.txt'
# print(path)
# print(client.get_currencies('ETH'))

print(client.get_recent_orders('KCS-BTC', limit=2))
print(time.time())
