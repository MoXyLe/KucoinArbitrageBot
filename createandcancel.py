from kucoin.client import Client
import kucoin
import time
# Test async calls, while this method isn't called
def order(firstpair, secondpair, thirdpair, client, number, percentage, digitformat):
    result = ''
    try:
        firstbalance = client.get_coin_balance(firstpair[1].split('-')[1])['balance']
    except:
        print("Can't get balance")
        return
    try:
        firstdigits = len(str(digitformat).split('.')[1])
    except TypeError or IndexError:
        firstdigits = 0
    try:
        seconddigits = len(str(digitformat).split('.')[1])
    except TypeError or IndexError:
        seconddigits = 0
    if firstbalance > firstpair[2]*firstpair[3]:
        print('Buying full order')
        try:
            transaction = client.create_order(firstpair[1], firstpair[0], firstpair[2], float(format(firstpair[3], f'.{firstdigits}f')))
        except (kucoin.exceptions.KucoinAPIException or kucoin.exceptions.KucoinResponseException) as error:
            print('Something went wrong')
            print(error)
            return
        print(transaction)
        time.sleep(1.3)
        client.cancel_order(transaction["orderOid"], firstpair[0], firstpair[1])
        orders = client.get_order_details(firstpair[1], firstpair[0], None, None, transaction["orderOid"])
        if orders['pendingAmount'] != 0.0 and orders['dealAmount'] != 0.0:
            try:
                transaction2 = client.create_order(secondpair[1], secondpair[0], secondpair[2], float(format((orders['dealAmount']*0.999) - (0.1**firstdigits), f'.{firstdigits}f')))
            except:
                print('Something went wrong')
                return
            print(transaction2)
            time.sleep(1.3)
            client.cancel_order(transaction2["orderOid"], secondpair[0], secondpair[1])
            secondorder = client.get_order_details(secondpair[1], secondpair[0], None, None, transaction2["orderOid"])
            if (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0 and number == 0 and percentage == 1) or (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0 and number == 1 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondorder['orderPrice']*secondorder['dealAmount']*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0 and number == 1 and percentage == 1) or (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0 and number == 0 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondorder['orderPrice']*secondorder['dealAmount']/thirdpair[2]*0.999) - (0.1**seconddigits), f'.{seconddigits}f')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] == 0.0 and number == 0 and percentage == 1) or (secondorder['pendingAmount'] == 0.0 and number == 1 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((orders['orderPrice']*orders['dealAmount']*0.999*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] == 0.0 and number == 0 and percentage == 2) or (secondorder['pendingAmount'] == 0.0 and number == 1 and percentage == 1):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((orders['orderPrice']*orders['dealAmount']/thirdpair[2]*0.999*0.999) - (0.1**seconddigits), f'.{seconddigits}f')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            else:
                try:
                    client.cancel_order(transaction2["orderOid"], secondpair[0], secondpair[1])
                except:
                    pass
                print(orders)
                print(secondorder)
                print('No success')
        elif orders['pendingAmount'] == 0.0:
            transaction2 = client.create_order(secondpair[1], secondpair[0], secondpair[2], float(format((secondpair[3]*0.999) - (0.1**firstdigits), f'.{firstdigits}f')))
            print(transaction2)
            time.sleep(1.3)
            client.cancel_order(transaction2["orderOid"], secondpair[0], secondpair[1])
            secondorder = client.get_order_details(secondpair[1], secondpair[0], None, None, transaction2["orderOid"])
            if (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0 and number == 0 and percentage == 1) or (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0 and number == 1 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondorder['orderPrice']*secondorder['dealAmount']*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0 and number == 1 and percentage == 1) or (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0 and number == 0 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondorder['orderPrice']*secondorder['dealAmount']/thirdpair[2]*0.999) - (0.1**seconddigits), f'.{seconddigits}f')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                lient.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] == 0.0 and number == 0 and percentage == 1) or (secondorder['pendingAmount'] == 0.0 and number == 1 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondpair[2]*secondpair[3]*0.999*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] == 0.0 and number == 0 and percentage == 2) or (secondorder['pendingAmount'] == 0.0 and number == 1 and percentage == 1):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondpair[2]*secondpair[3]/thirdpair[2]*0.999*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            else:
                try:
                    client.cancel_order(transaction2["orderOid"], secondpair[0], secondpair[1])
                except:
                    pass
                print(orders)
                print(secondorder)
                print('No success')
        else:
            try:
                client.cancel_order(transaction["orderOid"], firstpair[0], firstpair[1])
            except:
                pass
            print(orders)
            print('No success')
    elif firstbalance > 0.0:
        print('Buying not full order')
        newamount = float(format(firstbalance/firstpair[2], f'.{firstdigits}f'))
        if newamount == 0:
            print('Not enough money')
            return
        try:
            transaction = client.create_order(firstpair[1], firstpair[0], firstpair[2], newamount)
        except (kucoin.exceptions.KucoinAPIException or kucoin.exceptions.KucoinResponseException) as error:
            print('Something went wrong')
            print(error)
            return
        print(transaction)
        time.sleep(1.3)
        client.cancel_order(transaction["orderOid"], firstpair[0], firstpair[1])
        orders = client.get_order_details(firstpair[1], firstpair[0], None, None, transaction["orderOid"])
        if orders['pendingAmount'] != 0.0 and orders['dealAmount'] != 0.0:
            transaction2 = client.create_order(secondpair[1], secondpair[0], secondpair[2], float((format(orders['dealAmount']*0.999) - (0.1**firstdigits), f'.{firstdigits}f')))
            print(transaction2)
            time.sleep(1.3)
            client.cancel_order(transaction2["orderOid"], secondpair[0], secondpair[1])
            secondorder = client.get_order_details(secondpair[1], secondpair[0], None, None, transaction2["orderOid"])
            if (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0.0 and number == 0 and percentage == 1) or (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0.0 and number == 1 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondorder['orderPrice']*secondorder['dealAmount']*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0.0 and number == 1 and percentage == 1) or (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0.0 and number == 0 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondorder['orderPrice']*secondorder['dealAmount']/thirdpair[2]*0.999) - (0.1**seconddigits), f'.{seconddigits}f')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] == 0.0 and number == 0 and percentage == 1) or (secondorder['pendingAmount'] == 0.0 and number == 1 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((orders['orderPrice']*orders['dealAmount']*0.999*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] == 0.0 and number == 0 and percentage == 2) or (secondorder['pendingAmount'] == 0.0 and number == 1 and percentage == 1):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((orders['orderPrice']*orders['dealAmount']/thirdpair[2]*0.999*0.999) - (0.1**seconddigits), f'.{seconddigits}f')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            else:
                try:
                    client.cancel_order(transaction2["orderOid"], secondpair[0], secondpair[1])
                except:
                    pass
                print(orders)
                print(secondorder)
                print('No success')
        elif orders['pendingAmount'] == 0.0:
            transaction2 = client.create_order(secondpair[1], secondpair[0], secondpair[2], float(format((newamount*0.999) - (0.1**firstdigits), f'.{firstdigits}f')))
            print(transaction2)
            time.sleep(1.3)
            client.cancel_order(transaction2["orderOid"], secondpair[0], secondpair[1])
            secondorder = client.get_order_details(secondpair[1], secondpair[0], None, None, transaction2["orderOid"])
            if (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0.0 and number == 0 and percentage == 1) or (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0.0 and number == 1 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondorder['orderPrice']*secondorder['dealAmount']*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0.0 and number == 1 and percentage == 1) or (secondorder['pendingAmount'] != 0.0 and secondorder['dealAmount'] != 0.0 and number == 0 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondorder['orderPrice']*secondorder['dealAmount']/thirdpair[2]*0.999) - (0.1**seconddigits), f'.{seconddigits}f')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] == 0.0 and number == 0 and percentage == 1) or (secondorder['pendingAmount'] == 0.0 and number == 1 and percentage == 2):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondpair[2]*newamount*0.999*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success')
            elif (secondorder['pendingAmount'] == 0.0 and number == 0 and percentage == 2) or (secondorder['pendingAmount'] == 0.0 and number == 1 and percentage == 1):
                try:
                    transaction3 = client.create_order(thirdpair[1], thirdpair[0], thirdpair[2], float(format((secondpair[2]*newamount/thirdpair[2]*0.999*0.999) - (0.1**seconddigits), f'.{seconddigits}')))
                except:
                    print('Something went wrong')
                    return
                print(transaction3)
                time.sleep(1.3)
                client.cancel_order(transaction3["orderOid"], thirdpair[0], thirdpair[1])
                thirdorder = client.get_order_details(thirdpair[1], thirdpair[0], None, None, transaction3["orderOid"])
                print(orders)
                print(secondorder)
                print(thirdorder)
                print('Success!')
            else:
                try:
                    client.cancel_order(transaction2["orderOid"], secondpair[0], secondpair[1])
                except:
                    pass
                print(orders)
                print(secondorder)
                print('No success')
        else:
            try:
                client.cancel_order(transaction["orderOid"], firstpair[0], firstpair[1])
            except:
                pass
            print(orders)
            print('No success')
    else:
        print('There is no money to buy!')
    return
