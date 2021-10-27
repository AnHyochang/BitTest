from re import split
import time
import pyupbit
import datetime

access = ""
secret = ""

def get_sell_price(ticker, k, type):
    start_price = get_balanceBuyPrice(ticker)
    if type == 'up':        
        target_price = start_price + (int(start_price) * k)
        return target_price
    else:
        target_price = start_price - (int(start_price) * k)
        return target_price

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_BitBalance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['avg_buy_price'] is not None:
                return int( (float(b['balance'])+float(b['locked'])) * float(b['avg_buy_price']) )
            else:
                return 0
    return 0

def get_balanceBuyPrice(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0
    return 0

upbit = pyupbit.Upbit(access, secret)

print("AutoTrade Start")
BitArray = ['KRW-BTC', 'KRW-ETH', 'KRW-BCH', 'KRW-LTC', 'KRW-BSV', 'KRW-SOL', 'KRW-AXS', 'KRW-BTG', 'KRW-STRK', 'KRW-ETC', 'KRW-NEO', 'KRW-DOT', 'KRW-ATOM', 'KRW-LINK', 'KRW-POLY', 'KRW-ONT', 'KRW-MOC', 'KRW-WAVES', 'KRW-GAS', 'KRW-TON', 'KRW-XTZ', 'KRW-CBK', 'KRW-OMG', 'KRW-KAVA', 'KRW-MTL', 'KRW-SXP', 'KRW-ADA', 'KRW-ELF']
BitDic = {'KRW-BTC':0, 'KRW-ETH':0, 'KRW-BCH':0, 'KRW-LTC':0, 'KRW-BSV':0, 'KRW-SOL':0, 'KRW-AXS':0, 'KRW-BTG':0, 'KRW-STRK':0, 'KRW-ETC':0, 'KRW-NEO':0, 'KRW-DOT':0, 'KRW-ATOM':0, 'KRW-LINK':0, 'KRW-POLY':0, 'KRW-ONT':0, 'KRW-MOC':0, 'KRW-WAVES':0, 'KRW-GAS':0, 'KRW-TON':0, 'KRW-XTZ':0, 'KRW-CBK':0, 'KRW-OMG':0, 'KRW-KAVA':0, 'KRW-MTL':0, 'KRW-SXP':0, 'KRW-ADA':0, 'KRW-ELF':0}
BitMaxDic = {'KRW-BTC':0, 'KRW-ETH':0, 'KRW-BCH':0, 'KRW-LTC':0, 'KRW-BSV':0, 'KRW-SOL':0, 'KRW-AXS':0, 'KRW-BTG':0, 'KRW-STRK':0, 'KRW-ETC':0, 'KRW-NEO':0, 'KRW-DOT':0, 'KRW-ATOM':0, 'KRW-LINK':0, 'KRW-POLY':0, 'KRW-ONT':0, 'KRW-MOC':0, 'KRW-WAVES':0, 'KRW-GAS':0, 'KRW-TON':0, 'KRW-XTZ':0, 'KRW-CBK':0, 'KRW-OMG':0, 'KRW-KAVA':0, 'KRW-MTL':0, 'KRW-SXP':0, 'KRW-ADA':0, 'KRW-ELF':0}

while True:
    try:
        for TARGET_BIT in BitArray:
            #print(">>TARGET_BIT : " + TARGET_BIT + " > " + TARGET_BIT.replace("KRW-",""))
            now = datetime.datetime.now()
            start_time = get_start_time("KRW-BTC")
            end_time = start_time + datetime.timedelta(days=1)

            if start_time < now < end_time - datetime.timedelta(seconds=180):
                target_price = get_target_price(TARGET_BIT, 0.4)
                current_price = pyupbit.get_current_price(TARGET_BIT)
                target_top_price = target_price + (target_price*0.05)
                sell_up_price = get_sell_price(TARGET_BIT.replace("KRW-",""), 0.02, 'up')
                sell_down_price = get_sell_price(TARGET_BIT.replace("KRW-",""), 0.03, 'down')
                krw = get_balance("KRW")

                isBitPrice = get_BitBalance(TARGET_BIT.replace("KRW-",""))
                if target_price < current_price < target_top_price: 
                    if krw > 5000 and isBitPrice < 1000 :
                        if BitDic[TARGET_BIT] >= 5 and krw > 40000:
                            print(TARGET_BIT + " BuyCount ON" + " Count: " + str(BitDic[TARGET_BIT]))
                            upbit.buy_market_order(TARGET_BIT, 50000*0.9995)
                        else:
                            BitDic[TARGET_BIT] = BitDic[TARGET_BIT] + 1
                    elif krw > 1000 and isBitPrice > 1000 and current_price > sell_up_price :
                        if current_price > BitMaxDic[TARGET_BIT]:
                            BitMaxDic[TARGET_BIT] = current_price

                        max_down_price = BitMaxDic[TARGET_BIT] - (int(BitMaxDic[TARGET_BIT])*0.01)
                        if current_price < max_down_price:
                            print(TARGET_BIT + " Sell Price Max Down SELL : " + str(sell_up_price) + " << " + str(sell_up_price))
                            btc = get_balance(TARGET_BIT.replace("KRW-",""))
                            #upbit.sell_market_order(TARGET_BIT, btc*0.9995)
                            upbit.sell_market_order(TARGET_BIT, btc)
                            BitArray.remove(TARGET_BIT)
                    elif krw > 1000 and isBitPrice > 1000 and BitMaxDic[TARGET_BIT] > 0:
                        if current_price > BitMaxDic[TARGET_BIT]:
                            BitMaxDic[TARGET_BIT] = current_price

                        max_down_price = BitMaxDic[TARGET_BIT] - (int(BitMaxDic[TARGET_BIT])*0.01)
                        if current_price < max_down_price:
                            print(TARGET_BIT + " Sell Price Up SELL : " + str(sell_up_price) + " << " + str(sell_up_price))
                            btc = get_balance(TARGET_BIT.replace("KRW-",""))
                            #upbit.sell_market_order(TARGET_BIT, btc*0.9995)
                            upbit.sell_market_order(TARGET_BIT, btc)
                            BitArray.remove(TARGET_BIT)
                elif krw > 1000 and isBitPrice > 1000 and current_price > sell_up_price:
                    if current_price > BitMaxDic[TARGET_BIT]:
                        BitMaxDic[TARGET_BIT] = current_price

                    max_down_price = BitMaxDic[TARGET_BIT] - (int(BitMaxDic[TARGET_BIT])*0.01)
                    if current_price < max_down_price:
                        print(TARGET_BIT + " Sell Price Max Down SELL : " + str(sell_up_price) + " << " + str(sell_up_price))
                        btc = get_balance(TARGET_BIT.replace("KRW-",""))
                        upbit.sell_market_order(TARGET_BIT, btc)
                        BitArray.remove(TARGET_BIT)
                elif krw > 1000 and isBitPrice > 1000 and current_price < sell_down_price:
                        btc = get_balance(TARGET_BIT.replace("KRW-",""))
                        upbit.sell_market_order(TARGET_BIT, btc)
                        BitArray.remove(TARGET_BIT)
            else:
                btc = get_balance(TARGET_BIT.replace("KRW-",""))
                if btc > 0.00008 and current_price < sell_up_price: 
                    print("TARGET_BIT3===> " + TARGET_BIT)
                    upbit.sell_market_order(TARGET_BIT, btc)
                
                BitArray = ['KRW-BTC', 'KRW-ETH', 'KRW-BCH', 'KRW-LTC', 'KRW-BSV', 'KRW-SOL', 'KRW-AXS', 'KRW-BTG', 'KRW-STRK', 'KRW-ETC', 'KRW-NEO', 'KRW-DOT', 'KRW-ATOM', 'KRW-LINK', 'KRW-POLY', 'KRW-ONT', 'KRW-MOC', 'KRW-WAVES', 'KRW-GAS', 'KRW-TON', 'KRW-XTZ', 'KRW-CBK', 'KRW-OMG', 'KRW-KAVA', 'KRW-MTL', 'KRW-SXP', 'KRW-ADA', 'KRW-ELF']
                BitDic = {'KRW-BTC':0, 'KRW-ETH':0, 'KRW-BCH':0, 'KRW-LTC':0, 'KRW-BSV':0, 'KRW-SOL':0, 'KRW-AXS':0, 'KRW-BTG':0, 'KRW-STRK':0, 'KRW-ETC':0, 'KRW-NEO':0, 'KRW-DOT':0, 'KRW-ATOM':0, 'KRW-LINK':0, 'KRW-POLY':0, 'KRW-ONT':0, 'KRW-MOC':0, 'KRW-WAVES':0, 'KRW-GAS':0, 'KRW-TON':0, 'KRW-XTZ':0, 'KRW-CBK':0, 'KRW-OMG':0, 'KRW-KAVA':0, 'KRW-MTL':0, 'KRW-SXP':0, 'KRW-ADA':0, 'KRW-ELF':0}
                BitMaxDic = {'KRW-BTC':0, 'KRW-ETH':0, 'KRW-BCH':0, 'KRW-LTC':0, 'KRW-BSV':0, 'KRW-SOL':0, 'KRW-AXS':0, 'KRW-BTG':0, 'KRW-STRK':0, 'KRW-ETC':0, 'KRW-NEO':0, 'KRW-DOT':0, 'KRW-ATOM':0, 'KRW-LINK':0, 'KRW-POLY':0, 'KRW-ONT':0, 'KRW-MOC':0, 'KRW-WAVES':0, 'KRW-GAS':0, 'KRW-TON':0, 'KRW-XTZ':0, 'KRW-CBK':0, 'KRW-OMG':0, 'KRW-KAVA':0, 'KRW-MTL':0, 'KRW-SXP':0, 'KRW-ADA':0, 'KRW-ELF':0}
            time.sleep(1)
        time.sleep(2)
    except Exception as e:
        print(e)
        time.sleep(1)
