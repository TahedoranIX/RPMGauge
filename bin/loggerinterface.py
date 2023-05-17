import logging
from os import path

from obd import obd

from constants import GENERAL


class LoggerInterface:
	file = str(path.realpath(path.dirname(__file__)) + "/resources/logger.log")

	@classmethod
	def __init__(cls):
		fileH = logging.FileHandler(cls.file)
		fileH.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(message)s"))
		obd.logger.addHandler(fileH)
		# obd.logger.setLevel(obd.logging.DEBUG)

		logger = logging.getLogger(GENERAL)
		logger.setLevel(logging.DEBUG)
		console_handler = logging.StreamHandler()
		console_handler.setLevel(logging.DEBUG)
		console_handler.setFormatter(logging.Formatter("%(name)s - %(message)s"))
		file_handler = logging.FileHandler(cls.file)
		file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))
		logger.addHandler(console_handler)
		logger.addHandler(file_handler)
