

class TradeSettings:
    def __init__(self, ob):
        self.granularity= ob['granularity']
        self.dist = ob['dist']
        self.sl_pct= ob['sl_pct']
        self.tp_pct= ob['tp_pct']
        self.trailing_sl_trigger_pct= ob['trailing_sl_trigger_pct']
        self.trailing_sl_pct= ob['trailing_sl_pct']

    def __repr__(self):
        return str(vars(self))
    
    @classmethod
    def settings_to_str(cls, settings):
        ret_str = 'Trade Settings:\n'
        for _, v in settings.items():
            ret_str += f'{v}\n'
        ret_str += '\n'

        return ret_str