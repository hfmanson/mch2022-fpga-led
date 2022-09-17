import buttons
from .fpga_led import FPGALED

status = 0
led = FPGALED()
led.led_state(True)

# from https://github.com/badgeteam/mch2022-firmware-ice40/blob/master/projects/selftest/fw/fw_app.c
def led_set_status():
	global status
	if (status == 0):
		# Pre-boot continuous blue
		led.led_color(4, 4, 24)
		led.led_blink(False, 0, 0)
		led.led_breathe(False, 0, 0)
		led.exec()
	elif (status == 1):
		# Running: slow breathe blue
		led.led_color(4, 4, 24)
		led.led_blink(True, 200, 1000)
		led.led_breathe(True, 100, 200)
		led.exec()
	elif (status == 2):
		# Good: continuous green */
		led.led_color(0, 16, 0)
		led.led_blink(False, 0, 0)
		led.led_breathe(False, 0, 0)
		led.exec()
	elif (status == 3):
		# Bad: agressive red blink
		led.led_color(16, 0, 0)
		led.led_blink(True, 100, 100)
		led.led_breathe(False, 0, 0)
		led.exec()

def on_action_btn_b(pressed):
	global status
	if pressed:
		status += 1
		if (status > 3):
			status = 0
		led_set_status()

buttons.attach(buttons.BTN_B, on_action_btn_b)
