"""Data on COVD19.

sources:

https://ourworldindata.org/coronavirus
"""


DATA_DEATH_PERCENTAGE = {
    # Date: 2010-03-22
    'china': {'2010-03-22': 3265/81345},
    'italy': {'2010-03-22': 4825/53578},
    'brazil': {
        '2010-03-22-GOV-BR': 25/1546,
        '2010-03-22-JOHN-HOP': 18/1546,
        '2010-03-22-GOV-SP': 0.03},
    'korea': {'2010-03-22': 3265/81345},
}


DATA_BRAZIL = {
    'country': 'Brasil',
    'population': 206e6,
    'infected': 1,
    'doublingdays': 2.6766,  # calibrated
    'halvingdays': 21.7258,  # calibrated
    'death_percentage': DATA_DEATH_PERCENTAGE['brazil']['2010-03-22-GOV-SP'],
    'beds': 1.74,
    'history': [
        1, 1, 1, 1, 2, 2, 2, 2, 3, 8, 13,
        19, 25, 25, 34, 52, 77, 151, 151,
        200, 234, 346, 529, 640, 970, 1178],
    'tol': 1.0,
    }

DATA_KOREA = {
    'country': 'Coréia',
    'population': 51.709e6,
    'infected': 1,
    'doublingdays': 2.3,
    'halvingdays': 10,
    'death_percentage': DATA_DEATH_PERCENTAGE['korea']['2010-03-22'],
    'beds': 1.74,

    # [2020-03-22]
    # https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_South_Korea
    # dia 0: 2020-01-24
    'history': [
        1, 1, 1, 1, 2, 2, 3, 4, 4, 4, 6, 11, 12, 15, 15, 16, 19, 23,
        24, 24, 27, 27, 28, 28, 29, 30, 31, 51, 104, 204, 433,
        602, 833, 977, 1261, 1766, 2337, 3150, 4212],
    'tol': 1.0,
    }
