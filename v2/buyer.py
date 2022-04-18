from kucoin.client import Client
import kucoin
import config
import time
import methods
import json
import sys
import traceback

def buy_coin(number, percentage, threepairs, orderbooks, buy_amount, alt_buy_amount, price, client, name):
    new_client = methods.New_client(client)
    try:
        reserved_balance = 0
        if number == 0 and percentage[0] == 1:
            if price * buy_amount * new_client.get_currencies(threepairs[0].split('-')[1])['rates'][threepairs[0].split('-')[1]]['USD'] < 20.0:
                return 0
            digit_count = len(str(orderbooks[threepairs[0]][0][0][1]).split('.')[1])
            digit_count1 = len(str(orderbooks[threepairs[1]][0][0][1]).split('.')[1])
            digit_count2 = len(str(orderbooks[threepairs[2]][0][0][1]).split('.')[1])
            if digit_count < 2:
                digit_count = 2
            if digit_count1 < 2:
                digit_count1 = 2
            if digit_count2 < 4:
                digit_count2 = 4
            # if threepairs[0].split('-')[1] == 'BTC':
            #     digit_count = 8
            # elif threepairs[0].split('-')[1] == 'ETH':
            #     digit_count = 8
            # elif threepairs[0].split('-')[1] == 'USDT':
            #     digit_count = 6
            # elif threepairs[0].split('-')[1] == 'NEO':
            #     digit_count = 6
            # elif threepairs[0].split('-')[1] == 'KCS':
            #     digit_count = 4
            # if threepairs[1].split('-')[1] == 'BTC':
            #     digit_count1 = 8
            # elif threepairs[1].split('-')[1] == 'ETH':
            #     digit_count1 = 8
            # elif threepairs[1].split('-')[1] == 'USDT':
            #     digit_count1 = 6
            # elif threepairs[1].split('-')[1] == 'NEO':
            #     digit_count1 = 6
            # elif threepairs[1].split('-')[1] == 'KCS':
            #     digit_count1 = 4
            # if threepairs[2].split('-')[1] == 'BTC':
            #     digit_count2 = 8
            # elif threepairs[2].split('-')[1] == 'ETH':
            #     digit_count2 = 8
            # elif threepairs[2].split('-')[1] == 'USDT':
            #     digit_count2 = 6
            # elif threepairs[2].split('-')[1] == 'NEO':
            #     digit_count2 = 6
            # elif threepairs[2].split('-')[1] == 'KCS':
            #     digit_count2 = 4
            print(0, 1)
            start_balance = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
            coin1 = threepairs[0].split('-')[1]
            coin2 = threepairs[1].split('-')[1]
            my_file = open(f'{coin1}{name}.txt', 'r')
            read = my_file.read()
            my_file.close()
            amount = float(read)
            if amount >= 0:
                start_balance -= amount
            print('startbalance -', start_balance)
            print('amount -', amount)
            if start_balance < 0:
                print('Idk what just happened')
                return 0
            if start_balance > alt_buy_amount:
                print('Buying not on full balance')
                balance_before = new_client.get_coin_balance(threepairs[0].split('-')[0])['balance']
                transaction1 = new_client.create_order(threepairs[0], Client.SIDE_BUY, price, buy_amount)
                if transaction1 == None:
                    return 0
                print('First transaction begins')
                time.sleep(10)
                if new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                    c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                else:
                    time.sleep(10)
                    if new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                    else:
                        time.sleep(10)
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                time.sleep(2)
                dealAmount1 = new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                if dealAmount1 == None:
                    print('Deal amount 1 = None!!!')
                    while dealAmount1 == None:
                        dealAmount1 = new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                        print('Still None!!!')
                        time.sleep(2)
                print('Deal amount =', dealAmount1)
                if dealAmount1 != 0:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{percentage}\n')
                    stored_data.write(str(json.dumps(orderbooks)))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                    balance_after = new_client.get_coin_balance(threepairs[0].split('-')[0])['balance']
                    balance2_before = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                    reserved_balance = dealAmount1 * orderbooks[threepairs[1]][1][0][0]
                    my_file = open(f'{coin2}{name}.txt', 'r')
                    read = my_file.read()
                    my_file.close()
                    my_file = open(f'{coin2}{name}.txt', 'w')
                    prev_reserved_bal = read
                    read = str(float(prev_reserved_bal) + reserved_balance)
                    print('read -', read)
                    my_file.write(read)
                    my_file.close()
                    attempt = 1
                    transaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, orderbooks[threepairs[1]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                    while transaction2 == None and attempt < 100:
                        attempt += 1
                        transaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, orderbooks[threepairs[1]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                        time.sleep(1)
                        print('Trying to create order')
                    print('Second transaction begins')
                    time.sleep(5)
                    c = new_client.cancel_order(transaction2, Client.SIDE_SELL, threepairs[1])
                    time.sleep(2)
                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                    if pendingAmount2 == None:
                        print('Pending amount 2 = None!!!')
                        while pendingAmount2 == None:
                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    dealAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                    if dealAmount2 == None:
                        print('Deal amount 2 = None!!!')
                        while dealAmount2 == None:
                            dealAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    balance2_after = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                    if dealAmount2 != 0:
                        koeff = pendingAmount2 / dealAmount2
                    else:
                        koeff = 1
                    if pendingAmount2 == 0 or koeff < 0.01:
                        third_amount_rounded = f"%.{digit_count2}f" % ((dealAmount2 * orderbooks[threepairs[1]][1][0][0] * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_SELL, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_SELL, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin2}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin2}{name}.txt', 'w')
                        new_reserve = float(read) - reserved_balance
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                    else:
                        third_trans_amount = dealAmount2 * orderbooks[threepairs[1]][1][0][0]
                        while pendingAmount2 != 0:
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction began')
                            a = new_client.get_order_book(threepairs[1], limit=1)
                            newtransaction2 = list()
                            if a['BUY'][0][0] / orderbooks[threepairs[1]][1][0][0] / percentage[1] > 1.003:
                                newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                while newtransaction2 == None:
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    time.sleep(1)
                                    print('Trying to create order')
                                time.sleep(5)
                                c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                            else:
                                new_attempt = 1
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt started working\n')
                                stored_data.close()
                                while new_attempt < 100 and pendingAmount2 != 0: #a['SELL'][0][0] - (0.1 ** digit_count2) / orderbooks[threepairs[1]][1][0][0] / percentage[1] > 1.003
                                    a = new_client.get_order_book(threepairs[1], limit=1)
                                    stored_data = open('orderbooks.txt', 'a')
                                    stored_data.write(f"{a['SELL'][0][0]}\n")
                                    stored_data.close()
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    new_attempt += 1
                                    time.sleep(9)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                                    time.sleep(2)
                                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    if pendingAmount2 == None:
                                        print('Pending amount 2 = None!!!')
                                        while pendingAmount2 == None:
                                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                            print('Still None!!!')
                                if pendingAmount2 != 0:
                                    a = new_client.get_order_book(threepairs[1], limit=1)
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    time.sleep(5)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt finished working\n')
                                stored_data.close()
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction finished')
                            stored_data.close()
                            print('Second transaction begins')
                            time.sleep(2)
                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                            if pendingAmount2 == None:
                                print('Pending amount 2 = None!!!')
                                while pendingAmount2 == None:
                                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                            b = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                            if b == None:
                                print('Deal amount 2 = None!!!')
                                while b == None:
                                    b = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                                dealAmount2 += b
                            third_trans_amount += b * a['BUY'][0][0]
                            balance2_after = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                        third_amount_rounded = f"%.{digit_count2}f" % ((third_trans_amount * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_SELL, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_SELL, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin2}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin2}{name}.txt', 'w')
                        new_reserve = float(read) - reserved_balance
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                else:
                    return 1
            elif start_balance < alt_buy_amount and new_client.get_currencies(threepairs[0].split('-')[1])['rates'][threepairs[0].split('-')[1]]['USD'] * start_balance > 20.0:
                print('Buying on full balance')
                digit_count = len(str(orderbooks[threepairs[0]][0][0][1]).split('.')[1])
                digit_count1 = len(str(orderbooks[threepairs[1]][0][0][1]).split('.')[1])
                digit_count2 = len(str(orderbooks[threepairs[2]][0][0][1]).split('.')[1])
                if digit_count < 2:
                    digit_count = 2
                if digit_count1 < 2:
                    digit_count1 = 2
                if digit_count2 < 4:
                    digit_count2 = 4
                balance_before = new_client.get_coin_balance(threepairs[0].split('-')[0])['balance']
                print(float(format(start_balance / price, f'.{digit_count}f')))
                transaction1 = new_client.create_order(threepairs[0], Client.SIDE_BUY, price, round((start_balance / price) - (0.1 ** digit_count), digit_count))
                if transaction1 == None:
                    return 0
                print('First transaction begins')
                time.sleep(10)
                if new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                    c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                else:
                    time.sleep(10)
                    if new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                    else:
                        time.sleep(10)
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                time.sleep(2)
                dealAmount1 = new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                if dealAmount1 == None:
                    print('Deal amount 1 = None!!!')
                    while dealAmount1 == None:
                        dealAmount1 = new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                        print('Still None!!!')
                        time.sleep(2)
                print('Deal amount =', dealAmount1)
                if dealAmount1 != 0:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{percentage}\n')
                    stored_data.write(str(json.dumps(orderbooks)))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                    balance_after = new_client.get_coin_balance(threepairs[0].split('-')[0])['balance']
                    balance2_before = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                    reserved_balance = dealAmount1 * orderbooks[threepairs[1]][1][0][0]
                    my_file = open(f'{coin2}{name}.txt', 'r')
                    read = my_file.read()
                    my_file.close()
                    my_file = open(f'{coin2}{name}.txt', 'w')
                    prev_reserved_bal = read
                    read = str(float(prev_reserved_bal) + reserved_balance)
                    print('read -', read)
                    my_file.write(read)
                    my_file.close()
                    attempt = 1
                    transaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, orderbooks[threepairs[1]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                    while transaction2 == None and attempt < 100:
                        attempt += 1
                        transaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, orderbooks[threepairs[1]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                        time.sleep(1)
                        print('Trying to create order')
                    print('Second transaction begins')
                    time.sleep(5)
                    c = new_client.cancel_order(transaction2, Client.SIDE_SELL, threepairs[1])
                    time.sleep(2)
                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                    if pendingAmount2 == None:
                        print('Pending amount 2 = None!!!')
                        while pendingAmount2 == None:
                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    dealAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                    if dealAmount2 == None:
                        print('Deal amount 2 = None!!!')
                        while dealAmount2 == None:
                            dealAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    balance2_after = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                    if dealAmount2 != 0:
                        koeff = pendingAmount2 / dealAmount2
                    else:
                        koeff = 1
                    if pendingAmount2 == 0 or koeff < 0.1:
                        third_amount_rounded = f"%.{digit_count2}f" % ((dealAmount2 * orderbooks[threepairs[1]][1][0][0] * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_SELL, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_SELL, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin2}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin2}{name}.txt', 'w')
                        new_reserve = float(read) - reserved_balance
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                    else:
                        third_trans_amount = dealAmount2 * orderbooks[threepairs[1]][1][0][0]
                        while pendingAmount2 != 0:
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction began')
                            a = new_client.get_order_book(threepairs[1], limit=1)
                            newtransaction2 = list()
                            if a['BUY'][0][0] / orderbooks[threepairs[1]][1][0][0] / percentage[1] > 1.003:
                                newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                while newtransaction2 == None:
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    time.sleep(1)
                                    print('Trying to create order')
                                time.sleep(5)
                                c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                            else:
                                new_attempt = 1
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt started working\n')
                                stored_data.close()
                                while new_attempt < 100 and pendingAmount2 != 0: #a['SELL'][0][0] - (0.1 ** digit_count2) / orderbooks[threepairs[1]][1][0][0] / percentage[1] > 1.003
                                    a = new_client.get_order_book(threepairs[1], limit=1)
                                    stored_data = open('orderbooks.txt', 'a')
                                    stored_data.write(f"{a['SELL'][0][0]}\n")
                                    stored_data.close()
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    new_attempt += 1
                                    time.sleep(9)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                                    time.sleep(2)
                                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    if pendingAmount2 == None:
                                        print('Pending amount 2 = None!!!')
                                        while pendingAmount2 == None:
                                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                            print('Still None!!!')
                                if pendingAmount2 != 0:
                                    a = new_client.get_order_book(threepairs[1], limit=1)
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    time.sleep(5)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt finished working\n')
                                stored_data.close()
                            # attempt = 1
                            # newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            # while newtransaction2 == None and attempt < 100:
                            #     newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            #     attempt += 1
                            #     time.sleep(1)
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction finished')
                            stored_data.close()
                            print('Second transaction begins')
                            time.sleep(2)
                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                            if pendingAmount2 == None:
                                print('Pending amount 2 = None!!!')
                                while pendingAmount2 == None:
                                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                            b = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                            if b == None:
                                print('Deal amount 2 = None!!!')
                                while b == None:
                                    b = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                                dealAmount2 += b
                            third_trans_amount += b * a['BUY'][0][0]
                            balance2_after = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                        third_amount_rounded = f"%.{digit_count2}f" % ((third_trans_amount * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_SELL, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_SELL, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin2}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin2}{name}.txt', 'w')
                        new_reserve = float(read) - reserved_balance
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                else:
                    return 1
            else:
                print('Not enough money')
        elif number == 0 and percentage[0] == 2:
            if price * buy_amount * new_client.get_currencies(threepairs[1].split('-')[1])['rates'][threepairs[1].split('-')[1]]['USD'] < 20.0:
                return 0
            digit_count = len(str(orderbooks[threepairs[0]][0][0][1]).split('.')[1])
            digit_count2 = len(str(orderbooks[threepairs[2]][0][0][1]).split('.')[1])
            if digit_count < 2:
                digit_count = 2
            if digit_count2 < 4:
                digit_count2 = 4
            print(0, 2)
            start_balance = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
            coin1 = threepairs[0].split('-')[1]
            coin2 = threepairs[1].split('-')[1]
            my_file = open(f'{coin2}{name}.txt', 'r')
            read = my_file.read()
            my_file.close()
            amount = float(read)
            if amount >= 0:
                start_balance -= amount
            print('startbalance -', start_balance)
            print('amount -', amount)
            if start_balance < 0:
                print('Idk what just happened')
                return 0
            if start_balance > alt_buy_amount:
                print('Buying not on full balance')
                balance_before = new_client.get_coin_balance(threepairs[1].split('-')[0])['balance']
                balance2_before = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                transaction1 = new_client.create_order(threepairs[1], Client.SIDE_BUY, price, buy_amount)
                if transaction1 == None:
                    return 0
                print('First transaction begins')
                time.sleep(10)
                if new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                    c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                else:
                    time.sleep(10)
                    if new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                    else:
                        time.sleep(10)
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                time.sleep(2)
                dealAmount1 = new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                if dealAmount1 == None:
                    print('Deal amount 1 = None!!!')
                    while dealAmount1 == None:
                        dealAmount1 = new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                        print('Still None!!!')
                        time.sleep(2)
                print('Deal amount =', dealAmount1)
                if dealAmount1 != 0:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{percentage}\n')
                    stored_data.write(str(json.dumps(orderbooks)))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                    reserved_balance = dealAmount1 * orderbooks[threepairs[0]][1][0][0]
                    balance_after = new_client.get_coin_balance(threepairs[1].split('-')[0])['balance']
                    balance2_after = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                    my_file = open(f'{coin1}{name}.txt', 'r')
                    read = my_file.read()
                    my_file.close()
                    my_file = open(f'{coin1}{name}.txt', 'w')
                    prev_reserved_bal = read
                    read = str(float(prev_reserved_bal) + reserved_balance)
                    print('read -', read)
                    my_file.write(read)
                    my_file.close()
                    attempt = 1
                    transaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, orderbooks[threepairs[0]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count), digit_count))
                    while transaction2 == None and attempt < 100:
                        attempt += 1
                        transaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, orderbooks[threepairs[0]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count), digit_count))
                        time.sleep(1)
                        print('Trying to create order')
                    print('Second transaction begins')
                    time.sleep(5)
                    c = new_client.cancel_order(transaction2, Client.SIDE_SELL, threepairs[0])
                    time.sleep(2)
                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                    if pendingAmount2 == None:
                        print('Pending amount 2 = None!!!')
                        while pendingAmount2 == None:
                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    dealAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                    if dealAmount2 == None:
                        print('Deal amount 2 = None!!!')
                        while dealAmount2 == None:
                            dealAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    if dealAmount2 != 0:
                        koeff = pendingAmount2 / dealAmount2
                    else:
                        koeff = 1
                    if pendingAmount2 == 0 or koeff < 0.1:
                        third_amount_rounded = f"%.{digit_count2}f" % ((dealAmount2 * orderbooks[threepairs[1]][1][0][0] * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0],float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0],float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_BUY, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_BUY, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin1}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin1}{name}.txt', 'w')
                        new_reserve = float(read) - float(float(prev_reserved_bal) + reserved_balance)
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                    else:
                        third_trans_amount = dealAmount2 * orderbooks[threepairs[0]][1][0][0] / orderbooks[threepairs[2]][0][0][0]
                        while pendingAmount2 != 0:
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction began')
                            a = new_client.get_order_book(threepairs[0], limit=1)
                            newtransaction2 = list()
                            if a['BUY'][0][0] / orderbooks[threepairs[0]][1][0][0] / percentage[1] > 1.003:
                                newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                while newtransaction2 == None:
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    time.sleep(1)
                                    print('Trying to create order')
                                time.sleep(5)
                                c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                            else:
                                new_attempt = 1
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt started working\n')
                                stored_data.close()
                                while new_attempt < 100 and pendingAmount2 != 0: #a['SELL'][0][0] - (0.1 ** digit_count2) / orderbooks[threepairs[0]][1][0][0] / percentage[1] > 1.003
                                    a = new_client.get_order_book(threepairs[0], limit=1)
                                    stored_data = open('orderbooks.txt', 'a')
                                    stored_data.write(f"{a['SELL'][0][0]}\n")
                                    stored_data.close()
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    new_attempt += 1
                                    time.sleep(9)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                                    time.sleep(2)
                                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    if pendingAmount2 == None:
                                        print('Pending amount 2 = None!!!')
                                        while pendingAmount2 == None:
                                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                            print('Still None!!!')
                                if pendingAmount2 != 0:
                                    a = new_client.get_order_book(threepairs[0], limit=1)
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    time.sleep(5)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt finished working\n')
                                stored_data.close()
                            # attempt = 1
                            # newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            # while newtransaction2 == None and attempt < 100:
                            #     attempt += 1
                            #     newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            #     time.sleep(1)
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction finished')
                            stored_data.close()
                            print('Second transaction begins')
                            time.sleep(2)
                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                            if pendingAmount2 == None:
                                print('Pending amount 2 = None!!!')
                                while pendingAmount2 == None:
                                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                            b = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                            if b == None:
                                print('Deal amount 2 = None!!!')
                                while b == None:
                                    b = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                                dealAmount2 += b
                            third_trans_amount += b * a['BUY'][0][0] / orderbooks[threepairs[2]][0][0][0]
                            balance2_after = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
                        third_amount_rounded = f"%.{digit_count2}f" % ((third_trans_amount * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_BUY, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_BUY, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin1}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin1}{name}.txt', 'w')
                        new_reserve = float(read) - float(float(prev_reserved_bal) + reserved_balance)
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                else:
                    return 1
            elif start_balance < alt_buy_amount and new_client.get_currencies(threepairs[1].split('-')[1])['rates'][threepairs[1].split('-')[1]]['USD'] * start_balance > 20.0:
                print('Buying on full balance')
                digit_count = len(str(orderbooks[threepairs[1]][0][0][1]).split('.')[1])
                digit_count1 = len(str(orderbooks[threepairs[0]][0][0][1]).split('.')[1])
                digit_count2 = len(str(orderbooks[threepairs[2]][0][0][1]).split('.')[1])
                if digit_count < 2:
                    digit_count = 2
                if digit_count1 < 2:
                    digit_count1 = 2
                if digit_count2 < 4:
                    digit_count2 = 4
                balance_before = new_client.get_coin_balance(threepairs[1].split('-')[0])['balance']
                print(float(format(start_balance / price, f'.{digit_count}f')))
                balance2_before = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                transaction1 = new_client.create_order(threepairs[1], Client.SIDE_BUY, price, round((start_balance / price) - (0.1 ** digit_count), digit_count))
                if transaction1 == None:
                    return 0
                print('First transaction begins')
                time.sleep(10)
                if new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                    c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                else:
                    time.sleep(10)
                    if new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                    else:
                        time.sleep(10)
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                time.sleep(2)
                dealAmount1 = new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                if dealAmount1 == None:
                    print('Deal amount 1 = None!!!')
                    while dealAmount1 == None:
                        dealAmount1 = new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                        print('Still None!!!')
                        time.sleep(2)
                print('Deal amount =', dealAmount1)
                if dealAmount1 != 0:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{percentage}\n')
                    stored_data.write(str(json.dumps(orderbooks)))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                    balance_after = new_client.get_coin_balance(threepairs[1].split('-')[0])['balance']
                    balance2_after = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                    reserved_balance = dealAmount1 * orderbooks[threepairs[0]][1][0][0]
                    my_file = open(f'{coin1}{name}.txt', 'r')
                    read = my_file.read()
                    my_file.close()
                    my_file = open(f'{coin1}{name}.txt', 'w')
                    prev_reserved_bal = read
                    read = str(float(prev_reserved_bal) + reserved_balance)
                    print('read -', read)
                    my_file.write(read)
                    my_file.close()
                    attempt = 1
                    transaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, orderbooks[threepairs[0]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                    while transaction2 == None and attempt < 100:
                        attempt += 1
                        transaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, orderbooks[threepairs[0]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                        time.sleep(1)
                        print('Trying to create order')
                    print('Second transaction begins')
                    time.sleep(5)
                    c = new_client.cancel_order(transaction2, Client.SIDE_SELL, threepairs[0])
                    time.sleep(2)
                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                    if pendingAmount2 == None:
                        print('Pending amount 2 = None!!!')
                        while pendingAmount2 == None:
                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    dealAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                    if dealAmount2 == None:
                        print('Deal amount 2 = None!!!')
                        while dealAmount2 == None:
                            dealAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    if dealAmount2 != 0:
                        koeff = pendingAmount2 / dealAmount2
                    else:
                        koeff = 1
                    if pendingAmount2 == 0 or koeff < 0.1:
                        third_amount_rounded = f"%.{digit_count2}f" % ((dealAmount2 * orderbooks[threepairs[1]][1][0][0] * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction begins')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_BUY, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_BUY, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin1}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin1}{name}.txt', 'w')
                        new_reserve = float(read) - float(float(prev_reserved_bal) + reserved_balance)
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                    else:
                        third_trans_amount = dealAmount2 * orderbooks[threepairs[0]][1][0][0] / orderbooks[threepairs[2]][0][0][0]
                        while pendingAmount2 != 0:
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction began')
                            a = new_client.get_order_book(threepairs[0], limit=1)
                            newtransaction2 = list()
                            if a['BUY'][0][0] / orderbooks[threepairs[0]][1][0][0] / percentage[1] > 1.003:
                                newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                while newtransaction2 == None:
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    time.sleep(1)
                                    print('Trying to create order')
                                time.sleep(5)
                                c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                            else:
                                new_attempt = 1
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt started working\n')
                                stored_data.close()
                                while new_attempt < 100 and pendingAmount2 != 0: #a['SELL'][0][0] - (0.1 ** digit_count2) / orderbooks[threepairs[0]][1][0][0] / percentage[1] > 1.003
                                    a = new_client.get_order_book(threepairs[0], limit=1)
                                    stored_data = open('orderbooks.txt', 'a')
                                    stored_data.write(f"{a['SELL'][0][0]}\n")
                                    stored_data.close()
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    new_attempt += 1
                                    time.sleep(9)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                                    time.sleep(2)
                                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    if pendingAmount2 == None:
                                        print('Pending amount 2 = None!!!')
                                        while pendingAmount2 == None:
                                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                            print('Still None!!!')
                                if pendingAmount2 != 0:
                                    a = new_client.get_order_book(threepairs[0], limit=1)
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    time.sleep(5)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt finished working\n')
                                stored_data.close()
                            # attempt = 1
                            # newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            # while newtransaction2 == None and attempt < 100:
                            #     attempt += 1
                            #     newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            #     time.sleep(1)
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction finished')
                            stored_data.close()
                            print('Second transaction begins')
                            time.sleep(2)
                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                            if pendingAmount2 == None:
                                print('Pending amount 2 = None!!!')
                                while pendingAmount2 == None:
                                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                            b = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                            if b == None:
                                print('Deal amount 2 = None!!!')
                                while b == None:
                                    b = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                                dealAmount2 += b
                            third_trans_amount += b * a['BUY'][0][0] / orderbooks[threepairs[2]][0][0][0]
                            balance2_after = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
                        third_amount_rounded = f"%.{digit_count2}f" % ((third_trans_amount * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        # while transaction3 == None:
                        #     transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                        print('Third transaction begins')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_BUY, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_BUY, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin1}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin1}{name}.txt', 'w')
                        new_reserve = float(read) - float(float(prev_reserved_bal) + reserved_balance)
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                else:
                    return 1
            else:
                print('Not enough money')
        elif number == 1 and percentage[0] == 1:
            if price * buy_amount * new_client.get_currencies(threepairs[0].split('-')[1])['rates'][threepairs[0].split('-')[1]]['USD'] < 20.0:
                return 0
            digit_count1 = len(str(orderbooks[threepairs[1]][0][0][1]).split('.')[1])
            digit_count2 = len(str(orderbooks[threepairs[2]][0][0][1]).split('.')[1])
            if digit_count1 < 2:
                digit_count1 = 2
            if digit_count2 < 4:
                digit_count2 = 4
            print(1, 1)
            start_balance = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
            coin1 = threepairs[0].split('-')[1]
            coin2 = threepairs[1].split('-')[1]
            my_file = open(f'{coin1}{name}.txt', 'r')
            read = my_file.read()
            my_file.close()
            amount = float(read)
            if amount >= 0:
                start_balance -= amount
            print('startbalance -', start_balance)
            print('amount -', amount)
            if start_balance < 0:
                print('Idk what just happened')
                return 0
            if start_balance > alt_buy_amount:
                print('Buying not on full balance')
                transaction1 = new_client.create_order(threepairs[0], Client.SIDE_BUY, price, buy_amount)
                if transaction1 == None:
                    return 0
                print('First transaction begins')
                time.sleep(10)
                if new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                    c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                else:
                    time.sleep(10)
                    if new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                    else:
                        time.sleep(10)
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                time.sleep(2)
                dealAmount1 = new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                if dealAmount1 == None:
                    print('Deal amount 1 = None!!!')
                    while dealAmount1 == None:
                        dealAmount1 = new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                        print('Still None!!!')
                        time.sleep(2)
                print('Deal amount =', dealAmount1)
                if dealAmount1 != 0:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{percentage}\n')
                    stored_data.write(str(json.dumps(orderbooks)))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                    balance_after = new_client.get_coin_balance(threepairs[0].split('-')[0])['balance']
                    balance2_before = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
                    reserved_balance = dealAmount1 * orderbooks[threepairs[1]][1][0][0]
                    my_file = open(f'{coin2}{name}.txt', 'r')
                    read = my_file.read()
                    my_file.close()
                    my_file = open(f'{coin2}{name}.txt', 'w')
                    prev_reserved_bal = read
                    read = str(float(prev_reserved_bal) + reserved_balance)
                    print('read -', read)
                    my_file.write(read)
                    my_file.close()
                    attempt = 1
                    transaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, orderbooks[threepairs[1]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                    while transaction2 == None:
                        transaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, orderbooks[threepairs[1]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                        time.sleep(1)
                        print('Trying to create order')
                    print('Second transaction begins')
                    time.sleep(5)
                    c = new_client.cancel_order(transaction2, Client.SIDE_SELL, threepairs[1])
                    time.sleep(2)
                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                    if pendingAmount2 == None:
                        print('Pending amount 2 = None!!!')
                        while pendingAmount2 == None:
                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    dealAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                    if dealAmount2 == None:
                        print('Deal amount 2 = None!!!')
                        while dealAmount2 == None:
                            dealAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    balance2_after = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
                    if dealAmount2 != 0:
                        koeff = pendingAmount2 / dealAmount2
                    else:
                        koeff = 1
                    if pendingAmount2 == 0 or koeff < 0.01:
                        third_amount_rounded = f"%.{digit_count2}f" % ((dealAmount2 * orderbooks[threepairs[1]][1][0][0] / orderbooks[threepairs[2]][0][0][0] * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_BUY, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_BUY, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin2}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin2}{name}.txt', 'w')
                        new_reserve = float(read) - reserved_balance
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                    else:
                        third_trans_amount = dealAmount2 * orderbooks[threepairs[1]][1][0][0] / orderbooks[threepairs[2]][0][0][0]
                        while pendingAmount2 != 0:
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction began')
                            a = new_client.get_order_book(threepairs[1], limit=1)
                            newtransaction2 = list()
                            if a['BUY'][0][0] / orderbooks[threepairs[1]][1][0][0] / percentage[1] > 1.003:
                                newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                while newtransaction2 == None:
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    time.sleep(1)
                                    print('Trying to create order')
                                time.sleep(5)
                                c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                            else:
                                new_attempt = 1
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt started working\n')
                                stored_data.close()
                                while new_attempt < 100 and pendingAmount2 != 0: #a['SELL'][0][0] - (0.1 ** digit_count2) / orderbooks[threepairs[1]][1][0][0] / percentage[1] > 1.003
                                    a = new_client.get_order_book(threepairs[1], limit=1)
                                    stored_data = open('orderbooks.txt', 'a')
                                    stored_data.write(f"{a['SELL'][0][0]}\n")
                                    stored_data.close()
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    new_attempt += 1
                                    time.sleep(9)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                                    time.sleep(2)
                                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    if pendingAmount2 == None:
                                        print('Pending amount 2 = None!!!')
                                        while pendingAmount2 == None:
                                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                            print('Still None!!!')
                                if pendingAmount2 != 0:
                                    a = new_client.get_order_book(threepairs[1], limit=1)
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    time.sleep(5)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt finished working\n')
                                stored_data.close()
                            # attempt = 1
                            # newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            # while newtransaction2 == None and attempt < 100:
                            #     attempt += 1
                            #     newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            #     time.sleep(1)
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction finished')
                            stored_data.close()
                            print('Second transaction begins')
                            time.sleep(2)
                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                            if pendingAmount2 == None:
                                print('Pending amount 2 = None!!!')
                                while pendingAmount2 == None:
                                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                            b = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                            if b == None:
                                print('Deal amount 2 = None!!!')
                                while b == None:
                                    b = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                                dealAmount2 += b
                            third_trans_amount += b * a['BUY'][0][0] / orderbooks[threepairs[2]][0][0][0]
                            balance2_after = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
                        third_amount_rounded = f"%.{digit_count2}f" % ((third_trans_amount * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_BUY, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_BUY, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin2}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin2}{name}.txt', 'w')
                        new_reserve = float(read) - reserved_balance
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                else:
                    return 1
            elif start_balance < alt_buy_amount and new_client.get_currencies(threepairs[0].split('-')[1])['rates'][threepairs[0].split('-')[1]]['USD'] * start_balance > 20.0:
                print('Buying on full balance')
                digit_count = len(str(orderbooks[threepairs[0]][0][0][1]).split('.')[1])
                digit_count1 = len(str(orderbooks[threepairs[1]][0][0][1]).split('.')[1])
                digit_count2 = len(str(orderbooks[threepairs[2]][0][0][1]).split('.')[1])
                if digit_count < 2:
                    digit_count = 2
                if digit_count1 < 2:
                    digit_count1 = 2
                if digit_count2 < 4:
                    digit_count2 = 4
                print(float(format(start_balance / price, f'.{digit_count}f')))
                transaction1 = new_client.create_order(threepairs[0], Client.SIDE_BUY, price, round((start_balance / price) - (0.1 ** digit_count), digit_count))
                if transaction1 == None:
                    return 0
                print('First transaction begins')
                time.sleep(10)
                if new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                    c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                else:
                    time.sleep(10)
                    if new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                    else:
                        time.sleep(10)
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[0])
                time.sleep(2)
                dealAmount1 = new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                if dealAmount1 == None:
                    print('Deal amount 1 = None!!!')
                    while dealAmount1 == None:
                        dealAmount1 = new_client.get_order_details(threepairs[0], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                        print('Still None!!!')
                        time.sleep(2)
                print('Deal amount =', dealAmount1)
                if dealAmount1 != 0:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{percentage}\n')
                    stored_data.write(str(json.dumps(orderbooks)))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                    balance_after = new_client.get_coin_balance(threepairs[0].split('-')[0])['balance']
                    balance2_before = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                    reserved_balance = dealAmount1 * orderbooks[threepairs[1]][1][0][0]
                    my_file = open(f'{coin2}{name}.txt', 'r')
                    read = my_file.read()
                    my_file.close()
                    my_file = open(f'{coin2}{name}.txt', 'w')
                    prev_reserved_bal = read
                    read = str(float(prev_reserved_bal) + reserved_balance)
                    print('read -', read)
                    my_file.write(read)
                    my_file.close()
                    attempt = 1
                    transaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, orderbooks[threepairs[1]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                    while transaction2 == None:
                        transaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, orderbooks[threepairs[1]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                        time.sleep(1)
                        print('Trying to create order')
                    print('Second transaction begins')
                    time.sleep(5)
                    c = new_client.cancel_order(transaction2, Client.SIDE_SELL, threepairs[1])
                    time.sleep(2)
                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                    if pendingAmount2 == None:
                        print('Pending amount 2 = None!!!')
                        while pendingAmount2 == None:
                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    dealAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                    if dealAmount2 == None:
                        print('Deal amount 2 = None!!!')
                        while dealAmount2 == None:
                            dealAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    balance2_after = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                    if dealAmount2 != 0:
                        koeff = pendingAmount2 / dealAmount2
                    else:
                        koeff = 1
                    if pendingAmount2 == 0 or koeff < 0.1:
                        third_amount_rounded = f"%.{digit_count2}f" % ((dealAmount2 * orderbooks[threepairs[1]][1][0][0] / orderbooks[threepairs[2]][0][0][0] * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_BUY, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_BUY, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin2}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin2}{name}.txt', 'w')
                        new_reserve = float(read) - reserved_balance
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                    else:
                        third_trans_amount = dealAmount2 * orderbooks[threepairs[1]][1][0][0] / orderbooks[threepairs[2]][0][0][0]
                        while pendingAmount2 != 0:
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction began')
                            a = new_client.get_order_book(threepairs[1], limit=1)
                            newtransaction2 = list()
                            if a['BUY'][0][0] / orderbooks[threepairs[1]][1][0][0] / percentage[1] > 1.003:
                                newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                while newtransaction2 == None:
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    time.sleep(1)
                                    print('Trying to create order')
                                time.sleep(5)
                                c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                            else:
                                new_attempt = 1
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt started working\n')
                                stored_data.close()
                                while new_attempt < 100 and pendingAmount2 != 0: #a['SELL'][0][0] - (0.1 ** digit_count2) / orderbooks[threepairs[1]][1][0][0] / percentage[1] > 1.003
                                    a = new_client.get_order_book(threepairs[1], limit=1)
                                    stored_data = open('orderbooks.txt', 'a')
                                    stored_data.write(f"{a['SELL'][0][0]}\n")
                                    stored_data.close()
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    new_attempt += 1
                                    time.sleep(9)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                                    time.sleep(2)
                                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    if pendingAmount2 == None:
                                        print('Pending amount 2 = None!!!')
                                        while pendingAmount2 == None:
                                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                            print('Still None!!!')
                                if pendingAmount2 != 0:
                                    a = new_client.get_order_book(threepairs[1], limit=1)
                                    newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    time.sleep(5)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[1])
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt finished working\n')
                                stored_data.close()
                            # attempt = 1
                            # newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            # while newtransaction2 == None and attempt < 100:
                            #     attempt += 1
                            #     newtransaction2 = new_client.create_order(threepairs[1], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            #     time.sleep(1)
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction finished')
                            stored_data.close()
                            print('Second transaction begins')
                            time.sleep(2)
                            pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                            if pendingAmount2 == None:
                                print('Pending amount 2 = None!!!')
                                while pendingAmount2 == None:
                                    pendingAmount2 = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                            b = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                            if b == None:
                                print('Deal amount 2 = None!!!')
                                while b == None:
                                    b = new_client.get_order_details(threepairs[1], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                                dealAmount2 += b
                            third_trans_amount += b * a['BUY'][0][0] / orderbooks[threepairs[2]][0][0][0]
                            balance2_after = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
                        third_amount_rounded = f"%.{digit_count2}f" % ((third_trans_amount * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_BUY, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_BUY, a['SELL'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_BUY, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_BUY, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin2}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin2}{name}.txt', 'w')
                        new_reserve = float(read) - reserved_balance
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                else:
                    return 1
            else:
                print('Not enough money')
        elif number == 1 and percentage[0] == 2:
            if price * buy_amount * new_client.get_currencies(threepairs[1].split('-')[1])['rates'][threepairs[1].split('-')[1]]['USD'] < 20.0:
                return 0
            digit_count = len(str(orderbooks[threepairs[0]][0][0][1]).split('.')[1])
            digit_count2 = len(str(orderbooks[threepairs[2]][0][0][1]).split('.')[1])
            if digit_count < 2:
                digit_count = 2
            if digit_count2 < 4:
                digit_count2 = 4
            print(1, 2)
            start_balance = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
            coin1 = threepairs[0].split('-')[1]
            coin2 = threepairs[1].split('-')[1]
            my_file = open(f'{coin2}{name}.txt', 'r')
            read = my_file.read()
            my_file.close()
            amount = float(read)
            if amount >= 0:
                start_balance -= amount
            print('startbalance -', start_balance)
            print('amount -', amount)
            if start_balance < 0:
                print('Idk what just happened')
                return 0
            if start_balance > alt_buy_amount:
                print('Buying not on full balance')
                transaction1 = new_client.create_order(threepairs[1], Client.SIDE_BUY, price, buy_amount)
                if transaction1 == None:
                    return 0
                print('First transaction begins')
                time.sleep(10)
                if new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                    c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                else:
                    time.sleep(10)
                    if new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                    else:
                        time.sleep(10)
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                time.sleep(2)
                dealAmount1 = new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                if dealAmount1 == None:
                    print('Deal amount 1 = None!!!')
                    while dealAmount1 == None:
                        dealAmount1 = new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                        print('Still None!!!')
                        time.sleep(2)
                print('Deal amount =', dealAmount1)
                if dealAmount1 != 0:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{percentage}\n')
                    stored_data.write(str(json.dumps(orderbooks)))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                    reserved_balance = dealAmount1 * orderbooks[threepairs[0]][1][0][0]
                    my_file = open(f'{coin1}{name}.txt', 'r')
                    read = my_file.read()
                    my_file.close()
                    my_file = open(f'{coin1}{name}.txt', 'w')
                    prev_reserved_bal = read
                    read = str(float(prev_reserved_bal) + reserved_balance)
                    print('read -', read)
                    my_file.write(read)
                    my_file.close()
                    attempt = 1
                    transaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, orderbooks[threepairs[0]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count), digit_count))
                    while transaction2 == None:
                        transaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, orderbooks[threepairs[0]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count), digit_count))
                        time.sleep(1)
                        print('Trying to create order')
                    print('Second transaction begins')
                    time.sleep(5)
                    c = new_client.cancel_order(transaction2, Client.SIDE_SELL, threepairs[0])
                    time.sleep(2)
                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                    if pendingAmount2 == None:
                        print('Pending amount 2 = None!!!')
                        while pendingAmount2 == None:
                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    dealAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                    if dealAmount2 == None:
                        print('Deal amount 2 = None!!!')
                        while dealAmount2 == None:
                            dealAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    if dealAmount2 != 0:
                        koeff = pendingAmount2 / dealAmount2
                    else:
                        koeff = 1
                    if pendingAmount2 == 0 or koeff < 0.1:
                        third_amount_rounded = f"%.{digit_count2}f" % ((dealAmount2 * orderbooks[threepairs[1]][1][0][0] / orderbooks[threepairs[2]][0][0][0] * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_SELL, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_SELL, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin1}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin1}{name}.txt', 'w')
                        new_reserve = float(read) - float(float(prev_reserved_bal) + reserved_balance)
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                    else:
                        third_trans_amount = dealAmount2 * orderbooks[threepairs[0]][1][0][0]
                        while pendingAmount2 != 0:
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction began')
                            a = new_client.get_order_book(threepairs[0], limit=1)
                            newtransaction2 = list()
                            if a['BUY'][0][0] / orderbooks[threepairs[0]][1][0][0] / percentage[1] > 1.003:
                                newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                while newtransaction2 == None:
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    time.sleep(1)
                                    print('Trying to create order')
                                time.sleep(5)
                                c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                            else:
                                new_attempt = 1
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt started working\n')
                                stored_data.close()
                                while new_attempt < 100 and pendingAmount2 != 0: #a['SELL'][0][0] - (0.1 ** digit_count2) / orderbooks[threepairs[0]][1][0][0] / percentage[1] > 1.003
                                    a = new_client.get_order_book(threepairs[0], limit=1)
                                    stored_data = open('orderbooks.txt', 'a')
                                    stored_data.write(f"{a['SELL'][0][0]}\n")
                                    stored_data.close()
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    new_attempt += 1
                                    time.sleep(9)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                                    time.sleep(2)
                                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    if pendingAmount2 == None:
                                        print('Pending amount 2 = None!!!')
                                        while pendingAmount2 == None:
                                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                            print('Still None!!!')
                                if pendingAmount2 != 0:
                                    a = new_client.get_order_book(threepairs[0], limit=1)
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    time.sleep(5)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt finished working\n')
                                stored_data.close()
                            # attempt = 1
                            # newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            # while newtransaction2 == None and attempt < 100:
                            #     attempt += 1
                            #     newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            #     time.sleep(1)
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction finished')
                            stored_data.close()
                            print('Second transaction begins')
                            time.sleep(2)
                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                            if pendingAmount2 == None:
                                print('Pending amount 2 = None!!!')
                                while pendingAmount2 == None:
                                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                            b = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                            if b == None:
                                print('Deal amount 2 = None!!!')
                                while b == None:
                                    b = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                                dealAmount2 += b
                            third_trans_amount += b * a['BUY'][0][0]
                            balance2_after = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
                        third_amount_rounded = f"%.{digit_count2}f" % ((third_trans_amount * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_SELL, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_SELL, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin1}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin1}{name}.txt', 'w')
                        new_reserve = float(read) - float(float(prev_reserved_bal) + reserved_balance)
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                else:
                    return 1
            elif start_balance < alt_buy_amount and new_client.get_currencies(threepairs[1].split('-')[1])['rates'][threepairs[1].split('-')[1]]['USD'] * start_balance > 20.0:
                print('Buying on full balance')
                digit_count = len(str(orderbooks[threepairs[1]][0][0][1]).split('.')[1])
                digit_count1 = len(str(orderbooks[threepairs[0]][0][0][1]).split('.')[1])
                digit_count2 = len(str(orderbooks[threepairs[2]][0][0][1]).split('.')[1])
                if digit_count < 2:
                    digit_count = 2
                if digit_count1 < 2:
                    digit_count1 = 2
                if digit_count2 < 4:
                    digit_count2 = 4
                print(float(format(start_balance / price, f'.{digit_count}f')))
                transaction1 = new_client.create_order(threepairs[1], Client.SIDE_BUY, price, round((start_balance / price) - (0.1 ** digit_count), digit_count))
                if transaction1 == None:
                    return 0
                print('First transaction begins')
                time.sleep(10)
                if new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                    c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                else:
                    time.sleep(10)
                    if new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount'] != 0:
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                    else:
                        time.sleep(10)
                        c = new_client.cancel_order(transaction1, Client.SIDE_BUY, threepairs[1])
                time.sleep(2)
                dealAmount1 = new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                if dealAmount1 == None:
                    print('Deal amount 1 = None!!!')
                    while dealAmount1 == None:
                        dealAmount1 = new_client.get_order_details(threepairs[1], Client.SIDE_BUY, order_id=transaction1, limit=10, page=1)['dealAmount']
                        print('Still None!!!')
                        time.sleep(2)
                print('Deal amount =', dealAmount1)
                if dealAmount1 != 0:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{percentage}\n')
                    stored_data.write(str(json.dumps(orderbooks)))
                    stored_data.write(str(time.ctime(time.time())))
                    stored_data.close()
                    balance_after = new_client.get_coin_balance(threepairs[1].split('-')[0])['balance']
                    balance2_after = new_client.get_coin_balance(threepairs[1].split('-')[1])['balance']
                    reserved_balance = dealAmount1 * orderbooks[threepairs[0]][1][0][0]
                    my_file = open(f'{coin1}{name}.txt', 'r')
                    read = my_file.read()
                    my_file.close()
                    my_file = open(f'{coin1}{name}.txt', 'w')
                    prev_reserved_bal = read
                    read = str(float(prev_reserved_bal) + reserved_balance)
                    print('read -', read)
                    my_file.write(read)
                    my_file.close()
                    attempt = 1
                    transaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, orderbooks[threepairs[0]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                    while transaction2 == None:
                        transaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, orderbooks[threepairs[0]][1][0][0], round((dealAmount1 * 0.999) - (0.1 ** digit_count1), digit_count1))
                        time.sleep(1)
                        print('Trying to create order')
                    print('Second transaction begins')
                    time.sleep(5)
                    c = new_client.cancel_order(transaction2, Client.SIDE_SELL, threepairs[0])
                    time.sleep(2)
                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                    if pendingAmount2 == None:
                        print('Pending amount 2 = None!!!')
                        while pendingAmount2 == None:
                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['pendingAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    dealAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                    if dealAmount2 == None:
                        print('Deal amount 2 = None!!!')
                        while dealAmount2 == None:
                            dealAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=transaction2, limit=10, page=1)['dealAmount']
                            print('Still None!!!')
                            time.sleep(2)
                    if dealAmount2 != 0:
                        koeff = pendingAmount2 / dealAmount2
                    else:
                        koeff = 1
                    if pendingAmount2 == 0 or koeff < 0.1:
                        third_amount_rounded = f"%.{digit_count2}f" % ((dealAmount2 * orderbooks[threepairs[1]][1][0][0] / orderbooks[threepairs[2]][0][0][0] * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][0][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction begins')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_SELL, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_SELL, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin1}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin1}{name}.txt', 'w')
                        new_reserve = float(read) - float(float(prev_reserved_bal) + reserved_balance)
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                    else:
                        third_trans_amount = dealAmount2 * orderbooks[threepairs[0]][1][0][0]
                        while pendingAmount2 != 0:
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction began')
                            a = new_client.get_order_book(threepairs[0], limit=1)
                            newtransaction2 = list()
                            if a['BUY'][0][0] / orderbooks[threepairs[0]][1][0][0] / percentage[1] > 1.003:
                                newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                while newtransaction2 == None:
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    time.sleep(1)
                                    print('Trying to create order')
                                time.sleep(5)
                                c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                            else:
                                new_attempt = 1
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt started working\n')
                                stored_data.close()
                                while new_attempt < 100 and pendingAmount2 != 0: #a['SELL'][0][0] - (0.1 ** digit_count2) / orderbooks[threepairs[0]][1][0][0] / percentage[1] > 1.003
                                    a = new_client.get_order_book(threepairs[0], limit=1)
                                    stored_data = open('orderbooks.txt', 'a')
                                    stored_data.write(f"{a['SELL'][0][0]}\n")
                                    stored_data.close()
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['SELL'][0][0] - (0.1 ** digit_count2), pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    new_attempt += 1
                                    time.sleep(9)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                                    time.sleep(2)
                                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    if pendingAmount2 == None:
                                        print('Pending amount 2 = None!!!')
                                        while pendingAmount2 == None:
                                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                            print('Still None!!!')
                                if pendingAmount2 != 0:
                                    a = new_client.get_order_book(threepairs[0], limit=1)
                                    newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                    while newtransaction2 == None:
                                        newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                                        time.sleep(1)
                                        print('Trying to create order')
                                    time.sleep(5)
                                    c = new_client.cancel_order(newtransaction2, Client.SIDE_SELL, threepairs[0])
                                stored_data = open('orderbooks.txt', 'a')
                                stored_data.write('New attempt finished working\n')
                                stored_data.close()
                            # attempt = 1
                            # newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            # while newtransaction2 == None and attempt < 100:
                            #     attempt += 1
                            #     newtransaction2 = new_client.create_order(threepairs[0], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount2)
                            #     time.sleep(1)
                            stored_data = open('orderbooks.txt', 'a')
                            stored_data.write('New second transaction finished')
                            stored_data.close()
                            print('Second transaction begins')
                            time.sleep(2)
                            pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                            if pendingAmount2 == None:
                                print('Pending amount 2 = None!!!')
                                while pendingAmount2 == None:
                                    pendingAmount2 = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                            b = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                            if b == None:
                                print('Deal amount 2 = None!!!')
                                while b == None:
                                    b = new_client.get_order_details(threepairs[0], Client.SIDE_SELL, order_id=newtransaction2, limit=10, page=1)['dealAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                                dealAmount2 += b
                            third_trans_amount += b * a['BUY'][0][0]
                            balance2_after = new_client.get_coin_balance(threepairs[0].split('-')[1])['balance']
                        third_amount_rounded = f"%.{digit_count2}f" % ((third_trans_amount * 0.999) - (0.1 ** digit_count2))
                        transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                        while transaction3 == None:
                            transaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, orderbooks[threepairs[2]][1][0][0], float(third_amount_rounded))
                            time.sleep(1)
                            print('Trying to create order')
                        print('Third transaction begins')
                        time.sleep(5)
                        c = new_client.cancel_order(transaction3, Client.SIDE_SELL, threepairs[2])
                        time.sleep(2)
                        pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                        if pendingAmount3 == None:
                            print('Pending amount 3 = None!!!')
                            while pendingAmount3 == None:
                                pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['pendingAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                        if dealAmount3 == None:
                            print('Deal amount 3 = None!!!')
                            while dealAmount3 == None:
                                dealAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=transaction3, limit=10, page=1)['dealAmount']
                                print('Still None!!!')
                                time.sleep(2)
                        while pendingAmount3 != 0:
                            a = new_client.get_order_book(threepairs[2], limit=1)
                            newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                            while newtransaction3 == None:
                                newtransaction3 = new_client.create_order(threepairs[2], Client.SIDE_SELL, a['BUY'][0][0], pendingAmount3)
                                time.sleep(1)
                                print('Trying to create order')
                            print('Third transaction')
                            time.sleep(5)
                            c = new_client.cancel_order(newtransaction3, Client.SIDE_SELL, threepairs[2])
                            time.sleep(2)
                            pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                            if pendingAmount3 == None:
                                print('Pending amount 3 = None!!!')
                                while pendingAmount3 == None:
                                    pendingAmount3 = new_client.get_order_details(threepairs[2], Client.SIDE_SELL, order_id=newtransaction3, limit=10, page=1)['pendingAmount']
                                    print('Still None!!!')
                                    time.sleep(2)
                        my_file = open(f'{coin1}{name}.txt', 'r')
                        read = my_file.read()
                        my_file.close()
                        my_file = open(f'{coin1}{name}.txt', 'w')
                        new_reserve = float(read) - float(float(prev_reserved_bal) + reserved_balance)
                        read = str(new_reserve)
                        my_file.write(read)
                        my_file.close()
                        return 1
                else:
                    return 1
            else:
                print('Not enough money')
            return 0
    except Exception as e:
        # if isinstance(e, IndexError):
        #     return 0
        stored_data = open('orderbooks.txt', 'a')
        stored_data.write(f'\n{percentage}\n')
        stored_data.write(str(e))
        stored_data.write(str(traceback.format_exc()))
        stored_data.write(str(time.ctime(time.time())))
        stored_data.close()
        coin_file = open(f'coins{name}.txt', 'r')
        coin_read = coin_file.read()
        coin_file.close()
        coin_name = threepairs[0].split('-')[0]
        if f'{coin_name}-1' in coin_read:
            coin_file_2 = open(f'coins{name}.txt', 'w')
            coin_read = coin_read.replace(f'{coin_name}-1', f'{coin_name}-0')
            coin_file_2.write(coin_read)
            coin_file_2.close()
        if reserved_balance != 0:
            if (number == 1 and percentage == 2) or (number == 0 and percentage == 1):
                my_file = open(f'{coin2}{name}.txt', 'r')
                read = my_file.read()
                my_file.close()
                my_file = open(f'{coin2}{name}.txt', 'w')
                new_reserve = float(read) - reserved_balance
                read = str(new_reserve)
                my_file.write(read)
                my_file.close()
            else:
                my_file = open(f'{coin1}{name}.txt', 'r')
                read = my_file.read()
                my_file.close()
                my_file = open(f'{coin1}{name}.txt', 'w')
                new_reserve = float(read) - reserved_balance
                read = str(new_reserve)
                my_file.write(read)
                my_file.close()
        print(e)
        print('Something went wrong!!! Fix it now!')
        return 0
