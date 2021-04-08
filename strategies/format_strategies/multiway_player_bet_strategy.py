from copy import deepcopy
from .strategy import FormatStrategy
from collections import OrderedDict


class MultiWayPlayerBetStrategy(FormatStrategy):
    def __init__(self, strategy):
        super().__init__(strategy)

    
    def append_market(self, caller, parsed_market) -> None:
        if not caller.player_name in caller.response[self.strategy]:
            caller.response[self.strategy][caller.player_name] = OrderedDict(deepcopy(caller.event_info))
            caller.response[self.strategy][caller.player_name].update({'playerName': caller.player_name})
            caller.response[self.strategy][caller.player_name].move_to_end('playerName', last=False)
        
        caller.response[self.strategy][caller.player_name]['markets'][caller.market_name].extend(parsed_market)
        # Remove duplicates from market list
        market_list = caller.response[self.strategy][caller.player_name]['markets'][caller.market_name]
        market_list = [
            dict(t) for t 
            in {tuple(d.items())
            for d in market_list}
        ]
        caller.response[self.strategy][caller.player_name]['markets'] = market_list
