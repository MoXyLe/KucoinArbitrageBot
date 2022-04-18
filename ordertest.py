from kucoin.client import Client
import kucoin
import time

api_key = '5a7dbf7272455a3b24bad060'
api_secret = '22ba7c11-12b5-4594-9ae0-8e230175daa9'
client = Client(api_key, api_secret)
try:
    print(time.clock())
    transaction = client.create_order('GAS-BTC', Client.SIDE_BUY, '0.004', '0.1')
    print(time.clock())
    print(transaction)
    time.sleep(1)
    orders = client.get_order_details('GAS-BTC', Client.SIDE_BUY, 1, 1, order_id=transaction['orderOid'])
    print(time.clock())
    print(orders)
    print(client.cancel_order(transaction["orderOid"], 'BUY', 'GAS-BTC'))
    print(time.clock())
except (kucoin.exceptions.KucoinAPIException or kucoin.exceptions.KucoinResponseException) as error:
    print(error)
