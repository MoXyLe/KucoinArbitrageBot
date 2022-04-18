from kucoin.client import Client
import kucoin
import config
import time
from buyer import buy_coin
import methods
import traceback
import os

def calculateOrders(i):
    # if name == '1':
    #     client = Client(config.api_key, config.api_secret)
    # elif name == '2':
    #     client = Client(config.api_key2, config.api_secret2)
    # else:
    client = Client(config.api_key, config.api_secret)
    new_client = methods.New_client(client)
    start_time = time.time()
    potential = 0
    attempt = 0
    reloading = False
    best_order = 0
    if start_time % 900 < 10:
        process_file = open('process.txt', 'r')
        process_read = process_file.read()
        if str(os.getpid()) in process_read:
            coins_file = open('coins1.txt', 'r')
            coins_read = coins_file.read()
            coins_file.close()
            coins_file = open('coins1.txt', 'w')
            coins_file.write(coins_read.replace('1', '0'))
            coins_file.close()
            # coins_file = open('BTC1.txt', 'w')
            # coins_file.write('0.0')
            # coins_file.close()
            # coins_file = open('ETH1.txt', 'w')
            # coins_file.write('0.0')
            # coins_file.close()
            # coins_file = open('USDT1.txt', 'w')
            # coins_file.write('0.0')
            # coins_file.close()
            # coins_file = open('NEO1.txt', 'w')
            # coins_file.write('0.0')
            # coins_file.close()
            # coins_file = open('KCS1.txt', 'w')
            # coins_file.write('0.0')
            # coins_file.close()
        time.sleep(10)
    while (potential == 1 or attempt == 0) and time.time() - 1800 < start_time:
        if attempt == 0:
            start_time = time.time()
        orderbooks = dict()
        number = 0
        threepairs = list()
        for j in i:
            a = j.split('-')
            try:
                orders = client.get_order_book(f'{a[0]}-{a[1]}', limit=3)
                if orders != None:
                    orderbooks[f'{a[0]}-{a[1]}'] = orders['SELL'], orders['BUY']
                else:
                    break
                threepairs.append(f'{a[0]}-{a[1]}')
            except Exception as error:
                try:
                    orders = client.get_order_book(f'{a[1]}-{a[0]}', limit=3)
                    if orders != None:
                        orderbooks[f'{a[1]}-{a[0]}'] = orders['SELL'], orders['BUY']
                    else:
                        break
                    threepairs.append(f'{a[1]}-{a[0]}')
                    number = 1
                except Exception as error:
                    break
        if number == 1:
            try:
                try:
                    percentage1 = (orderbooks[threepairs[0]][1][0][0] + (attempt+1)*(0.1**len(str(orderbooks[threepairs[0]][1][0][0]).split('.')[1])))/orderbooks[threepairs[1]][1][1][0]*orderbooks[threepairs[2]][0][2][0]
                except TypeError:
                    print('TypeError')
                    continue
                try:
                    percentage2 = (orderbooks[threepairs[1]][1][0][0] + (attempt+1)*(0.1**len(str(orderbooks[threepairs[1]][1][0][0]).split('.')[1])))/orderbooks[threepairs[0]][1][1][0]/orderbooks[threepairs[2]][1][2][0]
                except TypeError:
                    print('TypeError')
                    continue
                try:
                    tick1 = new_client.get_tick(threepairs[0])
                    products1 = new_client.get_currencies(tick1['coinType'])['rates'][tick1['coinType']]['USD']
                    volume1 = products1 * tick1['vol']
                    tick2 = new_client.get_tick(threepairs[1])
                    products2 = new_client.get_currencies(tick2['coinType'])['rates'][tick2['coinType']]['USD']
                    volume2 = products2 * tick2['vol']
                except:
                    print('Error')
                    continue
                # my_file = open(f"data1.txt", "r")
                # read = my_file.read()
                # my_file.close()
                if percentage1 < 0.995 and volume2 > 10000 and percentage1 > 0.8:
                    if attempt == 0 and reloading == False:
                        print('Reloading')
                        reloading = True
                        best_order = orderbooks[threepairs[1]][1][0][0]
                        time.sleep(15)
                        continue
                    # my_file = open(f"data1.txt", "a")
                    # my_file.write(threepairs[2])
                    # my_file.close()
                    if attempt == 1 and orderbooks[threepairs[1]][1][0][0] < best_order:
                        potential = 0
                        print('Price changed')
                        continue
                    orders = new_client.get_recent_orders(threepairs[1])
                    if orderbooks[threepairs[1]][1][0][0] / orders[len(orders)-1][2] > 1.03:
                        potential = 0
                        print('Too big price, not safe')
                        continue
                    coin_file = open(f'coins1.txt', 'r')
                    print('File opened')
                    coin_read = coin_file.read()
                    print('File read')
                    coin_file.close()
                    coin_name = threepairs[0].split('-')[0]
                    if f'{coin_name}-1' in coin_read:
                        print('Coin is already buying')
                        return 0
                    elif f'{coin_name}-0' in coin_read:
                        coin_file_2 = open(f'coins1.txt', 'w')
                        coin_read = coin_read.replace(f'{coin_name}-0', f'{coin_name}-1')
                        coin_file_2.write(coin_read)
                        coin_file_2.close()
                    else:
                        coin_file_2 = open(f'coins1.txt', 'a')
                        coin_file_2.write(f'{coin_name}-1')
                        coin_file_2.close()
                    price = round(orderbooks[threepairs[0]][1][0][0] + (attempt+1)*(0.1**len(str(orderbooks[threepairs[0]][1][0][0]).split('.')[1])), len(str(orderbooks[threepairs[0]][1][0][0]).split('.')[1]) + 1)
                    print(f'Orderbooks - {orderbooks}')
                    print(f'Threepairs - {threepairs}')
                    print('first perc', percentage1)
                    print(f'volume - {volume1}')
                    print(f'price - {price}')
                    buy_amount = orderbooks[threepairs[1]][1][1][1]
                    alt_buy_amount = orderbooks[threepairs[1]][1][1][2] / orderbooks[threepairs[2]][0][0][0]
                    if orderbooks[threepairs[1]][1][2][1] < buy_amount:
                        buy_amount = orderbooks[threepairs[1]][1][2][1]
                        alt_buy_amount = orderbooks[threepairs[1]][1][2][2] / orderbooks[threepairs[2]][0][0][0]
                    potential = buy_coin(number, [1, percentage1], threepairs, orderbooks, buy_amount, alt_buy_amount, price, client, 1)
                    print('potential -', potential)
                    print(buy_amount)
                    print(alt_buy_amount)
                    coin_file = open(f'coins1.txt', 'r')
                    coin_read = coin_file.read()
                    coin_file.close()
                    if f'{coin_name}-1' in coin_read:
                        coin_read = coin_read.replace(f'{coin_name}-1', f'{coin_name}-0')
                        coin_file = open(f'coins1.txt', 'w')
                        coin_file.write(coin_read)
                        coin_file.close()
                    else:
                        print('Coin not found in file')
                    # my_file = open(f"data1.txt", "r")
                    # new_read = my_file.read().replace(threepairs[2], '')
                    # my_file.close()
                    # my_file = open(f"data1.txt", "w")
                    # my_file.write(new_read)
                    # my_file.close()
                elif percentage2 < 0.995 and volume1 > 10000 and percentage2 > 0.8:
                    # my_file = open(f"data1.txt", "a")
                    # my_file.write(threepairs[2])
                    # my_file.close()
                    if attempt == 0 and reloading == False:
                        print('Reloading')
                        reloading = True
                        best_order = orderbooks[threepairs[0]][1][0][0]
                        time.sleep(15)
                        continue
                    if attempt == 1 and best_order > orderbooks[threepairs[0]][1][0][0]:
                        potential = 0
                        print('Price changed')
                        continue
                    orders = new_client.get_recent_orders(threepairs[0])
                    if orderbooks[threepairs[0]][1][0][0] / orders[len(orders)-1][2] > 1.03:
                        potential = 0
                        print('Too big price, not safe')
                        continue
                    coin_file = open(f'coins1.txt', 'r')
                    print('File opened')
                    coin_read = coin_file.read()
                    print('File read')
                    coin_file.close()
                    coin_name = threepairs[0].split('-')[0]
                    if f'{coin_name}-1' in coin_read:
                        print('Coin is already buying')
                        return 0
                    elif f'{coin_name}-0' in coin_read:
                        coin_file_2 = open(f'coins1.txt', 'w')
                        coin_read = coin_read.replace(f'{coin_name}-0', f'{coin_name}-1')
                        coin_file_2.write(coin_read)
                        coin_file_2.close()
                    else:
                        coin_file_2 = open(f'coins1.txt', 'a')
                        coin_file_2.write(f'{coin_name}-1')
                        coin_file_2.close()
                    price = round(orderbooks[threepairs[1]][1][0][0] + (attempt+1)*(0.1**len(str(orderbooks[threepairs[1]][1][0][0]).split('.')[1])), len(str(orderbooks[threepairs[1]][1][0][0]).split('.')[1]) + 1)
                    print(f'Orderbooks - {orderbooks}')
                    print(f'Threepairs - {threepairs}')
                    print('second perc', percentage2)
                    print(f'volume - {volume2}')
                    print(f'price - {price}')
                    buy_amount = orderbooks[threepairs[0]][1][1][1]
                    alt_buy_amount = orderbooks[threepairs[0]][1][1][2] * orderbooks[threepairs[2]][0][0][0]
                    if orderbooks[threepairs[0]][1][2][1] < buy_amount:
                        buy_amount = orderbooks[threepairs[0]][1][2][1]
                        alt_buy_amount = orderbooks[threepairs[0]][1][2][2] * orderbooks[threepairs[2]][0][0][0]
                    potential = buy_coin(number, [2, percentage2], threepairs, orderbooks, buy_amount, alt_buy_amount, price, client, 1)
                    print('potential -', potential)
                    print(buy_amount)
                    print(alt_buy_amount)
                    coin_file = open(f'coins1.txt', 'r')
                    coin_read = coin_file.read()
                    coin_file.close()
                    if f'{coin_name}-1' in coin_read:
                        coin_read = coin_read.replace(f'{coin_name}-1', f'{coin_name}-0')
                        coin_file = open(f'coins1.txt', 'w')
                        coin_file.write(coin_read)
                        coin_file.close()
                    else:
                        print('Coin not found in file')
                    # my_file = open(f"data1.txt", "r")
                    # new_read = my_file.read().replace(threepairs[2], '')
                    # my_file.close()
                    # my_file = open(f"data1.txt", "w")
                    # my_file.write(new_read)
                    # my_file.close()
                else:
                    print('Searching for suitable pair')
                    # print(percentage1, percentage2)
                    potential = 0
            except Exception as error:
                if 'list index out of range' not in str(error):
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write('\n')
                    stored_data.write(str(error))
                    stored_data.write(str(traceback.format_exc()))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                time.sleep(3)
        else:
            try:
                try:
                    percentage1 = (orderbooks[threepairs[0]][1][0][0] + (0.1**len(str(orderbooks[threepairs[0]][1][0][0]).split('.')[1])))/orderbooks[threepairs[1]][1][1][0]/orderbooks[threepairs[2]][1][2][0]
                except TypeError:
                    print('TypeError')
                    continue
                try:
                    percentage2 = (orderbooks[threepairs[1]][1][0][0] + (0.1**len(str(orderbooks[threepairs[1]][1][0][0]).split('.')[1])))/orderbooks[threepairs[0]][1][1][0]*orderbooks[threepairs[2]][0][2][0]
                except TypeError:
                    print('TypeError')
                    continue
                try:
                    tick1 = new_client.get_tick(threepairs[0])
                    products1 = new_client.get_currencies(tick1['coinType'])['rates'][tick1['coinType']]['USD']
                    volume1 = products1 * tick1['vol']
                    tick2 = new_client.get_tick(threepairs[1])
                    products2 = new_client.get_currencies(tick2['coinType'])['rates'][tick2['coinType']]['USD']
                    volume2 = products2 * tick2['vol']
                except:
                    print('Error')
                    continue
                # my_file = open(f"data1.txt", "r")
                # read = my_file.read()
                # my_file.close()
                if percentage1 < 0.995 and volume2 > 10000 and percentage1 > 0.8:
                    # my_file = open(f"data1.txt", "a")
                    # my_file.write(threepairs[2])
                    # my_file.close()
                    if attempt == 0 and reloading == False:
                        print('Reloading')
                        reloading = True
                        best_order = orderbooks[threepairs[1]][1][0][0]
                        time.sleep(15)
                        continue
                    if attempt == 1 and best_order > orderbooks[threepairs[1]][1][0][0]:
                        potential = 0
                        print('Price changed')
                        continue
                    orders = new_client.get_recent_orders(threepairs[1])
                    if orderbooks[threepairs[1]][1][0][0] / orders[len(orders)-1][2] > 1.03:
                        potential = 0
                        print('Too big price, not safe')
                        continue
                    coin_file = open(f'coins1.txt', 'r')
                    print('File opened')
                    coin_read = coin_file.read()
                    print('File read')
                    coin_file.close()
                    coin_name = threepairs[0].split('-')[0]
                    if f'{coin_name}-1' in coin_read:
                        print('Coin is already buying')
                        return 0
                    elif f'{coin_name}-0' in coin_read:
                        coin_file_2 = open(f'coins1.txt', 'w')
                        coin_read = coin_read.replace(f'{coin_name}-0', f'{coin_name}-1')
                        coin_file_2.write(coin_read)
                        coin_file_2.close()
                    else:
                        coin_file_2 = open(f'coins1.txt', 'a')
                        coin_file_2.write(f'{coin_name}-1')
                        coin_file_2.close()
                    price = round(orderbooks[threepairs[0]][1][0][0] + (0.1**len(str(orderbooks[threepairs[0]][1][0][0]).split('.')[1])), len(str(orderbooks[threepairs[0]][1][0][0]).split('.')[1]) + 1)
                    print(f'Orderbooks - {orderbooks}')
                    print(f'Threepairs - {threepairs}')
                    print('first perc', percentage1)
                    print(f'volume - {volume1}')
                    print(f'price - {price}')
                    buy_amount = orderbooks[threepairs[1]][1][1][1]
                    alt_buy_amount = orderbooks[threepairs[1]][1][1][2] * orderbooks[threepairs[2]][0][0][0]
                    if orderbooks[threepairs[1]][1][2][1] < buy_amount:
                        buy_amount = orderbooks[threepairs[1]][1][2][1]
                        alt_buy_amount = orderbooks[threepairs[1]][1][2][2] * orderbooks[threepairs[2]][0][0][0]
                    potential = buy_coin(number, [1, percentage1], threepairs, orderbooks, buy_amount, alt_buy_amount, price, client, 1)
                    coin_file = open(f'coins1.txt', 'r')
                    coin_read = coin_file.read()
                    coin_file.close()
                    if f'{coin_name}-1' in coin_read:
                        coin_read = coin_read.replace(f'{coin_name}-1', f'{coin_name}-0')
                        coin_file = open(f'coins1.txt', 'w')
                        coin_file.write(coin_read)
                        coin_file.close()
                    else:
                        print('Coin not found in file')
                    print('potential -', potential)
                    print(buy_amount)
                    print(alt_buy_amount)
                    # my_file = open(f"data1.txt", "r")
                    # new_read = my_file.read().replace(threepairs[2], '')
                    # my_file.close()
                    # my_file = open(f"data1.txt", "w")
                    # my_file.write(new_read)
                    # my_file.close()
                elif percentage2 < 0.995 and volume1 > 10000 and percentage2 > 0.8:
                    # my_file = open(f"data1.txt", "a")
                    # my_file.write(threepairs[2])
                    # my_file.close()
                    if attempt == 0 and reloading == False:
                        print('Reloading')
                        reloading = True
                        best_order = orderbooks[threepairs[0]][1][0][0]
                        time.sleep(15)
                        continue
                    if attempt == 1 and best_order > orderbooks[threepairs[0]][1][0][0]:
                        potential = 0
                        print('Price changed')
                        continue
                    orders = new_client.get_recent_orders(threepairs[0])
                    if orderbooks[threepairs[0]][1][0][0] / orders[len(orders)-1][2] > 1.03:
                        potential = 0
                        print('Too big price, not safe')
                        continue
                    coin_file = open(f'coins1.txt', 'r')
                    print('File opened')
                    coin_read = coin_file.read()
                    print('File read')
                    coin_file.close()
                    coin_name = threepairs[0].split('-')[0]
                    if f'{coin_name}-1' in coin_read:
                        print('Coin is already buying')
                        return 0
                    elif f'{coin_name}-0' in coin_read:
                        coin_file_2 = open(f'coins1.txt', 'w')
                        coin_read = coin_read.replace(f'{coin_name}-0', f'{coin_name}-1')
                        coin_file_2.write(coin_read)
                        coin_file_2.close()
                    else:
                        coin_file_2 = open(f'coins1.txt', 'a')
                        coin_file_2.write(f'{coin_name}-1')
                        coin_file_2.close()
                    price = round(orderbooks[threepairs[1]][1][0][0] + (0.1**len(str(orderbooks[threepairs[1]][1][0][0]).split('.')[1])), len(str(orderbooks[threepairs[1]][1][0][0]).split('.')[1]) + 1)
                    print(f'Orderbooks - {orderbooks}')
                    print(f'Threepairs - {threepairs}')
                    print('second perc', percentage2)
                    print(f'volume - {volume2}')
                    print(f'price - {price}')
                    buy_amount = orderbooks[threepairs[0]][1][1][1]
                    alt_buy_amount = orderbooks[threepairs[0]][1][1][2] / orderbooks[threepairs[2]][0][0][0]
                    if orderbooks[threepairs[0]][1][2][1] < buy_amount:
                        buy_amount = orderbooks[threepairs[0]][1][2][1]
                        alt_buy_amount = orderbooks[threepairs[0]][1][2][2] / orderbooks[threepairs[2]][0][0][0]
                    potential = buy_coin(number, [2, percentage2], threepairs, orderbooks, buy_amount, alt_buy_amount, price, client, 1)
                    coin_file = open(f'coins1.txt', 'r')
                    coin_read = coin_file.read()
                    coin_file.close()
                    if f'{coin_name}-1' in coin_read:
                        coin_read = coin_read.replace(f'{coin_name}-1', f'{coin_name}-0')
                        coin_file = open(f'coins1.txt', 'w')
                        coin_file.write(coin_read)
                        coin_file.close()
                    else:
                        print('Coin not found in file')
                    print('potential -', potential)
                    print(buy_amount)
                    print(alt_buy_amount)
                    # my_file = open(f"data1.txt", "r")
                    # new_read = my_file.read().replace(threepairs[2], '')
                    # my_file.close()
                    # my_file = open(f"data1.txt", "w")
                    # my_file.write(new_read)
                    # my_file.close()
                else:
                    print('Searching for suitable pair')
                    # print(percentage1, percentage2)
                    # print(volume1, volume2)
                    potential = 0
            except Exception as error:
                if 'list index out of range' not in str(error):
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write('\n')
                    stored_data.write(str(error))
                    stored_data.write(str(traceback.format_exc()))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                time.sleep(3)
        attempt += 1
