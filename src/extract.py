import os
import time
import datetime
import warnings
import pandas as pd
from typing import Callable
from bs4 import BeautifulSoup

from connect import WebSocketClient
from validate import ALLOWED_TOKENPAIRS

SAVE_DIR = '/data'


def clear_html(text: str) -> str:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text(separator=' ')
        text = text.strip().replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
    return text


def get_df_with_time(filename: str, cols: list[str], start_time: datetime.datetime) -> tuple[int, pd.DataFrame]:
    cols = ['time', 'title', 'body']
    if os.path.exists(filename):
        data = pd.read_csv(filename)
        data['time'] = pd.to_datetime(data['time'])
        start_time = int(data['time'].iloc[-1].timestamp() + 1) * 1000
    else:
        data = pd.DataFrame(columns=cols)
        start_time = int(start_time.timestamp()) * 1000
    return start_time, data


def iterate_over_time(
    filename: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    step: int,
    data: pd.DataFrame,
    download: Callable[[WebSocketClient, int], list[dict]],
    parse: Callable[[pd.DataFrame], pd.DataFrame]):
    with WebSocketClient(demo=True, stream=False) as client:
        for t in range(start_time, end_time, step):
            time.sleep(1)
            show_time = lambda t: datetime.datetime.fromtimestamp(t // 1000).strftime('%d.%m.%Y')
            print(f'Downloading {show_time(t)} -> {show_time(t + step)}')
            data_t = download(client, t)
            if len(data_t) == 0: continue
            data_t = pd.DataFrame(data_t)
            data_t['time'] = pd.to_datetime(data_t['time'], unit='ms')
            data_t = parse(data_t)
            data_t = data_t.sort_values('time')
            if len(data) == 0: data = data_t
            else: data = pd.concat([data, data_t], ignore_index=True)
            data.to_csv(filename, index=False)
            print(f'Added {len(data_t)} items')
    print(f'Saved {len(data)} items')
    

def get_news():
    start_time = datetime.datetime(2023, 1, 1)
    end_time = int(datetime.datetime.now().timestamp()) * 1000
    cols = ['time', 'title', 'body']
    file = os.path.join(SAVE_DIR, 'news.csv')
    start_time, data = get_df_with_time(file, cols, start_time)
    step = 7 * 24 * 60 * 60 * 1000 # week
    def _download(client: WebSocketClient, t: int) -> list[dict]:
        return client.run('getNews', dict(start = t, end = t + step - 1), cols)
    def _parse(data: pd.DataFrame) -> pd.DataFrame:
        data['body'] = data['body'].apply(clear_html)
        data['title'] = data['title'].apply(clear_html)
        return data[cols]
    iterate_over_time(file, start_time, end_time, step, data, _download, _parse)


def get_symbols_info():
    # http://developers.xstore.pro/documentation/#getSymbol
    cols = [
        'low', 'high',
        'ask', 'bid', 'spreadRaw', 'spreadTable',
        'time', 'starting', 'description', 'symbol', 'type', 'categoryName', 'groupName',
        'contractSize', 'tickSize', 'tickValue', 
        'currency', 'currencyPair', 'currencyProfit',
        'initialMargin', 'instantMaxVolume', 'leverage',
        'longOnly', 'shortSelling', 'trailingEnabled',
        'lotMax', 'lotMin', 'lotStep',
        'marginHedged', 'marginHedgedStrong', 'marginMaintenance', 'marginMode',
        'pipsPrecision', 'precision', 
        'profitMode', 'quoteId',
        'swap_rollover3days', 'swapEnable', 'swapLong', 'swapShort', 'swapType',
    ]
    data = []
    with WebSocketClient(demo=True, stream=False) as client:
        for token in ALLOWED_TOKENPAIRS:
            data += client.run('getSymbol', dict(symbol=token), cols)
    data = pd.DataFrame(data)
    data['quoteId'] = data['quoteId'].map({1: 'fixed', 2: 'float', 3: 'depth', 4: 'cross'})
    data['marginMode'] = data['marginMode'].map({101: 'forex', 102: 'cfd leveraged', 103: 'cfd'})
    data['profitMode'] = data['profitMode'].map({5: 'forex', 6: 'cfd'})
    data.to_csv(os.path.join(SAVE_DIR, 'symbols.csv'), index=False)


if __name__ == '__main__':
    # get_news()
    # get_symbols_info()
    pass