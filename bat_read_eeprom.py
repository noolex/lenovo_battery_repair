import smbus2
import sys

CMD_SET_EEPROM_ADDRESS = 0x09
CMD_READ_EEPROM_BLOCK = 0x0c
EEPROM_BLOCKSZ = 0x20
EEPROM_BASE_ADDR = 0x4000
EEPROM_BLOCK_COUNT = 64

def readBlock(bus, dev, cmd, sz):
    cmdmsg = smbus2.i2c_msg.write(dev, [cmd])
    msg = smbus2.i2c_msg.read(dev, sz + 1)
    bus.i2c_rdwr(cmdmsg, msg)
    data = list(msg)
    fulldata = data[1:]
    return fulldata

def readEepromBlock(bus, dev, blocknum):
    try:
        bus.write_word_data(dev, CMD_SET_EEPROM_ADDRESS, EEPROM_BASE_ADDR+(blocknum*32)); 
    except:
        print("Error write word data")
        return None
    data = readBlock(bus, dev, CMD_READ_EEPROM_BLOCK, 32)
    return data

if len(sys.argv) < 4:
    print("Error invalid arguments")
    print ("bat_read_eeprom [i2c-port-num] [i2c-hex-address] [file_name_to_write]")
    exit()

port = int(sys.argv[1])
dev = int(sys.argv[2], base=16)
name = sys.argv[3]

bus = smbus2.SMBus(port)

fout = open(name, "wb")
fullsz = 0

for i in range(0, EEPROM_BLOCK_COUNT):
    data = readEepromBlock(bus, dev, i)
    
    if data == None:
        print("Error read block", i)
        exit()
    if len(data) != EEPROM_BLOCKSZ:
        print("Error data len", len(data))
        exit()

    fullsz += len(data)
    fout.write(bytes(data))
    print("Read", i, "block") 
print("Writing", fullsz, "bytes to", name)
fout.close()
bus.close()
