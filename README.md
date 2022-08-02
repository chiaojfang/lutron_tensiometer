# Automatic Tensile Testing Machine using Lutron Force Gauge, Tensiometer and Stepper Motor

This is the control code used for the tensile testing machine in Lung-pan's lab. 
The setup consists of an automatic tensiometer drived by a stepper motor along with a Lutron force gauge.


## Using the tensile testing machine
The Arduino board on the test bench has the proper code uploaded already. 
To use the testing machine, simply hook up the motor driver with **5 - 12V power supply**, connect the Arduino and Force Gauge to the computer using the **USB hub** in the back, then run **tensile_test_interface.py**.

The **tensile_test_interface.py** would prompt relevent entries (filename for the csv, moving direction) for the specific tensile test, then machine will start performing the test automatically. 
**Remember to first zero the caliper.**
Once a fracture is detected (i.e. measured force is less than 0.5 x Max_Force), the machine will stop; then the program would prompt an input for the final value (position) on the caliper.

Default speed:  1 mm / min. To use different speed, add the following code to the python script:
~~~
mt_ser.write(bytes('t TIME\n','utf-8')) // Default: TIME = 60
~~~
where TIME is the amount of time to travel 1 mm distance.



## Supplementary files 

**Motor_control/Motor_control.ino**: the Arduino code used to control the stepper motor

**Lutron_Readout/lutron_interface.py**: Reads the measurement from the Lutron force gauge via the RS-232 serial interface (see force gauge manual for details). Sample rate ~3.4 Hz. 

**Laser_cut_files** contains the vector files of the laser-cut pieces on the device.
