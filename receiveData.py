from machine import UART
import time

buffer = bytearray(31)
uart = UART(1, 115200)  # uart1 tx-pin 4, rx-pin 5

while True:
    c = uart.read(1)
    if c and c[0] == 0x20:
        uart.readinto(buffer)
        checksum = 0xffff - 0x20
        for i in range(29):
            checksum -= buffer[i]
        if checksum == ((buffer[30] << 8) | buffer[29]):
            buffer[0] = 0x40
            ch1 = buffer[2] * 255 + buffer[1]
            ch2 = buffer[4] * 255 + buffer[3]
            ch3 = buffer[6] * 255 + buffer[5]
            ch4 = buffer[8] * 255 + buffer[7]
            ch5 = buffer[10] * 255 + buffer[9]
            ch6 = buffer[12] * 255 + buffer[11]
            print('ch  1-', ch1, '  2-', ch2, '  3-', ch3, '  4-', ch4, '  5-', ch5, '   6-', ch6)