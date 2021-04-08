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
    # events = await api.get_le_events()
    for event in events[0]['Categories'][0]['Leagues'][0]['Matches']:
        event_details = await api.get_event_details(event['Id'])
        parsed_event = parser.parse(event_details)
        print()
        # For v1
        v1_event = parsed_event['v1']
        # kafka producer here

            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())