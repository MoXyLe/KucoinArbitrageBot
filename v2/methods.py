from kucoin.client import Client
import kucoin
import config
import time

class New_client:
    client = Client(config.api_key, config.api_secret)
    def create_order(self, pair, type, price, buy_amount):
        try:
            returning = self.client.create_order(pair, type, price, buy_amount)
            try:
                subscript = returning['orderOid']
                if subscript == None or subscript == '':
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f"\nsubscript is None or ''\n")
                    stored_data.close()
                return subscript
            except Exception as error:
                stored_data = open('orderbooks.txt', 'a')
                stored_data.write(f'\n{error}\n')
                stored_data.close()
                return self.create_order(pair, type, price, buy_amount)
        except Exception as error:
            try:
                a = f'{error}'
                if 'Min amount' in a:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{error}\n')
                    stored_data.close()
                    return 'Null'
                if "b''" in a:
                    time.sleep(10)
                    print('Exception on server, retrying!')
                    return self.create_order(pair, type, price, buy_amount)
            except Exception as e:
                stored_data = open('orderbooks.txt', 'a')
                stored_data.write('\nexception in create_order\n')
                stored_data.write(str(e))
                stored_data.close()
                return self.create_order(pair, type, price, buy_amount)
            if isinstance(error, kucoin.exceptions.KucoinAPIException):
                string = f'{error}'
                if 'Insufficient balance' not in string:
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{error}\n')
                    stored_data.close()
                return self.create_order(pair, type, price, buy_amount)
            print(error)
            print('create order')
            time.sleep(3)
            return self.create_order(pair, type, price, buy_amount)
    def get_coin_balance(self, coin):
        try:
            return self.client.get_coin_balance(coin)
        except Exception as error:
            print(error)
            print('get coin balance')
            time.sleep(3)
            return self.get_coin_balance(coin)
    def get_currencies(self, coin):
        try:
            return self.client.get_currencies(coin)
        except Exception as error:
            print(error)
            print('get currencies')
            time.sleep(3)
            return self.get_currencies(coin)
    def cancel_order(self, number, type, pair):
        try:
            return self.client.cancel_order(number, type, pair)
        except Exception as error:
            try:
                if 'Signature verification failed' in str(error):
                    time.sleep(20)
                    stored_data = open('orderbooks.txt', 'a')
                    stored_data.write(f'\n{error}\n')
                    stored_data.close()
                    return self.cancel_order(number, type, pair)
            except:
                pass
            print(error)
            print('cancel order')
            time.sleep(3)
            return self.cancel_order(number, type, pair)
    def get_order_details(self, pair, type, order_id, limit, page):
        try:
            returning = self.client.get_order_details(pair, type, order_id=order_id, limit=limit, page=page)
            try:
                subscript = returning['dealAmount']
                return returning
            except Exception as error:
                stored_data = open('orderbooks.txt', 'a')
                stored_data.write(f'\n{error}\n')
                stored_data.close()
                return self.get_order_details(pair, type, order_id, limit, page)
        except Exception as error:
            print(error)
            print('get order details')
            time.sleep(3)
            return self.get_order_details(pair, type, order_id, limit, page)
    def get_order_book(self, pair, limit):
        try:
            book = self.client.get_order_book(pair, limit=limit)
            sell = book['SELL'][0][0]
            return book
        except Exception as error:
            print(error)
            print('get order book')
            time.sleep(3)
            return self.get_order_book(pair, limit)
    def get_tick(self, pair):
        try:
            return self.client.get_tick(pair)
        except Exception as error:
            print(error)
            print('get tick')
            time.sleep(3)
            return self.get_tick(pair)
    def get_trading_markets(self):
        try:
            returning = self.client.get_trading_markets()
            try:
                subscript = returning[0]
                return returning
            except:
                stored_data = open('orderbooks.txt', 'a')
                stored_data.write('\nNoneType Error, retrying\n')
                stored_data.close()
                return self.get_trading_markets()
                time.sleep(1.5)
        except Exception as error:
            print(error)
            print('get markets')
            time.sleep(3)
            return self.get_trading_markets()
    def get_trading_symbols(self, symbol):
        try:
            returning = self.client.get_trading_symbols(symbol)
            try:
                subscript = returning[0]
                return returning
            except:
                stored_data = open('orderbooks.txt', 'a')
                stored_data.write('\nNoneType Error, retrying\n')
                stored_data.close()
                return self.get_trading_symbols(symbol)
                time.sleep(1.5)
        except Exception as error:
            print(error)
            print('get markets')
            time.sleep(3)
            return self.get_trading_markets(symbol)
    def get_recent_orders(self, symbol):
        try:
            returning = self.client.get_recent_orders(symbol)
            return returning
        except Exception as error:
            print(error)
            print('get markets')
            time.sleep(3)
            return self.get_recent_orders(symbol)
    def __init__(self, client):
        self.client = client
