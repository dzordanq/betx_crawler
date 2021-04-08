from datetime import datetime, timezone
from copy import deepcopy
from collections import defaultdict, OrderedDict
from typing import DefaultDict 
from strategies.format_strategies.strategy import FormatStrategy
from strategies.format_strategies import MultiWayPlayerBetStrategy, DefaultStrategy, V1Strategy

local_timezone = datetime.now().astimezone().tzinfo

class Parser:
    def __init__(self, config) -> None:
        self.config = config
        self.strategy: FormatStrategy = None
        self.strategies = {
            'default': DefaultStrategy('default'),
            'multiwayPlayerBet': MultiWayPlayerBetStrategy('multiwayPlayerBet'),
            'v1': V1Strategy('v1')
        }
        self.player_name: str = ''

    def parse(self, event):
        self.response = {
            'default': None,
            'multiwayPlayerBet': {},
            'v1': None
        }
        event_info = self._get_event_info(event)
        if event_info:
            self.event_info = event_info
            self.response['default'] = deepcopy(event_info)
            self.response['v1'] = deepcopy(event_info)
            for market in event['Offers']:
                parsed_market = self._parse_market(market)
                if parsed_market:
                    self.strategy.append_market(self, parsed_market)

            
            return {
                "default": self.response['default'],
                "v1": self.response['v1'],
                "multiwayPlayerBet": [
                    {
                        **p,
                        'markets': [
                            {
                                "marketName": market_name,
                                "bets": market_value
                            } for market_name, market_value in p['markets'].items()]
                        
                    } for p in self.response['multiwayPlayerBet'].values()]
            }


    def _get_event_info(self, event):
        self.home_name = event['TeamHome']
        self.away_name = event['TeamAway']
        sport = event['SportName']
        if sport in self.config:
            self.sport = self.config[sport]
            date = datetime.fromisoformat(event['MatchStartTime'][:-1])
            date = date.replace(tzinfo=timezone.utc).astimezone(tz=local_timezone)
            return {
                "homeName": self.home_name,
                "awayName": self.away_name,
                "date": date.strftime("%Y-%m-%d"),
                "hour": date.strftime("%H:%M"),
                "competition": event['LeagueName'],
                "country": event['CategoryName'],
                "sport": self.sport['translatedName'],
                "markets": defaultdict(list)
            }

    
    def _parse_market(self, market):
        market_name = market['OriginDescription']
        if market_name in self.sport['markets']:
            self.market_name = self.sport['markets'][market_name]['translatedName']
            # Set strategy
            strategy = self.sport['markets'][market_name]['strategy'] 
            self.strategy = self.strategies[strategy]

            self.line = market.get('Sbv')
            self.player_name = market.get('SbvText').replace(",","") if market.get('SbvText') else None
            outcomes = []
            for outcome in market['Odds']:
                parsed_outcome = self._parse_outcome(outcome)
                if parsed_outcome:
                    outcomes.append(parsed_outcome)

            return outcomes


    def _parse_outcome(self, outcome):
        if outcome['Active']:
            outcome_name = self._parse_outcome_name(outcome['Name'])
            outcome_odd = outcome['Odd']
            if outcome_odd > 0:
                if self.line:
                    outcome_name = f"{outcome_name} ({self.line})"
                return {
                    "outcomeName": outcome_name,
                    "outcomeOdd": outcome_odd
                }

    
    def _parse_outcome_name(self, outcome_name):
        transformed_outcome_name = outcome_name.replace("Więcej", "Over").replace("Mniej", "Under")
        if isinstance(self.strategy, MultiWayPlayerBetStrategy):
            if outcome_name.isnumeric():
                line = float(outcome_name) - 0.5
                transformed_outcome_name = f"Over ({line})"
        return transformed_outcome_name
       