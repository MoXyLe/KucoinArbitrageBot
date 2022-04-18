from kucoin.client import Client
import kucoin
import time
import createandcancel
def calculate(number, firstformula, threepairs, firstcoinamount, client, orderbooks):
    if number == 0:
        try:
            percentage1 = firstformula[0][0]/firstformula[1][1]/firstformula[2][1]
            print(1)
            print(orderbooks)
            print(firstformula[0], firstformula[1], firstformula[2])
            print('first perc', percentage1)
            # if percentage1 <= 0.9922:
            #     firstsecondamount = float()
            #     if firstcoinamount[0][0][0][1] >= firstcoinamount[1][1][0][1]:
            #         firstsecondamount = firstcoinamount[1][1][0][1]
            #     else:
            #         firstsecondamount = firstcoinamount[0][0][0][1]
            if percentage1 <= 0.9922:
                firstsecondamount = float()
                if firstcoinamount[0][0][0][1] >= firstcoinamount[1][1][0][1]:
                    firstsecondamount = firstcoinamount[1][1][0][1]
                else:
                    firstsecondamount = firstcoinamount[1][1][0][1]
                if firstcoinamount[1][1][0][1] >= firstcoinamount[0][0][0][1]:
                    if firstcoinamount[2][1][0][2]/firstcoinamount[0][0][0][0] >= firstcoinamount[0][0][0][1]:
                        firstsecondamount = firstcoinamount[0][0][0][1]
                    else:
                        firstsecondamount = firstcoinamount[2][1][0][2]/firstcoinamount[0][0][0][0]
                else:
                    if firstcoinamount[2][1][0][2]/firstcoinamount[0][0][0][0] >= firstcoinamount[1][1][0][1]:
                        firstsecondamount = firstcoinamount[1][1][0][1]
                    else:
                        firstsecondamount = firstcoinamount[2][1][0][2]/firstcoinamount[0][0][0][0]
                amount = client.get_currencies(threepairs[0].split('-')[0])
                #print('amount = ', amount)
                if amount['rates'][threepairs[0].split('-')[0]]['USD']*firstsecondamount > 1.0:
                    print(0)
                    print(orderbooks)
                    print(firstformula[0], firstformula[1], firstformula[2])
                    print('first perc =', percentage1)
                    print('USD = ', amount['rates'][threepairs[0].split('-')[0]]['USD']*firstsecondamount)
                    print('amount to buy =', firstsecondamount)
                    print(time.localtime())
                    # amountlist = [firstcoinamount[0][0][0][1], firstcoinamount[1][1][0][1]]
                    #print('amountlist = ', amountlist)
                    #createandcancel.order(['BUY', threepairs[0], firstformula[0][0], firstsecondamount], ['SELL', threepairs[1], firstformula[1][1], firstsecondamount], ['SELL', threepairs[2], firstformula[2][1], firstcoinamount[2][1][0][1]], client, 0, 1, firstcoinamount[0][1][0][1])
                #continue
            percentage2 = firstformula[1][0]/firstformula[0][1]*firstformula[2][0]
            print('second perc = ', percentage2)
            if percentage2 <= 0.9922 and percentage1 >= 0.9922:
                firstsecondamount = float()
                if firstcoinamount[1][0][0][1] >= firstcoinamount[0][1][0][1]:
                    firstsecondamount = firstcoinamount[0][1][0][1]
                else:
                    firstsecondamount = firstcoinamount[1][0][0][1]
                if firstcoinamount[1][0][0][1] >= firstcoinamount[0][1][0][1]:
                    if firstcoinamount[2][0][0][2]/firstcoinamount[0][0][0][0] >= firstcoinamount[0][1][0][1]:
                        firstsecondamount = firstcoinamount[0][1][0][1]
                    else:
                        firstsecondamount = firstcoinamount[2][0][0][2]/firstcoinamount[0][0][0][0]
                else:
                    if firstcoinamount[2][0][0][2]/firstcoinamount[0][0][0][0] >= firstcoinamount[1][0][0][1]:
                        firstsecondamount = firstcoinamount[1][0][0][1]
                    else:
                        firstsecondamount = firstcoinamount[2][0][0][2]/firstcoinamount[0][0][0][0]
                amount = client.get_currencies(threepairs[0].split('-')[0])
                #print('amount = ', amount)
                if amount['rates'][threepairs[0].split('-')[0]]['USD']*firstsecondamount > 1.0:
                    print(0)
                    print(orderbooks)
                    print(firstformula[1], firstformula[0], firstformula[2])
                    print('second perc =', percentage2)
                    print('USD = ', amount['rates'][threepairs[0].split('-')[0]]['USD']*firstsecondamount)
                    print('amount to buy =', firstsecondamount)
                    print(time.localtime())
                    #createandcancel.order(['BUY', threepairs[1], firstformula[1][0], firstsecondamount], ['SELL', threepairs[0], firstformula[0][1], firstsecondamount], ['BUY', threepairs[2], firstformula[2][0], firstcoinamount[2][0][0][1]], client, 0, 2, firstcoinamount[0][1][0][1])
                #continue
        except IndexError:
            # percentage = 1.0
            # print(percentage)
            pass
    else:
        try:
            percentage1 = firstformula[0][0]/firstformula[1][1]*firstformula[2][0]
            print(1)
            print(orderbooks)
            print(firstformula[0], firstformula[1], firstformula[2])
            print('first perc', percentage1)
            if percentage1 <= 0.9922:
                firstsecondamount = float()
                if firstcoinamount[0][0][0][1] >= firstcoinamount[1][1][0][1]:
                    firstsecondamount = firstcoinamount[1][1][0][1]
                else:
                    firstsecondamount = firstcoinamount[1][1][0][1]
                if firstcoinamount[1][1][0][1] >= firstcoinamount[0][0][0][1]:
                    if firstcoinamount[2][0][0][1]/firstcoinamount[0][0][0][0] >= firstcoinamount[0][0][0][1]:
                        firstsecondamount = firstcoinamount[0][0][0][1]
                    else:
                        firstsecondamount = firstcoinamount[2][0][0][1]/firstcoinamount[0][0][0][0]
                else:
                    if firstcoinamount[2][0][0][1]/firstcoinamount[0][0][0][0] >= firstcoinamount[1][1][0][1]:
                        firstsecondamount = firstcoinamount[1][1][0][1]
                    else:
                        firstsecondamount = firstcoinamount[2][0][0][1]/firstcoinamount[0][0][0][0]
                amount = client.get_currencies(threepairs[0].split('-')[0])
                #print('amount = ', amount)
                if amount['rates'][threepairs[0].split('-')[0]]['USD']*firstsecondamount > 1.0:
                    print(1)
                    print(orderbooks)
                    print(firstformula[0], firstformula[1], firstformula[2])
                    print('first perc', percentage1)
                    print('USD = ', amount['rates'][threepairs[0].split('-')[0]]['USD']*firstsecondamount)
                    print('amount to buy =', firstsecondamount)
                    print(time.localtime())
                    # amountlist = [firstcoinamount[0][0][0][1], firstcoinamount[1][1][0][1]]
                    # print('amountlist = ', amountlist)
                    #createandcancel.order(['BUY', threepairs[0], firstformula[0][0], firstsecondamount], ['SELL', threepairs[1], firstformula[1][1], firstsecondamount], ['BUY', threepairs[2], firstformula[2][0], firstcoinamount[2][0][0][1]], client, 1, 1, firstcoinamount[0][1][0][1])
                #continue
            percentage2 = firstformula[1][0]/firstformula[0][1]/firstformula[2][1]
            print('second perc = ', percentage2)
            if percentage2 <= 0.9922 and percentage1 >= 0.9922:
                firstsecondamount = float()
                if firstcoinamount[1][0][0][1] >= firstcoinamount[0][1][0][1]:
                    firstsecondamount = firstcoinamount[0][1][0][1]
                else:
                    firstsecondamount = firstcoinamount[1][0][0][1]
                if firstcoinamount[1][0][0][1] >= firstcoinamount[0][1][0][1]:
                    if firstcoinamount[2][1][0][1]/firstcoinamount[0][0][0][0] >= firstcoinamount[0][1][0][1]:
                        firstsecondamount = firstcoinamount[0][1][0][1]
                    else:
                        firstsecondamount = firstcoinamount[2][1][0][1]/firstcoinamount[0][0][0][0]
                else:
                    if firstcoinamount[2][1][0][1]/firstcoinamount[0][0][0][0] >= firstcoinamount[1][0][0][1]:
                        firstsecondamount = firstcoinamount[1][0][0][1]
                    else:
                        firstsecondamount = firstcoinamount[2][1][0][1]/firstcoinamount[0][0][0][0]
                amount = client.get_currencies(threepairs[0].split('-')[0])
                #print('amount = ', amount)
                if amount['rates'][threepairs[0].split('-')[0]]['USD']*firstsecondamount > 1.0:
                    print(1)
                    print(orderbooks)
                    print(firstformula[1], firstformula[0], firstformula[2])
                    print('second perc', percentage2)
                    print('USD = ', amount['rates'][threepairs[0].split('-')[0]]['USD']*firstsecondamount)
                    print('amount to buy =', firstsecondamount)
                    print(time.localtime())
                    # amountlist = [firstcoinamount[0][0][0][1], firstcoinamount[1][1][0][1]]
                    # print('amountlist = ', amountlist)
                    #createandcancel.order(['BUY', threepairs[1], firstformula[1][0], firstsecondamount], ['SELL', threepairs[0], firstformula[0][1], firstsecondamount], ['SELL', threepairs[2], firstformula[2][1], firstcoinamount[2][1][0][1]], client, 1, 2, firstcoinamount[0][1][0][1])
                #continue
            # percentslist[f'{i}11'] = percentage1
            # percentslist[f'{i}12'] = percentage2
        except IndexError:
            # percentage = 1.0
            # print(percentage)
            pass
