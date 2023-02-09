# Constants info for cars.
MINIMUM_RPM = 1200
MAXIMUM_RPM = 5500
GASOLINE_DENSITY = 720  # g/L
GASOLINE_STOICHIOMETRIC = 14.7  # air/gasoline (grams)
DIESEL_DENSITY = 850  # g/L
DIESEL_STOICHIOMETRIC = 14.5  # air/diesel (grams)
THROTTLE_MINIMUM = 7  # Min Throttle position to count as throttleless
MINIMUM_SPEED = 5  # Min speed to consider stopped vehicle.

# main timeouts
WAIT_REFRESH_OBD = 1
WAIT_REFRESH_PRINTHUB = 0.25

# gas.py
TICK_RESET_GAS = WAIT_REFRESH_PRINTHUB
WAIT_RESET_GAS = 12 * TICK_RESET_GAS
KM_TO_SAVE_MPG = 0.5
MAX_O2_VOL = 0.8
MIN_O2_VOL = 0.1
OK_O2_VOL = 0.45

# timeturbo.py
WAIT_TURBOTIME = 60  # Seconds

# dtc.py
WAIT_CLEAN_CODES = WAIT_RESET_GAS
TICK_CLEAN_CODES = WAIT_REFRESH_PRINTHUB

# Raspberry config
# PORT = "/dev/pts/2"
PORT = "/dev/rfcomm99"  # Port we listen for OBD