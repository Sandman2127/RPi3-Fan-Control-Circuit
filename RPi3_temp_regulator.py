#!/usr/bin/env python

#cat /sys/class/thermal/thermal_zone0/temp 

"""
Notes on the input circuit, We'll use a common emitter amplifier with an NPN 2222A by Fairchild:
	*The max output current of a gpio pin is 16 mA calculated here: http://www.thebox.myzen.co.uk/Raspberry/Understanding_Outputs.html
	*I'll feed the base of the transistor with ~8 mA using a 3.3V output and a 470 Ohm resistor. This will allow me to push the transistor halfway to saturation (15mA)
			*This is the best we can do with a 3.3v output and no additional amplifiers between and not overstressing the RPi3.
	* Given that I'm using a 9V battery to power the fan, I still cannot push the fan at its maximum capacity, bc it expects 12V source and up to 200 mA
	* Notes suggest it takes 0.7V across the base emitter junction to activate the transistor fully
"""


import RPi.GPIO as GPIO, time

cutoff = 37.0
cutoff_150perc = cutoff + (cutoff*0.5)
cutoff_200perc = cutoff + float(cutoff)


def GPIO_setup():

	GPIO.setmode(GPIO.BOARD)
	
	channels_out = [37]   # use as gpio output (37 is second up from bottom), use 39 bottom left as ground, 16 mamp max
	channels_in = []

	for channel in channels_out:
		GPIO.setup(channel, GPIO.OUT)   # Setup as an output channel
		GPIO.output(channel, GPIO.LOW)  # Set it to low
	
	#for channel in channels_in:
		#GPIO.setup(channel, GPIO.IN)

	# TODO can also do many channels at once
	# chan_list = [11,12]                             # also works with tuples
	# GPIO.output(chan_list, GPIO.LOW)                # sets all to GPIO.LOW
	# GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))   # sets first HIGH and second LOW


def finding_temp():

	with open("/sys/class/thermal/thermal_zone0/temp",'r') as f:
		lines = f.readlines()
		temp=str(lines[0][0:2]) + str(".")+ str(lines[0][2:])
		temp=float(temp)
		return temp

def run_fan(temp,pin):

	#Some background data:
	#GPIO.output(channel, state)
	#State can be 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
	
	if temp >= cutoff:
		#initiate fan running w/PWM type function: equivalent to 100% duty cycle on a 200ms cycle
		if temp >= cutoff_200perc:
			#toggle on constantly
			while True:
				GPIO.output(pin, GPIO.HIGH)

		elif temp >= cutoff_150perc:
			#toggle on for 0.1 sec off for 0.1 sec, equivalent to 50% duty cycle on a 200ms cycle
			while True:
				GPIO.output(pin, GPIO.HIGH)
				time.sleep(0.100)
				GPIO.output(pin, GPIO.LOW)
				time.sleep(0.100)
		else:
			#toggle on for 0.050 sec off for 0.150 sec, equivalent to 25% duty cycle on a 200ms cycle
			while True:
				GPIO.output(pin, GPIO.HIGH)
				time.sleep(0.075)
				GPIO.output(pin, GPIO.LOW)
				time.sleep(0.125)

	else:
		print "current temp: ", temp," is below the temperature cutoff: ",cutoff," therefore the fan remains off."
		pass



	



if '__name__' != '__main__':
	
	GPIO_setup()

	try:	
		while True:
			time.sleep(10)
			temp=finding_temp()
			#print temp
			pin = 37
			run_fan(temp,pin)

	except KeyboardInterrupt:
		GPIO.cleanup()
		print "Keyboard Interrupt, GPIO cleanup initiated"

