import machine
from Timer import Timer


class MotionSensor:

    def __init__(self, pin, retrigger_delay_ms, timer_n=1):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.retrigger_delay_ms = retrigger_delay_ms

        self.timer_n = timer_n
        self.timer = None
        self.last_motion = 0
        self.should_update = False

    def poll(self):
        if self.pin.value():
            self._motion_detected()
            if self.timer is not None:
                self.timer.stop()
                self.timer = None
            self.timer = Timer(timer_number=self.timer_n * -1,
                               mode=Timer.ONE_SHOT,
                               period=self.retrigger_delay_ms,
                               callback=self._no_motion_detected)
        return self.last_motion

    def _motion_detected(self):
        if not self.last_motion:
            self.last_motion = 1
            self.should_update = True

    def _no_motion_detected(self):
        self.last_motion = 0
        self.should_update = True
        
    def confirm_update(self):
        self.should_update = False

