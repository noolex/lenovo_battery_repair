import smbus2 
import sys
import struct

def getstring(b) :
    i = 0
    for k in b:
        if k == 0:
            break
        else:
            i += 1
    return bytes(b[1:i]).decode("utf8")

def rd_string(bus, devaddr, cmd):
    len = 1
    str = "None"
    try:
        len = bus.read_byte_data(devaddr, cmd)
    except:
        return "Error read len"
    if len:
        try:
            data = bus.read_i2c_block_data(devaddr, cmd, len+1)
            str = getstring(data)
        except:
            return "Error read block"
    return str

def rd_word(bus, devaddr, cmd):
    str = "None"
    try:
        val = bus.read_word_data(devaddr, cmd)
        str = "0x{0:x}".format(val)
    except:
        return "Error read word"
    return str

def rd_word_val(bus, devaddr, cmd):
    val = -1
    try:
        val = bus.read_word_data(devaddr, cmd)
    except:
        val = -1
    return val

# ==== main scketch =====

if len(sys.argv) < 3:
    print("Error invalid arguments")
    print ("python3 bat_report [i2c-port-num] [i2c-hex-address]")
    exit()

port = int(sys.argv[1])
dev = int(sys.argv[2], base=16)

bus = smbus2.SMBus(port)

#Todo enable PEC
#SMBEnablePEC(1);
print("-------------------------------------------------\n");
print("Manufacturer Name:", rd_string(bus, dev, 0x20));
print("Device Name:", rd_string(bus, dev, 0x21));
print("Device Chemistry:", rd_string(bus, dev, 0x22));
print("Serial Number:", rd_word(bus, dev, 0x1c))

val = rd_word_val(bus, dev, 0x1b);
print("Manufacture Date:", end=' ') 
if val >= 0:
    print("{:d}.{:02d}.{:02d}".format(1980+(val>>9), val>>5&0xF, val&0x1F))
else: 
    print("Error")

print("Manufacturer Access:", rd_word(bus, dev, 0x00));
print("Remaining Capacity Alarm:", rd_word_val(bus, dev, 0x01),"mAh(/10mWh)")
print("Remaining Time Alarm:", rd_word_val(bus, dev, 0x02), "min")
print("Battery Mode:",rd_word(bus, dev, 0x03))
print("At Rate:", rd_word_val(bus, dev, 0x04), "mAh(/10mWh)")
print("At Rate Time To Full:", rd_word_val(bus, dev, 0x05), "min")
print("At Rate Time To Empty:", rd_word_val(bus, dev, 0x06), "min")
print("At Rate OK:", rd_word_val(bus, dev, 0x07))

t = float(rd_word_val(bus, dev, 0x08))
print("Temperature:", t*0.1-273.15,"degC")

print("Voltage:", rd_word_val(bus, dev, 0x09), "mV")
print("Current:", rd_word_val(bus, dev, 0x0a), "mA")
print("Average Current:", rd_word_val(bus, dev, 0x0b), "mA")
print("Max Error:", rd_word_val(bus, dev, 0x0c), "%")
print("Relative State Of Charge:", rd_word_val(bus, dev, 0x0d),"%")
print("Absolute State Of Charge:", rd_word_val(bus, dev, 0x0e), "%")
print("Remaining Capacity:", rd_word_val(bus, dev, 0x0f), "mAh(/10mWh)")
print("Full Charge Capacity:", rd_word_val(bus, dev, 0x10), "mAh(/10mWh)")
print("Run Time To Empty:", rd_word_val(bus, dev, 0x11), "min")
print("Average Time To Empty:", rd_word_val(bus, dev, 0x12), "min")
print("Average Time To Full:", rd_word_val(bus, dev, 0x13), "min")
print("Charging Current:", rd_word_val(bus, dev, 0x14), "mA")
print("Charging Voltage:", rd_word_val(bus, dev, 0x15), "mV")
print("Battery Status:", rd_word(bus, dev, 0x16))
print("Cycle Count:", rd_word_val(bus, dev, 0x17))

print("Manufacturer Data: ")
#get lenovo data
len = bus.read_byte_data(dev, 0x23)
data = bus.read_i2c_block_data(dev, 0x23, len+1)
if len == 14:
    cells = struct.unpack("<4x4H2x", bytes(data[1:]))
    print("Cells voltage:", cells[0], cells[1], cells[2], cells[3], "mV")
else:
    print(data)
    