import smbus2
import sys

if len(sys.argv) < 3:
    print("Error invalid arguments")
    print ("python3 bat_hack.py [i2c-port-num] [i2c-hex-address]")
    exit()

port = int(sys.argv[1])
dev = int(sys.argv[2], base=16)

bus = smbus2.SMBus(port)

bus.write_word_data(dev, 0x71, 0x0214)
print("Send 0x0214 -> 0x71")
val = bus.read_word_data(dev, 0x73)
print("Value from 0x73", val)
val = 0x10000 - val
print("First pswd:", val)
bus.write_word_data(dev, 0x71, val)
print("Send", val, "->0x71")
bus.write_word_data(dev, 0x70, 0x0517)
print("Send 0x0517->0x70")
print("Hacking Ok")
bus.close()