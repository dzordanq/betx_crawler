import json
from collections import defaultdict
from Api import BetX
from Parser import Parser
from config import SPORTS, config
import asyncio


api = BetX()
parser = Parser(config)


async def main():
    events = await api.get_nba_events()
    for event in events[0]['Categories'][0]['Leagues'][0]['Matches']:
        event_details = await api.get_event_details(event['Id'])
        parsed_event = parser.parse(event_details)
        print()
            



loop = asyncio.get_event_loop()
loop.run_until_complete(main())