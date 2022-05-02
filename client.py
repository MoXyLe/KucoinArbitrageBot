from kucoin.client import Client
import kucoin
import time
from calculate_amount import calculate
import requests
from multiprocessing import Pool
from keys import api_key, api_secret

print(time.clock())
client = Client(api_key, api_secret)
markets = client.get_trading_markets()
pairsdata = list()
# for i in markets:
#     pairsdata.append(client.get_trading_symbols(i))
pairsdata.append('KCS-BTC')
pairsdata.append('KCS-USDT')
pairsdata.append('BTC-USDT')

fullpairs = list()
for i in pairsdata:
    # for j in i:
        # fullpairs.append(j['symbol'])
    fullpairs.append(i)

combinedpairs = dict()
pairnumber = 0
for i in range(0,len(fullpairs)):
    a = fullpairs[i].split('-')
    pairnumber += 1
    justlist = list()
    justlist.append(fullpairs[i])
    if pairnumber <= len(fullpairs) - 1:
        for j in range(pairnumber,len(fullpairs)):
            b = fullpairs[j].split('-')
            if a[0] == b[0]:
                justlist.append(fullpairs[j])
    if a[0] not in combinedpairs:
        combinedpairs[a[0]] = justlist

deletedCoins = list()
for i,j in combinedpairs.items():
    if len(j) == 1:
        deletedCoins.append(i)
for i in deletedCoins:
    combinedpairs.pop(i)

doublepairlist = list()

for i in combinedpairs.values():
    count = 1
    for j in range(0,len(i)):
        if count != len(i):
            for f in range(count, len(i)):
                doublepairlist.append([i[j], i[f]])
            count += 1

for i in doublepairlist:
    j = i[0].split('-')
    f = i[1].split('-')
    i.append(f'{f[1]}-{j[1]}')

print(len(doublepairlist))

# requests = 0
# percentslist = dict()
#while True:
def getpairs():
    while True:
        for i in doublepairlist:
            if i[0].split('-')[0] != i[1].split('-')[0]:
                continue
            if 'BTC' not in i[2]:
                continue
            orderbooks = dict()
            number = 0
            potential = dict()
            threepairs = list()
            print(f'i - {i}')
            for j in i:
                a = j.split('-')
                #requests += 1
                try:
                    orders = client.get_order_book(f'{a[0]}-{a[1]}', limit=1)
                    orderbooks[f'{a[0]}-{a[1]}'] = orders['SELL'], orders['BUY']
                    threepairs.append(f'{a[0]}-{a[1]}')
                except kucoin.exceptions.KucoinAPIException or kucoin.exceptions.KucoinResponseException or IndexError or requests.exceptions.ConnectionError:
                    try:
                        orders = client.get_order_book(f'{a[1]}-{a[0]}', limit=1)
                        orderbooks[f'{a[1]}-{a[0]}'] = orders['SELL'], orders['BUY']
                        threepairs.append(f'{a[1]}-{a[0]}')
                        number = 1
                    except kucoin.exceptions.KucoinAPIException or kucoin.exceptions.KucoinResponseException or IndexError:
                        pass
            # print(orderbooks)
            firstformula = list()
            firstcoinamount = []
            for h in orderbooks.values():
                if h != None and type(h[0]) != type(None) and type(h[1]) != type(None):
                    try:
                        firstformula.append((h[0][0][0],h[1][0][0]))
                        firstcoinamount.append(h)
                        # print('h = ', h)
                    except IndexError or TypeError:
                        pass
            calculate(number, firstformula, threepairs, firstcoinamount, client, orderbooks)
            time.sleep(10)
    # input("Continue? ")
# percentslist.sort()
# print(percentslist)

if __name__ == '__main__':
    # pool = Pool(processes=5)     # runs in *only* one process
    # res = pool.apply_async(getpairs, (loopcount, ))
    # print(res.get(timeout=160)
    getpairs()
# print(requests)
print(time.clock())
print(time.localtime())
