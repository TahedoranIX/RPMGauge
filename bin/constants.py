MINIMUM_RPM = 1200
MAXIMUM_RPM = 5500
WAIT_TIME = 1  # Sleep to read the values from obd and print in lcd.
WAIT_RESET_GAS = 3  # If wait time = 1 -> 3s.
WAIT_TURBOTIME = 60
PORT = "/dev/pts/2"
#PORT = "/dev/rfcomm99" # Puerto que asignado al OBD
FILE_HANDLER = '/home/pi/bin/mpg.dat'
#FILE_HANDLER = '/home/pi/Documents/rpm/mpg.dat'
DENSIDAD_G = 720  # Densidad de la gasolina g/L
ESTEQUIOMETRICA = 14.7  # Valor ideal de la mezcla estequiométrica
THROTTLE_MINIMUM = 7  # Min Throttle position
MINIMUM_SPEED = 5
