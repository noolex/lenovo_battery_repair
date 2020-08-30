# lenovo_battery_repair
Scripts for repair lenovo battery LNV-45N1175 from ThinkPad x230 on bq8030 controller

Connect battery to VGA (D-Sub):   
Battery connector: | + | + |      |SCL|SDA|unkn|GND|GND|    
VGA connector pins: 5-GND, 12-SDA, 15-SCL

Detecting i2c port using i2c-tools and get port number of VGA I2C device
```
$i2cdetect -l
```
Detect i2c-hex-address for connected battery. And find bat-address by connect-disconnect battery
```
$i2cdetect -y [portnum]
```
Get report about battery
```
$python3 bat_report.py [portnum] [i2c-hex-address]
```
Hack bat for access to eeprom
```
$python3 bat_hack.py [portnum] [i2c-hex-address]
```
Read eeprom
```
$python3 bat_read_eeprom.py [portnum] [i2c-hex-address] [eeprom-filename]
```
Correct eeprom, I don't know how.... See below

Write eeprom
```
$python3 bat_write_eeprom.py [portnum] [i2c-hex-address] [eeprom-filename]
```
After that don't forget start battery cntroller
```
$python3 bat_exec.py [portnum] [i2c-hex-address]
```
### Thanks for Viktor:
http://www.karosium.com/2016/08/hacking-bq8030-with-sanyo-firmware.html    
https://github.com/karosium/smbusb

## Correct EEPROM file

For **my** battery I correct eeprom:
1) reset Charge Cycles:   
[0x500-0x501] set 0x0000   
[0x600-0x601] set 0x0000  
3) [0x5A8] change 0x80 -> 0x00
2) [0x668] change 0x80 -> 0x00



