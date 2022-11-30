from ECU_commands.ECU.coolant import Coolant
from ECU_commands.ECU.gas import Gas
from ECU_commands.ECU.rpm import RPMNumber, RPMGraph
from coche import Coche
from Interfaces.console import Console
from Interfaces.lcdsingle import LCDSingle
from lib.RotaryLibrary.encoder import Encoder
from menu import Menu
from obdsingle import OBDSingle

encoder = Encoder(20, 16, 21)
lcd = LCDSingle(26, 19, 13, 6, 5, 0)
console = Console()
obd = OBDSingle()


menu1 = Menu(RPMGraph(), RPMNumber())
menu2 = Menu(Gas(), Coolant())
menu3 = Menu(Gas(), Coolant())

nuevo = Coche(encoder, console, [menu1, menu2, menu3])

nuevo.mainLoop()
