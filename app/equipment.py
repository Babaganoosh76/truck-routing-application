from app import app

class Equipment():

	def __init__(self, form_data):
		self.id = form_data.id.data
		self.mileage = form_data.mileage.data
		self.notes = form_data.notes.data if form_data.notes.data else None