from ECU_commands.ecu import ECU
from Observers.observable import Observable


class Coolant(ECU):
	def __init__(self) -> None:
		super().__init__()
		self.coolOBD = 0

	def update(self, commands: Observable):
		self.coolOBD = commands["coolant"]

	def print(self):
		return 'Temp: ' + str(self.coolOBD) + ' C'
