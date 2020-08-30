# lenovo_battery_repair
Scripts for repair lenovo battery LNV-45N1175 from ThinkPad x230

Connect battery to VGA (D-Sub):
Battery connector: | + | + |      |SCL|SDA|unkn|GND|GND|

VGA connector pins: 5-GND, 12-SDA, 15-SCL

Detecting i2c port using i2c-tools
```
$i2cdetect -l
```
Detect i2c-hex-address for connected battery. And find bat-address by connect-disconnect battery
```
$i2cdetect -y 2
```
Get report about battery
```
$python3 bat_report.py 2 0x0b
```
Hack bat for access to eeprom
```
$python3 bat_hack.py 2 0x0b
```
Read eeprom
```
$python3 bat_read_eeprom.py 2 0x0b eeprom.bin
```
Write eeprom
```
$python3 bat_write_eeprom.py 2 0x0b eeprom.bin
```
After that don't forget start battery cntroller
```
$python3 bat_exec.py 2 0x0b
```


