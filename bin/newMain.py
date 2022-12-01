from ECU_commands.ECU.coolant import Coolant
from ECU_commands.ECU.gas import Gas
from ECU_commands.ECU.rpm import RPMNumber, RPMGraph
from ECU_commands.ECU.timeturbo import TimeTurbo
from coche import Coche
from Interfaces.console import Console
from Interfaces.lcdsingle import LCDSingle
from lib.RotaryLibrary.encoder import Encoder
from menu import Menu
from obdsingle import OBDSingle

encoder = Encoder(20, 16, 21)
lcd = LCDSingle(26, 19, 13, 6, 5, 0)
console = Console()
obd = OBDSingle(console)


menu1 = Menu(Coolant(), RPMNumber())
menu2 = Menu(Gas(), RPMNumber())
menu3 = Menu(Coolant(), TimeTurbo())

main = Coche(encoder, lcd, [menu1, menu2, menu3])
main.mainLoop()
