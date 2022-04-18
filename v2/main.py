from kucoin.client import Client
from multiprocessing import Process
import kucoin
import config
import time
from orders import calculateOrders
from market_scan import pair_count
import os

def first_func(doublepairlist, i):
    # name = number
    #
    # if name == '1':
    #     client = Client(config.api_key, config.api_secret)
    # elif name == '2':
    #     client = Client(config.api_key2, config.api_secret2)
    # else:
    if i == 1:
        process_file = open('process.txt', 'w')
        process_file.write(str(os.getpid()))
        process_file.close()

    client = Client(config.api_key, config.api_secret)

    while True:
        for i in doublepairlist:
            if i[0].split('-')[0] != i[1].split('-')[0]:
                continue
            # if ('ETH' not in i[2] or 'BTC' not in i[2]):
            calculateOrders(i)

if __name__ == '__main__':
    pair_list = pair_count()

    length = len(pair_list) // 5

    if len(pair_list) % 5 != 0:
        length += 1

    for i in range(1, length + 1):
        pairs = list()
        if i != length:
            for a in range((i * 5) - 5, i * 5):
                pairs.append(pair_list[a])
        else:
            for a in range((i * 5) - 5, len(pair_list)):
                pairs.append(pair_list[a])
        Process(target=first_func, args=(pairs, i,)).start()

        print('Process Started')
        time.sleep(0.3)
