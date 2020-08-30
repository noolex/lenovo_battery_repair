# lenovo_battery_repair
Scripts for repair lenovo battery LNV-45N1175 from ThinkPad x230

Connect battery to VGA (D-Sub):
Battery connector: | + | + |      |SCL|SDA|unkn|GND|GND|
VGA connector pins: 5-GND, 12-SDA, 15-SCL

Detecting i2c port
'''
i2cdetect -l
'''
