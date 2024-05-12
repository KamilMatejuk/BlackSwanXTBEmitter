import connexion
import pandas as pd
from flask import jsonify
from decouple import Config, RepositoryEnv
from flask_socketio import SocketIO

from src.validate import validate_tokenpair, validate_interval, validate_times, validate_indicator


def get_price_for_timerange(
        tokenPair: str,
        interval: str,
        startTime: int,
        endTime: int):
    try:
        validate_tokenpair(tokenPair)
        validate_interval(interval)
        validate_times(startTime, endTime)
    except Exception as ex:
        return jsonify({"error": "Invalid request schema", "details": str(ex)}), 401
    
    # data = pd.read_csv(f'data/binance_{tokenPair}_{interval}.csv')
    # data = data[['timestamp_close', 'price_close']]
    # data = data.rename(columns={'timestamp_close': 'timestamp', 'price_close': 'price'})
    # data = data[(data['timestamp'] >= startTime) & (data['timestamp'] <= endTime)]
    # return list(data.T.to_dict().values()), 200
    # TODO


def get_indicators_for_timerange(
        tokenPair: str,
        interval: str,
        startTime: int,
        endTime: int,
        indicator: str):
    try:
        validate_tokenpair(tokenPair)
        validate_interval(interval)
        validate_times(startTime, endTime)
    except Exception as ex:
        return jsonify({"error": "Invalid request schema", "details": str(ex)}), 401

    # data = pd.read_csv(f'data/binance_{tokenPair}_{interval}.csv')
    
    # try:
    #     validate_indicator(indicator, list(data.columns))
    # except Exception as ex:
    #     return jsonify({"error": "Invalid request schema", "details": str(ex)}), 401
    
    # data = data[['timestamp_close', indicator]]
    # data = data.rename(columns={'timestamp_close': 'timestamp'})
    # data = data[(data['timestamp'] >= startTime) & (data['timestamp'] <= endTime)]
    # return list(data.T.to_dict().values()), 200
    # TODO


config = Config(RepositoryEnv('.env.local'))
port = config.get('PORT')
app = connexion.FlaskApp(__name__,
        server='tornado',
        specification_dir='',
        options={'swagger_url': '/swagger-ui'})
app.add_api('openapi.yaml')
print(f' * Checkout SwaggerUI http://127.0.0.1:{port}/swagger-ui/')
socketio = SocketIO(app.app)
socketio.run(app.app, port=port)
