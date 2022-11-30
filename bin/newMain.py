from ECU_commands.ECU.coolant import Coolant
from ECU_commands.ECU.gas import Gas
from ECU_commands.ECU.rpm import RPMNumber
from coche import Coche
from console import Console
from lib.LCDLibrary.lcdLibrary import LCD
from lib.RotaryLibrary.encoder import Encoder
from menu import Menu

encoder = Encoder(20, 16, 21)
lcd = LCD(0, 5, 26, 19, 13, 6)
console = Console()

menu1 = Menu(RPMNumber(), Coolant())
menu2 = Menu(Gas(), Coolant())
menu3 = Menu(Gas(), Coolant())

nuevo = Coche(encoder, lcd, [menu1, menu2, menu3])

nuevo.print(menu1.print())
