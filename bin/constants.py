MINIMUM_RPM = 1200
MAXIMUM_RPM = 5500

KM_TO_SAVE_MPG = 0.05
WAIT_TIME_OBD = 1  # Sleep time to refresh obd values
WAIT_TIME_PRINTHUB = WAIT_TIME_OBD / 2
WAIT_RESET_GAS = 6 * WAIT_TIME_PRINTHUB  # If wait_time_lcd = 0.5 -> 3s.
WAIT_TURBOTIME = 60  # Time to let turbo cooldown once you stopped.
# PORT = "/dev/pts/2"
PORT = "/dev/rfcomm99" # Puerto que asignado al OBD
FILE_HANDLER = '/home/pi/bin/mpg.dat'
# FILE_HANDLER = '/home/pi/Documents/rpm/mpg.dat'
DENSIDAD_G = 720  # Densidad de la gasolina g/L
ESTEQUIOMETRICA = 14.7  # Valor ideal de la mezcla estequiométrica
THROTTLE_MINIMUM = 7  # Min Throttle position to count as throttleless
MINIMUM_SPEED = 5  # Min speed to consider stopped vehicle.
