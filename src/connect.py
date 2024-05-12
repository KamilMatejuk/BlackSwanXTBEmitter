# https://playground.xapi.pro/
# http://developers.xstore.pro/documentation/


import json
import datetime
import pandas as pd
from websockets.sync.client import connect
from decouple import Config, RepositoryEnv


pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

    
config = Config(RepositoryEnv('.env'))
USER_ID = config.get('USER_ID')
USER_PASSWORD = config.get('USER_PASSWORD')
LOG = False


class WebSocketClient:
    def __init__(self, demo: bool = True, stream: bool = False):
        self.url = self.get_base_url(demo, stream)
        self.websocket = connect(self.url)
        if LOG: print(f'Created client for {self.url}')
    
    def close(self):
        self.websocket.close()
    
    def get_base_url(self, demo: bool, stream: bool) -> str:
        # http://developers.xstore.pro/documentation/#communication-with-the-xstation-api
        slug1 = 'demo' if demo else 'real'
        slug2 = 'Stream' if stream else ''
        slug = slug1 + slug2
        ports = {
            'demo': 5124,
            'demoStream': 5125,
            'real': 5112,
            'realStream': 5113,
        }
        # port = ports[slug]
        # return f'wss://ws.xtb.com/{slug}:{port}'
        return f'wss://ws.xtb.com/{slug}'
    
    def run(self, cmd: str, args: dict | None = None, fields: list[str] | None = None) -> list:
        if LOG: print(f'Running {cmd}' + \
            (f' with {args}' if args is not None else '') + \
            (f' and selected fields {fields}' if fields is not None else ''))
        self.websocket.send(json.dumps({'command': cmd, 'arguments': args or {}}))
        msg = self.websocket.recv()
        resp = self._parse_response(msg, fields)
        if LOG: print(f'Got reponse {resp}')
        return resp
    
    def _parse_response(self, msg: str, fields: list[str] | None = None) -> list:
        try:
            msg = json.loads(msg)
            status = msg['status']
            if not status:
                print(f'Failed with code {msg["errorCode"]}: {msg["errorDescr"]}')
                return None
            if 'returnData' in msg: msg = msg['returnData']
            if fields is None: return msg
            assert len(fields) > 0, f'If fields are selected, cannot be of len 0'
            result = [self._extract_field(msg, f) for f in fields]
            if len(result) == 1: return result[0]
            return result
        except json.JSONDecodeError as ex:
            print(f'Failed parsing response "{msg}": {ex}')
            return None
    
    def _extract_field(self, data: dict | list, field: str) -> list:
        data = data.copy()
        for part in field.split('.'):
            if isinstance(data, dict): data = data[part]
            elif isinstance(data, (list, tuple)): data = data[int(part)]
        return data
        
    def login(self):
        return self.run('login', dict(userId=USER_ID, password=USER_PASSWORD), ['streamSessionId'])


if __name__ == '__main__':
    client = WebSocketClient(demo=True, stream=False)
    ssid = client.login()
    
    # data = client.run('getCalendar')
    # data = pd.DataFrame(data)
    # data['time'] = pd.to_datetime(data['time'], unit='ms')
    # print(data.head(5))
    
    # data = client.run('getNews', dict(
    #     start=int(datetime.datetime(2024, 1, 1).timestamp()) * 1000,
    #     end=int(datetime.datetime(2024, 2, 1).timestamp()) * 1000))
    # data = pd.DataFrame(data)
    # data['time'] = pd.to_datetime(data['time'], unit='ms')
    # print(data.head(5))

    client.close()