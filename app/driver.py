from app import app

class Driver():

	def __init__(self, form_data):
		self.name = form_data.name.data
		self.alias = form_data.alias.data if form_data.alias.data else None
		self.vehicle = form_data.vehicle.data if form_data.vehicle.data not in [None,'None','N/A',''] else None
		self.percentage = form_data.percentage.data
		self.forklift = form_data.forklift.data
		self.subhauler = False