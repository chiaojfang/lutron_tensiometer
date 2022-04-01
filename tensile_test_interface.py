import serial
import time 
from datetime import datetime

T = 60 # time per 1 mm

BAUD_RATE = 9600 

LOADCELL_COM_PORT = 'COM4'
lc_ser = serial.Serial(LOADCELL_COM_PORT, BAUD_RATE, timeout = 1)

MOTOR_COM_PORT = 'COM3'
mt_ser = serial.Serial(MOTOR_COM_PORT, BAUD_RATE, timeout = 1)


if lc_ser.is_open is True:
    print(lc_ser.name, 'load cell port opened successfully')

if mt_ser.is_open is True:
    print(mt_ser.name, 'motor controller port opened successfully')

unit_dict = {'55':'kg',
             '56':'lb',
             '57':'g', 
             '58':'oz',
             '59':'N'}

print(mt_ser.readline().decode()) ## Make sure motor control ready

while lc_ser.read() != b'\r': ## wait to align loadcell readout data
    continue

filename = './data/' + input('Filename: ') + '.csv'
f = open(filename, 'a')
f.write(datetime.now().strftime('%m/%d/%Y,%H:%M:%S'))


r = input('[u]p or [d]own: ')
print(r)
if r == 'u':
    ret = mt_ser.write(bytes('u\n','utf-8'))
    f.write('\nDirection: , UP\n')
elif r == 'd':
    ret = mt_ser.write(bytes('d\n','utf-8'))
    f.write('\nDirection: , DOWN\n')
time.sleep(0.05)
print(mt_ser.readline().decode()) 

ret = mt_ser.write(bytes('t'+str(T)+'\n','utf-8'))
print('t'+str(T)+'\n')
time.sleep(0.05)
print(mt_ser.readline().decode()) 

print("Start testing ...")
f.write('START\n')
f.write('Time (ns), Distance (mm), Force (N)\n')

try:
    ret = mt_ser.write(bytes('s\n','utf-8'))
    t_start = time.time_ns()
    max_force = 0

    while True:
        r = lc_ser.read(16)
        polarity = 1 - 2 * int(chr(r[5]))
        decimal = 10 ** (-1 * int(chr(r[6])))
        unit = unit_dict[r[3:5].decode()]
        value = int(r[7:16].decode())
        abs_force = value * decimal
        print(abs_force, unit)
        
        distance = (time.time_ns() - t_start) / (T * 1000000000)

        f.write(str(time.time_ns())+','+str(distance)+','+str(abs_force)+'\n')

        if abs_force < max_force / 2 - 0.1:
            break
        else:
            max_force = max(max_force, abs_force)

    ret = mt_ser.write(bytes('p\n','utf-8'))

except KeyboardInterrupt:
    ret = mt_ser.write(bytes('p\n','utf-8'))
    lc_ser.close()
    print("Exited with keyboard interrupt")

else:
    r = input("Position: ")
    f.write('END, Position:, '+r+'\n')
    f.close()
    for i in range(3):
        print("\a")
        time.sleep(1)
    print("Finished")


exit()
########################################################################

try:
    while lc_ser.read() != b'\r': ## wait to align loadcell readout data
        continue

    while True:
        r = lc_ser.read(16)
        polarity = 1 - 2 * int(chr(r[5]))
        decimal = 10 ** (-1 * int(chr(r[6])))
        unit = unit_dict[r[3:5].decode()]
        value = int(r[7:16].decode())
        ## print(value)
        ## print('unit:', decimal, unit)
        ## print('polarity:', polarity)

        force = value * polarity * decimal
        print(force, unit)

except KeyboardInterrupt:
    lc_ser.close()
    print("end")

