from loggerinterface import LoggerInterface
from ECU_commands.ECU.coolant import Coolant
from ECU_commands.ECU.dtc import DtcScreen
from ECU_commands.ECU.gas import Gas
from ECU_commands.ECU.rpm import RPMGraph, RPMNumber
from ECU_commands.ECU.timeturbo import TimeTurbo
from car import Car
from Interfaces.console import Console
from Interfaces.lcdhandler import LCDHandler
from lib.RotaryLibrary.encoder import Encoder
from menu import Menu
from Interfaces.obdhandler import OBDHandler

encoder = Encoder(13, 19, 6)  # Raspberry casa
lcd = LCDHandler(d4=26, d5=19, d6=13, d7=6, en=5, rs=0)  # Raspberry casa

# encoder = Encoder(20, 16, 21)  # Raspberry coche
# lcd = LCDHandler(d4=23, d5=18, d6=15, d7=14, en=24, rs=25)  # Raspberry coche

LoggerInterface()

console = Console()
obd = OBDHandler(console)

menu1 = Menu([RPMNumber(), Coolant()])
menu2 = Menu([RPMGraph(), Gas()])
menu3 = Menu([Coolant(), TimeTurbo()])
menu4 = Menu([DtcScreen()])

main = Car(encoder, console, [menu1, menu2, menu3, menu4])
# main.dieselCar()
main.mainLoop()
