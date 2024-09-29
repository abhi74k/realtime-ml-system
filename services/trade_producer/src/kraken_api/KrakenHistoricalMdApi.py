import websocket
import json
from datetime import datetime
from loguru import logger
import requests
import time

class KrakenHistoricalMdApi:

    def __init__(self, ticker, from_dt_str, to_dt_str, on_trade_message=None, trace=False):

        self.ticker = ticker

        self.on_trade_message = on_trade_message
        self.trace = trace


        self.payload = {}
        self.headers = {
            'Accept': 'application/json'
        }

        self.from_epoch = int(datetime.strptime(from_dt_str, "%Y-%m-%d %H:%M:%S").timestamp())
        self.to_epoch = int(datetime.strptime(to_dt_str, "%Y-%m-%d %H:%M:%S").timestamp())

        self.base_url = "https://api.kraken.com/0/public/Trades?pair={}&since={}"

        logger.info(f"From date: {from_dt_str} ({self.from_epoch}), To date: {to_dt_str} ({self.to_epoch})")


    def run_forever(self):

        done = False
        since  = self.from_epoch

        while not done:

            # Print since which is epoch time in human radable format
            logger.info(f"Fetching trades since: {since} ({datetime.fromtimestamp(since)})")

            url = self.base_url.format(self.ticker, since)

            response = requests.request("GET", url, headers=self.headers, data=self.payload) # Retrieve 1000 trades
            response_text = response.text

            # Convert json test to dictionary
            response_dict = json.loads(response_text)

            error = response_dict['error']
            result = response_dict['result']

            since = int(result['last']) // 1e9
            del result['last']

            trade_list = result[self.ticker]
            logger.info(f"Ticker: {self.ticker}, Num trades: {len(trade_list)}")

            for trade in trade_list:
                price, volume, time_dbl, buy_sell, market_limit, miscellaneous, trade_id = trade
                time_secs = int(time_dbl)
                if time_secs >= self.to_epoch:
                    logger.info(f"Ticker:{self.ticker}, TimeSecs: {time_secs} ({datetime.fromtimestamp(time_secs)}) is greater than to_epoch: {datetime.fromtimestamp(self.to_epoch)}")
                    done = True
                    break

                if self.trace:
                    logger.info(f"Ticker:{self.ticker}, Price: {price}, Volume: {volume}, TimeSecs: {time_secs}, Buy/Sell: {buy_sell}, Market/Limit: {market_limit}, Miscellaneous: {miscellaneous}, Trade ID: {trade_id}")

                if self.on_trade_message is not None:
                    self.on_trade_message(self.ticker, int(time_dbl * 1e3), price, volume, buy_sell)

            time.sleep(1)

if __name__ == "__main__":

    ticker = "ETH/USD"
    from_dt = "2024-09-20 00:00:00"
    to_dt = "2024-09-21 00:00:00"

    subscriber = KrakenHistoricalMdApi(ticker, from_dt, to_dt, on_trade_message=None, trace=True)
    subscriber.run_forever()

    print("Done")
