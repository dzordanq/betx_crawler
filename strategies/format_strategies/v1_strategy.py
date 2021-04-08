from .strategy import FormatStrategy

class V1Strategy(FormatStrategy):
    def __init__(self, strategy):
        super().__init__(strategy)


    def append_market(self, caller, parsed_market):
        if parsed_market:
            if caller.sport['translatedName'] == 'basketball':
                caller.response[self.strategy]['markets'][caller.market_name].append({
                    "playerName": caller.player_name,
                    "bets": parsed_market
                })
            else:
                caller.response[self.strategy]['markets'][caller.market_name].append(parsed_market)

