import smbus2
import sys

if len(sys.argv) < 3:
    print("Error invalid arguments")
    print ("bat_exec [i2c-port-num] [i2c-hex-address]")
    exit()

port = int(sys.argv[1])
dev = int(sys.argv[2], base=16)

bus = smbus2.SMBus(port)

bus.write_byte(dev, 0x08)
print("Start OK.")
bus.close()