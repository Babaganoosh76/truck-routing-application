from app import app
from datetime import datetime

class Load():

  def __init__(self, row_data=None, date=None, subhaul=None, other_data=None, form_data=None):
    reject_fields = [None,'None','N/A','','[]',0]
    if form_data:
      self.driver = form_data.driver.data if form_data.driver.data not in reject_fields else None
      self.vehicle = form_data.vehicle.data if form_data.vehicle.data not in reject_fields else None
      self.hand_tag = form_data.hand_tag.data if form_data.hand_tag.data not in reject_fields else None
      self.origin = form_data.origin.data if form_data.origin.data not in reject_fields else None
      self.customer = form_data.customer.data if form_data.customer.data not in reject_fields else None
      self.po_num = form_data.po_num.data if form_data.po_num.data not in reject_fields else None
      self.destination = form_data.destination.data if form_data.destination.data not in reject_fields else None
      self.date = datetime.strptime(form_data.date.data, '%m/%d/%Y') if form_data.date.data else None
      self.forklift = form_data.forklift.data if form_data.forklift.data else 0
      self.amount_paid = form_data.amount_paid.data if form_data.amount_paid.data else 0
      self.amount_billed = form_data.amount_billed.data if form_data.amount_billed.data else 0
      self.subhaul = form_data.subhaul.data
      self.preload = form_data.preload.data
      self.other = form_data.other.data.split('\r\n') if form_data.other.data else None

    else:
      self.driver = row_data[0].value if row_data[0].value else None
      do = app.config['DRIVERS'].find_one({'alias':row_data[0].value})
      if do:
        # self.driver = driver['name']
        self.vehicle = do['vehicle']
      else:
        # self.driver = row_data[0].value if row_data[0].value else None
        self.vehicle = None
      self.hand_tag = row_data[1].value if row_data[1].value else None
      self.origin = row_data[2].value if row_data[2].value else None
      self.customer = row_data[3].value if row_data[3].value else None
      self.po_num = row_data[4].value if row_data[4].value else None
      self.destination = row_data[5].value if row_data[5].value else None
      self.date = date
      self.forklift = row_data[6].value if row_data[6].value else 0
      self.subhaul = subhaul
      if subhaul:
        self.amount_paid = row_data[7].value if row_data[7].value else 0
        self.amount_billed = row_data[8].value if row_data[8].value else 0
      else:
        self.amount_paid = 0
        self.amount_billed = row_data[7].value if row_data[7].value else 0
      self.preload = False
      self.other = [other_data] if other_data else []

  def set_other(self, other_data):
    for cell in other_data:
      if cell.value:
        self.other.append(cell.value)

  # def __init__(self, driver, hand_tag, pick_up_location, customer, po_num, destination, forklift, amount_billed, other=[]):
  #   self.driver = driver
  #   self.hand_tag = hand_tag
  #   self.pick_up_location = pick_up_location
  #   self.customer = customer
  #   self.po_num = po_num
  #   self.destination = destination
  #   self.forklift = forklift
  #   self.amount_billed = amount_billed
  #   self.other = other
