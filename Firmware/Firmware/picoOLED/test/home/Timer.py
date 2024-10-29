import machine
import sys


class Timer:
    PERIODIC = machine.Timer.PERIODIC
    ONE_SHOT = machine.Timer.ONE_SHOT

    def __init__(self, timer_number, mode, period, callback):
        self._platform = sys.platform
        self.timer_number = timer_number
        self.mode = mode
        self.period = period
        self.callback = callback
        self._timer = None
        self.start()

    def _do_callback(self, _):
        self.callback()

    def start(self):
        if self._platform == "rp2":
            self._timer = machine.Timer(mode=self.mode, period=self.period, callback=self._do_callback)
        elif self._platform == 'esp32':
            tn = self.timer_number
            if tn > 0:
                tn = tn * -1
            self._timer = machine.Timer(tn)
            self._timer.init(mode=self.mode, period=self.period, callback=self._do_callback)
        else:
            raise Exception(f"Unsupported platform: {self._platform}")

    def stop(self):
        if self._timer is not None:
            self._timer.deinit()
