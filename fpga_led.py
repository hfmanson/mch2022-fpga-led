# Python version of https://github.com/badgeteam/mch2022-firmware-ice40/blob/master/projects/selftest/fw/led.c

import mch22
from fpga_wishbone import FPGAWB


def op_split(path):
	if path == "":
		return ("", "")
	r = path.rsplit("/", 1)
	if len(r) == 1:
		return ("", path)
	head = r[0]
	if not head:
		head = "/"
	return (head, r[1])

class FPGALED:
	def __init__(self):

		# load bitstream from SD card onto the FPGA
		with open(op_split(__file__)[0] + "/spi_skeleton.bin", "rb") as f:
			mch22.fpga_load(f.read())

		# create a wishbone command buffer
		self.c = FPGAWB()

		# LEDPWRR
		self.write(0x11, 0x00)
		# LEDPWRG
		self.write(0x12, 0x00)
		# LEDPWRB
		self.write(0x13, 0x00)
		# LEDDBCRR
		self.write(0x15, 0x00)
		# LEDDBCFR
		self.write(0x16, 0x00)
		# LEDDONR
		self.write(0x1A, 0x00)
		# LEDDOFR
		self.write(0x1B, 0x00)
		# LEDDBR
		self.write(0x19, 0xE0)
		# LEDDCR0
		self.write(0x18, 0x5D)

		# CSR
		self.write(0x00, 0x0E)

		self.c.exec()

	def write(self, address, data):
		self.c.queue_write(0, address << 2, data)

	def exec(self):
		self.c.exec()

	def led_color(self, r, g, b):
		# r and g swapped on mch2022 badge
		# LEDPWRR
		self.write(0x11, g)
		# LEDPWRG
		self.write(0x12, r)
		# LEDPWRB
		self.write(0x13, b)

	def led_state(self, on):
		# LEDDCR0
		if (on):
			self.write(0x18, 0xDD)
		else:
			self.write(0x18, 0x5D)

	def led_blink(self, enabled, on_time_ms, off_time_ms):
		# Disable EXE before doing any change */
		# LED_CSR_RGBLEDEN | LED_CSR_CURREN;
		self.write(0x00, 0x0C)

		# Load new config
		if (enabled):
			# LEDDONR
			self.write(0x1A, (on_time_ms >> 5) & 0xFF)
			# LEDDOFR
			self.write(0x1B, (off_time_ms >> 5) & 0xFF)
		else:
			# LEDDONR
			self.write(0x1A, 0)
			# LEDDOFR
			self.write(0x1B, 0)

		# Re-enable execution */
		# LED_CSR_LEDDEXE | LED_CSR_RGBLEDEN | LED_CSR_CURREN;
		self.write(0x00, 0x0E)

	def led_breathe(self, enabled, rise_time_ms, fall_time_ms):
		if (enabled):
			#led_regs->ip.bcrr = LEDDA_IP_BREATHE_ENABLE | LEDDA_IP_BREATHE_MODULATE | LEDDA_IP_BREATHE_TIME_MS(rise_time_ms);
			self.write(0x15, 0xA0 | ((rise_time_ms >> 7) & 0x0f))
			#led_regs->ip.bcfr = LEDDA_IP_BREATHE_ENABLE | LEDDA_IP_BREATHE_MODULATE | LEDDA_IP_BREATHE_TIME_MS(fall_time_ms);
			self.write(0x16, 0xA0 | ((fall_time_ms >> 7) & 0x0f))
		else:
			self.write(0x15, 0)
			self.write(0x16, 0)
