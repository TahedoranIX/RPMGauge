from ECU_commands.ECU.coolant import Coolant
from ECU_commands.ECU.errorScreen import DtcScreen
from ECU_commands.ECU.gas import Gas
from ECU_commands.ECU.rpm import RPMNumber, RPMGraph
from ECU_commands.ECU.timeturbo import TimeTurbo
from ECU_commands.ecu import ECU
from coche import Coche
from Interfaces.console import Console
from Interfaces.lcdsingle import LCDSingle
from lib.RotaryLibrary.encoder import Encoder
from menu import Menu
from obdsingle import OBDSingle


encoder = Encoder(13, 19, 6)  # Raspberry casa
lcd = LCDSingle(d4=26,d5=19,d6=13,d7=6,en=5,rs=0)  # Raspberry casa

# encoder = Encoder(20, 16, 21)  # Raspberry coche
# lcd = LCDSingle(d4=23, d5=18, d6=15, d7=14, en=24, rs=25)  # Raspberry coche
console = Console()
obd = OBDSingle()

menu1 = Menu(Coolant(), RPMNumber())
menu2 = Menu(RPMGraph(), Gas())
menu3 = Menu(Coolant(), TimeTurbo())
menu4 = Menu(DtcScreen())

main = Coche(encoder, lcd, [menu1, menu2, menu3, menu4])
main.mainLoop()
