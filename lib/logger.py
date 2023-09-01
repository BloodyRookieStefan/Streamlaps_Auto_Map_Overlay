############################################################################
# Contains program logging functions
# Date: 01.09.2023
############################################################################

from datetime import datetime

class CLogger:

    def __init__(self) -> None:
        pass

    def info(self, t):
        self._print('INFO', t)

    def warning(self, t):
        self._print('WARNING', t)

    def error(self, t):
        self._print('ERROR', t)

    def _print(self, preFix, t):
        print(f'{datetime.now().strftime("%d.%m.%Y-%H:%M:%S")}-{preFix}> {t}')

Log = CLogger()