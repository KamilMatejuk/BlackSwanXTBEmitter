ALLOWED_TOKENPAIRS = [
    'USD/PLN',
    'CHF/PLN',
    'CAD/PLN',
    'EUR/PLN',
    'UAH/PLN',
    'RUB/PLN',
]

ALLOWED_INTERVALS = [ '1d', '1h', '1m' ]


def validate_tokenpair(tokenPair: str):
    assert tokenPair in ALLOWED_TOKENPAIRS, f'Temporarly only {" ".join(ALLOWED_TOKENPAIRS)} pairs is supported'


def validate_interval(interval: str):
    assert interval in ALLOWED_INTERVALS, f'Temporarly only {" ".join(ALLOWED_INTERVALS)} intervals is supported'


def validate_times(startTime: int, endTime: int):
    assert startTime >= 1503100799999, 'Temporarly cannot start before 18.08.2017 (Unix 1503100799999)'
    assert endTime <= 1693180799999, 'Temporarly cannot end after 27.08.2023 (Unix 1693180799999)'
    assert startTime < endTime, 'Start time has to be before end time'


def validate_indicator(indicator: list, columns: list):
    assert indicator in columns, f'Unknown indicator {indicator}, only available are {columns}'
