import serial

COM_PORT = 'COM4'
BAUD_RATE = 9600 
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout = 1)

if ser.is_open is True:
    print(ser.name, 'open successfully')

unit_dict = {'55':'kg',
             '56':'lb',
             '57':'g', 
             '58':'oz',
             '59':'N'}

try:
    while ser.read() != b'\r': ## wait to align
        continue

    while True:
        r = ser.read(16)
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
    ser.close()
    print("end")

