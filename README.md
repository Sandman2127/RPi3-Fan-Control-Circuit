# Raspberry Pi3 Fan Control Software & Circuit

### Software Design:

This script was intended as an automated Fan Control system for the Raspberry Pi 3. It is very experimental so results may vary dependent on configuration. It is reasonable to assume that this controller will function well with a recent version of RPi3 and the designation of the correct position of the python2 environment in your ~/.bashrc (see usage).

The program senses temperature of the processor by reading the constantly updated file /sys/class/thermal/thermal_zone0/temp in short time intervals.

### Circuit Details:

![Fan Circuit](https://sandman2127.github.io/images/FAN_RPi_circuit_sim.png)

[Circuit Details and Simulation](https://sandman2127.github.io/design/Pi_Fan_Proj/)

### Circuit Description:
- The circuit is a common-emitter amplifier with an NPN 2222A by Fairchild:
- We feed the base of the transistor with ~8 mA using a 3.3V output from the [RPi3 pin 37](https://docs.microsoft.com/en-us/windows/iot-core/learn-about-hardware/pinmappings/pinmappingsrpi) through a 470 Ohm resistor. This setup pushes the transistor base current flow (3.3V/470Ohm = ~7 mA) halfway to RPi3's pin saturation (16 mA)
- The max output current of a gpio pin is 16 mA calculated here: http://www.thebox.myzen.co.uk/Raspberry/Understanding_Outputs.html
- My fan can accept up to a 12V power source across the leads forcing a current flow of up to 200 mA 

### Usage
To run automatically add these lines to the bottom of your ~/.bashrc
```
# use python2.7:
/path/to/RPi.GPIO/python /path/to/RPi3_temp_control/RPi3_temp_regulator.py & 
```




