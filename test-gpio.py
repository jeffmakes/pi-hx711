import gpiod
import time


chip = gpiod.chip("gpiochip0")

led_error = chip.get_line(11) 
led_armed = chip.get_line(5)
led_status = chip.get_line(7)

config = gpiod.line_request()
config.consumer = "jeff" # no idea what this does
config.request_type = gpiod.line_request.DIRECTION_OUTPUT

led_error.request(config)
led_armed.request(config)
led_status.request(config)

led_error.set_value(0)
led_armed.set_value(0)
led_status.set_value(0)

led_test = led_status

while True:
    led_test.set_value(0)
    time.sleep(0.3)
    led_test.set_value(1)
    time.sleep(0.3)

