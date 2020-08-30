import smbus2
import sys
from time import sleep

CMD_WRITE_EEPROM_BLOCK = 0x10
CMD_ERASE_EEPROM_FLASH = 0x12
DATA_ERASE_CONFIRM = 0x83DE

def writeEepromBlock(bus, dev, blocknum, data):
    wrd = [CMD_WRITE_EEPROM_BLOCK, len(data) + 1, blocknum] + data
    msg = smbus2.i2c_msg.write(dev, wrd)
    bus.i2c_rdwr(msg)
    print("Write block", blocknum)
    sleep(0.5)
    return len(data)

if len(sys.argv) < 4:
    print("Error invalid arguments")
    print ("python3 bat_write_eeprom.py [i2c-port-num] [i2c-hex-address] [file_name_to_write]")
    exit()

port = int(sys.argv[1])
dev = int(sys.argv[2], base=16)
name = sys.argv[3]

bus = smbus2.SMBus(port)

fin = open(name, "rb")
if fin == None:
    print("File not found")
    exit(0)

print("Erase eeprom...", end='')
bus.write_word_data(dev, CMD_ERASE_EEPROM_FLASH,DATA_ERASE_CONFIRM);
sleep(1)
print("OK")

fullsz = 0
for i in range(0, 62):
    data = fin.read(32)
    fullsz += writeEepromBlock(bus, dev, i, list(data))

print("Writing", fullsz, "bytes")
fin.close()
bus.close()
