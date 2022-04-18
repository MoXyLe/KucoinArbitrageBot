from kucoin.client import Client
import kucoin
import time

api_key = '5a7dbf7272455a3b24bad060'
api_secret = '22ba7c11-12b5-4594-9ae0-8e230175daa9'
client = Client(api_key, api_secret)
markets = client.get_trading_markets()
trading_symbols = list()
unsortedpairs = list()

for i in markets:
    trading_symbols.append(client.get_trading_symbols(i))

for i in trading_symbols:
    for j in i:
        unsortedpairs.append(j['symbol'])

combinedpairs = dict()
pairnumber = 0

for i in range(0,len(unsortedpairs)):
    a = unsortedpairs[i].split('-')
    pairnumber += 1
    justlist = list()
    justlist.append(unsortedpairs[i])
    if pairnumber <= len(unsortedpairs) - 1:
        for j in range(pairnumber,len(unsortedpairs)):
            b = unsortedpairs[j].split('-')
            if a[0] == b[0]:
                justlist.append(unsortedpairs[j])
    if a[0] not in combinedpairs:
        combinedpairs[a[0]] = justlist

deletedCoins = list()

for i,j in combinedpairs.items():
    if len(j) == 1:
        deletedCoins.append(i)
for i in deletedCoins:
    combinedpairs.pop(i)

sortedpairs = list()

for i in combinedpairs.values():
    count = 1
    for j in range(0,len(i)):
        if count != len(i):
            for f in range(count, len(i)):
                sortedpairs.append([i[j], i[f]])
            count += 1

for i in sortedpairs:
    j = i[0].split('-')
    f = i[1].split('-')
    i.append(f'{f[1]}-{j[1]}')

print(len(sortedpairs))

for i in sortedpairs:
    if i[0].split('-')[0] != i[1].split('-')[0]:
        continue
    if 'BTC' not in i[2]:
        continue
    orderbooks = dict()
    number = 0
    threepairs = list()
    for j in i:
        a = j.split('-')
        #requests += 1
        try:
            orders = client.get_order_book(f'{a[0]}-{a[1]}', limit=3)
            orderbooks[f'{a[0]}-{a[1]}'] = orders['SELL'], orders['BUY']
            threepairs.append(f'{a[0]}-{a[1]}')
        except kucoin.exceptions.KucoinAPIException or kucoin.exceptions.KucoinResponseException or IndexError or requests.exceptions.ConnectionError:
            try:
                orders = client.get_order_book(f'{a[1]}-{a[0]}', limit=3)
                orderbooks[f'{a[1]}-{a[0]}'] = orders['SELL'], orders['BUY']
                threepairs.append(f'{a[1]}-{a[0]}')
                number = 1
            except kucoin.exceptions.KucoinAPIException or kucoin.exceptions.KucoinResponseException or IndexError:
                pass
    print(f'orderbooks - {orderbooks}\nthreepairs - {threepairs}')
