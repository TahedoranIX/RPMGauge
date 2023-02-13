# Constants info for cars.
MINIMUM_RPM = 1200
MAXIMUM_RPM = 5500
GASOLINE_DENSITY = 720  # (g/L)
GASOLINE_STOICHIOMETRIC = 14.7  # air/gasoline (grams)
DIESEL_DENSITY = 850  # (g/L)
DIESEL_STOICHIOMETRIC = 14.5  # air/diesel (grams)
THROTTLE_MINIMUM = 7  # Min Throttle position to count as throttleless
MINIMUM_SPEED = 5  # Min speed to consider stopped vehicle.

# main timeouts
WAIT_REFRESH_OBD = 1  # (s)
WAIT_REFRESH_PRINTHUB = 0.5  # (s)

# gas.py
TICK_RESET_GAS = WAIT_REFRESH_PRINTHUB
WAIT_RESET_GAS = (1/WAIT_REFRESH_PRINTHUB) * TICK_RESET_GAS * 3  # Last number total wait time (s)
OK_O2_VOL = 0.45  # (V)

# timeturbo.py
WAIT_TURBOTIME = 60  # (s)

# dtc.py
WAIT_CLEAN_CODES = WAIT_RESET_GAS
TICK_CLEAN_CODES = TICK_RESET_GAS

# Raspberry config
# PORT = "/dev/pts/2"
PORT = "/dev/rfcomm99"  # Port we listen for OBD