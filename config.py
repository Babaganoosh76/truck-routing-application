import os
from pymongo import MongoClient

# SERVER_NAME = 'sundancetransportinc.com'
SERVER_NAME = 'local.com:8888'
SECRET_KEY = 'supersecretkey'
DB_NAME = 'sundance'
DATABASE = MongoClient()[DB_NAME]
USERS = DATABASE.users
DRIVERS = DATABASE.drivers
EQUIPMENT = DATABASE.equipment
LOADS = DATABASE.loads
DEBUG = True

DRIVERS_TEMP = ['Craig', 'Matt', 'Dave', 'Cande', 'Bryan']
CITIES_TEMP = ['Antioch','Arbuckle','Brentwood','Chico','Citrus Heights','Concord','Cupertino','Danville','Daly City','Diablo','Dixon','Dublin','Elk Grove','El Dorado Hills','Fairfield','Folsom','Fremont','Fresno','Gilroy','Hayward','Hollister','Lincoln','Livermore','Lodi','Los Banos','Los Gatos','Oakland','Oakley','Orinda','Palo Alto','Petaluma','Manteca','Merced','Milpitas','Morgan Hill','Mountain House','Mountain View','Napa','Newark','Rancho Cordova','Redwood City','Richmond','Riverbank','Roseville','Sacramento','San Francisco','San Mateo','San Jose','San Rafael','San Ramon','Santa Clara','Santa Rosa','Sunnyvale','Tracy','Union City','Vacaville','Vallejo','Woodland','Winters','Yuba City']
