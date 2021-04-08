from .strategy import FormatStrategy

class DefaultStrategy(FormatStrategy):
    def __init__(self, strategy):
        super().__init__(strategy)


    def append_market(self, caller, parsed_market):
        caller.response[self.strategy]['markets'].append(parsed_market) if parsed_market else None

