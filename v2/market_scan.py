from kucoin.client import Client
import kucoin
import config
import time
import methods

def pair_count():

    client = Client(config.api_key, config.api_secret)

    new_client = methods.New_client(client)

    markets = new_client.get_trading_markets()
    pairsdata = list()
    for i in markets:
        try:
            pairsdata.append(new_client.get_trading_symbols(i))
        except:
            try:
                pairsdata.append(new_client.get_trading_symbols(i))
            except:
                print('F*uck KuCoin')
    fullpairs = list()
    for i in pairsdata:
        for j in i:
            fullpairs.append(j['symbol'])

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

    return doublepairlist
