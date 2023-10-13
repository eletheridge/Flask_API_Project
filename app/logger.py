from datetime import datetime


class Logger:
	def __init__(self, filename='/logs/app.log', app_name=__name__):
		self.filename = filename
		self.app_name = app_name

	def write(self, level='INFO', message='No message provided'):
		with open(self.filename, 'a') as file:
			file.write(f'{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} -- {self.app_name} -- {level} -- {message}\n')