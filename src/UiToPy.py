import os
os.system(command="pyuic5 -o ui_tiny.py tiny_uart.ui")

os.system(command="pyrcc5 ..\ico\ico.qrc -o ico_rc.py")