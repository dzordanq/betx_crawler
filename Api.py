from aiohttp import request
import json 


class BetX:

    def __init__(self) -> None:
        self.headers = {
            'authority': 'sportbettingapi.ebetx.pl',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'terminalid': '1',
            'accept-language': 'pl',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'content-type': 'application/json',
            'device-type': 'desktop',
            'accept': 'application/json, text/plain, */*',
            'languageid': 'pl',
            'origin': 'https://ebetx.pl',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://ebetx.pl/',
        }


    async def get_nba_events(self):
        payload = {
            "Offset":0,
            "Limit":50,
            "SportIds":[391], # BasketballId
            "CategoryIds":[2462],
            "LeagueIds":[19945],
            "DateFrom":"2021-04-08T11:56:13.981Z",
            "DateTo":"2022-02-01T23:00:00.980Z"
        }
        url = 'https://sportbettingapi.ebetx.pl/api/sport/offer/v2/sports/offer'

        async with request('POST', url, headers=self.headers, data=json.dumps(payload)) as response:
            data = await response.json()

        if data['Count'] > 0:
            return data['Response']
        else:
            return {}


    async def get_event_details(self, event_id):
        payload = {"MatchId": event_id}
        url = 'https://sportbettingapi.ebetx.pl/api/sport/offer/v2/match/offers'

        async with request('POST', url, headers=self.headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                data = await response.json()
            else:
                print("Response status: ", response.status)
                data = {}

        
        return data
