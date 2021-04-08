SPORTS = {
        "football": 388,
        "basketball": 391
    }

import yaml
config = {}
with open(r'config.yml', encoding='utf-8') as config_file:
    yaml_config = yaml.load(config_file, Loader=yaml.FullLoader)
    for sport in yaml_config:
        config[sport['name']] = {
            'translatedName': sport['translatedName'],
            'markets': dict(zip(
                [market['name'] for market in sport['markets']], #keys
                [dict(list(market.items())[1:]) for market in sport['markets']] # values
            ))
        }

                           