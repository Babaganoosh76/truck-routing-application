from app import app, lm
from flask import Blueprint, request, make_response, redirect, render_template, url_for, flash, json, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from .forms import *
from .user import *
from .load import *
from .driver import *
from .equipment import *
from .excel import *
from .stats import *
from werkzeug.security import generate_password_hash
from bson import ObjectId
import requests
from os import listdir
from datetime import datetime, timedelta
from dateutil import parser
import pdfkit
from .ortools import *
import re
from .st_classes import *

GMAPS_KEY = os.environ.get('GMAPS_API')
DEPOT = 'Sacramento, CA, USA'

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(error,category='error')
			print((getattr(form, field).label.text,error))

def json_serialize(obj):
	if isinstance(obj, datetime):
		return obj.isoformat()
	if isinstance(obj, ObjectId):
		return str(obj)
	raise TypeError ('Type %s not serializable' % type(obj))

def api_request(arr):
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
	dret = []
	tret = []
	for i in range(len(arr)):
		s1 = arr[i][1].get_fmt_location()
		s2 = arr[:i] + arr[i+1:]
		s3 = '|'.join(s[1].get_fmt_location() for s in s2)
		res = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?key=' + GMAPS_KEY + '&origins=' + s1 + '&destinations=' + s3).json()
		drow = [STDistance(e['distance']['value']) for e in res['rows'][0]['elements']]
		drow.insert(i,0)
		dret.append(drow)
		trow = [STInterval(secs=e['duration']['value']) for e in res['rows'][0]['elements']]
		trow.insert(i,0)
		tret.append(trow)
	return dret, tret

splash = Blueprint('splash', __name__, template_folder='templates')
dashboard = Blueprint('dashboard', __name__, template_folder='templates', subdomain='dashboard')

@splash.route('/')
def splash_index():
	return render_template('splash-index.html')

@splash.route('/subhaul')
def splash_subhaul():
	return render_template('splash-subhaul.html')

@splash.route('/equipment')
def splash_equipment():
	return render_template('splash-equipment.html')

@splash.route('/get-gallery')
def get_gallery():
	gallery = None
	for path in ['/var/www/sundance/app/static/img/gallery','app/static/img/gallery']:
		try:
			gallery = listdir(path)
		except:
			pass
	return jsonify(gallery)

@app.route('/', subdomain='www')
def redirect_index():
	return redirect(url_for('splash.splash_index'))

@dashboard.route('/route', methods=['GET'])
def route():
	return render_template('route.html')

@dashboard.route('/route-result', methods=['GET', 'POST'])
def route_result():
	ROUTE_DEBUG = False
	if request.method == 'POST':
		# arrays of formatted strings
		ogn = [o for o in request.form.getlist('origin') if o]
		dst = [d for d in request.form.getlist('destination') if d]
		n = len(ogn)
		tms = [t for t in request.form.getlist('time')[:n]]
		pds = request.form.getlist('pd')[:n]
		cpm = float(request.form.get('cpm') or 0)

		#reject empty/uneven arrays
		if (not (ogn and dst) or n != len(dst)) and not ROUTE_DEBUG:
			flash('Please supply an equal number of origins and destinations')
			return redirect(url_for('dashboard.route'))

		# concatenated strings
		ogn_obj = [(i*2+1,STLocation(o, i*2+1)) for i,o in enumerate(ogn)]
		dst_obj = [(j*2+2,STLocation(d, j*2+2)) for j,d in enumerate(dst)]
		
		tms_obj = []
		tms_obj.append((0,MAX_TRAVEL_TIME))
		for i in range(n):
			if not tms[i]:
				tms_obj.append((0,MAX_TRAVEL_TIME))
				tms_obj.append((0,MAX_TRAVEL_TIME))
			elif (pds[i] == '0'):
				tms_obj.append((STTime(fmt=tms[i]),STTime(fmt=tms[i])))
				tms_obj.append((0,MAX_TRAVEL_TIME))
			elif (pds[i] == '1'):
				tms_obj.append((0,MAX_TRAVEL_TIME))
				tms_obj.append((STTime(fmt=tms[i]),STTime(fmt=tms[i])))

		veh = request.form.get('vehicles') or 1
		both = []
		both.append((0,STLocation(DEPOT, 0)))
		for i in range(len(ogn)):
			both.append(ogn_obj[i])
			both.append(dst_obj[i])
		
		# both_str = '|'.join(b[1].get_fmt_location() for b in both)
		# res = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?key=' + GMAPS_KEY + '&origins=' + both_str + '&destinations=' + both_str).json()
		# distances = [[STDistance(e['distance']['value']) for e in r['elements']] for r in res['rows']]
		# times = [[STInterval(secs=e['duration']['value']) for e in r['elements']] for r in res['rows']] # time in minutes

		distances, times = api_request(both)

		if ROUTE_DEBUG:
			data = test_data()
		else:
			data = create_data([], times, tms_obj, int(veh))

		routes, dropped = or_route(data) or []

		if routes:
			return render_template('route-result.html', locs=both, distances=distances, routes=routes, dropped=dropped, cpm=cpm)
		else:
			flash('No solution found')
			return redirect(url_for('dashboard.route'))

	return render_template('route-result.html')


@dashboard.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST' and form.validate_on_submit():
		user = app.config['USERS'].find_one({'_id': form.username.data})
		if user and User.validate_login(user['password'], form.password.data):
			user_obj = User(user['_id'])
			login_user(user_obj)
			flash('Logged in successfully!', category='success')
			return redirect(request.args.get('next') or url_for('dashboard'))
		flash('Wrong username or password!', category='error')
	return render_template('login.html', form=form)

@dashboard.route('/sign-up', methods=['GET', 'POST'])
def signUp():
	form = SignUpForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			user = app.config['USERS'].find_one({'_id': form.username.data})
			if user:
				flash('Username already taken', category='error')
			else:
				pass_hash = generate_password_hash(form.password.data)
				uid = app.config['USERS'].insert({'_id': form.username.data, 'password': pass_hash})
				user_obj = User(uid)
				login_user(user_obj)
				flash('Logged in successfully!', category='success')
				return redirect(request.args.get('next') or url_for('dashboard'))
		else:
			flash_errors(form)
	return render_template('sign-up.html', form=form)

@dashboard.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@dashboard.route('/')
# @login_required
def dashboard_index():
	return render_template('dashboard.html')


@dashboard.route('/statistics')
# @login_required
def statistics():
	return render_template('statistics.html')


@dashboard.route('/loads')
# @login_required
def loads():
	return render_template('loads.html')

@dashboard.route('/search-loads')
# @login_required
def search_loads():
	query = request.args.get('query')
	field = request.args.get('field')
	sort = 'date'
	limit = 50
	if field and query:
		loads = app.config['LOADS'].find({field:query}).collation({'locale':'en','strength':2}).sort(sort,-1).limit(limit)
	elif query:
		loads = app.config['LOADS'].find({'$text':{'$search':query,'$caseSensitive':False}}).sort(sort,-1).limit(limit)
	else:
		loads = app.config['LOADS'].find().sort(sort,-1).limit(limit)
	html = render_template('loads-row.html', loads=loads)
	return html

@dashboard.route('/l/<lid>')
# @login_required
def load_id(lid):
	load = app.config['LOADS'].find_one({'_id':ObjectId(lid)})
	if not load:
		return error_404('Load doesn\'t exist')
	driver = app.config['DRIVERS'].find_one({'alias':load['driver']})
	cpm = PRICE_PER_GALLON/MILES_PER_GALLON
	return render_template('load.html', load=load, driver=driver, cpm=cpm)

@dashboard.route('/l/<lid>/edit', methods=['GET','POST'])
# @login_required
def edit_load_id(lid):
	form1 = EditLoadForm()
	load = app.config['LOADS'].find_one({'_id':ObjectId(lid)})

	if not load:
		return error_404('Load doesn\'t exist')

	if request.method == 'POST':
		if form1.validate_on_submit():
			temp = Load(form_data=form1)
			app.config['LOADS'].update_one({'_id':ObjectId(lid)},{'$set':temp.__dict__})
		else:
			flash_errors(form1)
			return redirect(url_for('.edit_load_id', lid=load['_id']))
		return redirect(url_for('.load_id', lid=load['_id']))
		print('Edit user')

	# driver = app.config['DRIVERS'].find_one({'alias':load['driver']})
	return render_template('load-edit.html', form1=form1, load=load)


@dashboard.route('/drivers')
# @login_required
def drivers():
	form1 = EditDriverForm()
	drivers = app.config['DRIVERS'].find({})
	return render_template('drivers.html', form1=form1, drivers=drivers)

@dashboard.route('/add-driver', methods=['POST'])
# @login_required
def add_driver():
	form1 = AddDriverForm()
	if form1.validate_on_submit():
		nd = Driver(form1)
		ret = app.config['DRIVERS'].insert(nd.__dict__)
	else:
		flash_errors(form1)
	return redirect(url_for('.drivers'))

@dashboard.route('/edit-driver', methods=['POST'])
# @login_required
def edit_driver():
	form1 = EditDriverForm()
	if form1.validate_on_submit():
		temp = Driver(form1)
		driver = app.config['DRIVERS'].update_one({'_id':ObjectId(form1.id.data)},{'$set':temp.__dict__})
		return json.dumps({'success':'Driver updated'}), 200, {'ContentType':'application/json'}
	else:
		flash_errors(form1)
		return redirect(url_for('.drivers'))


@dashboard.route('/equipment')
# @login_required
def equipment():
	form1 = NewEquipmentForm()
	equipment = app.config['EQUIPMENT'].find({})
	return render_template('equipment.html', form1=form1, equipment=equipment)

@dashboard.route('/add-equipment', methods=['POST'])
# @login_required
def add_equipment():
	form1 = NewEquipmentForm()
	if form1.validate_on_submit():
		ne = Equipment(form1)
		app.config['EQUIPMENT'].insert(ne.__dict__)
	else:
		flash_errors(form1)
	return redirect(url_for('.equipment'))

@dashboard.route('/delete_all_loads', methods=['POST'])
# @login_required
def delete_all_loads():
	loads = app.config['LOADS'].remove()
	return redirect(url_for('.loads'))

@dashboard.route('/upload')
# @login_required
def upload():
	return render_template('upload.html')


@dashboard.route('/check-upload-dates')
# @login_required
def check_upload_dates():
	ret = {'invalid':[],'overwrite':[]}
	for sheet in request.args.getlist('sheets[]'):
		try:
			date = parser.parse(sheet)
		except ValueError:
			ret['invalid'].append(sheet)
			continue
		if list(app.config['LOADS'].find({'date':date})):
			ret['overwrite'].append(date.strftime('%B %-d'))
	return jsonify(ret)

@dashboard.route('/upload-dispatch', methods=['POST'])
# @login_required
def upload_dispatch():
	file = request.files.get('excel_file')
	if not file:
		return json.dumps({'error':'No valid file'}), 200, {'ContentType':'application/json'}
	try:
		wb = load_workbook(file, data_only=True)
	except IOError:
		return json.dumps({'error':'Error opening file'}), 200, {'ContentType':'application/json'}

	import_dispatch_sheets(wb, request.form.get('sheets').split(','))
	flash('Data successfully imported!')
	return json.dumps({'success':'File read'}), 200, {'ContentType':'application/json'}


@dashboard.route('/price-calculator')
# @login_required
def price_calculator():
	return render_template('price-calc.html')

@dashboard.route('/price-sheet')
# @login_required
def price_sheet():
	return render_template('price-sheet.html')

@dashboard.route('/create-price-sheet-xlsx', methods=['GET','POST'])
# @login_required
def create_price_sheet_xlsx():
	origin = request.args.get('origin')
	if not origin:
		return redirect(request.referrer)
	filename = '/download/price_sheet.xlsx'
	customer = request.args.get('customer') if request.args.get('customer') else 'CUSTOMER'
	destinations = '|'.join(a+', CA' for a in app.config['CITIES_TEMP']).replace(' ','+')
	data = []

	res = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+origin.replace(' ','+')+'&destinations='+destinations+'&key=AIzaSyAHJw-3P7bVLWl0hEyPObtDyHU2LzsiCak').json()
	for i,r in enumerate(res['rows'][0]['elements']):
		miles = r['distance']['value']*0.00062137 if r['status'] == 'OK' else None
		data.append({'city':app.config['CITIES_TEMP'][i],'miles':miles,'rate':0})

	create_price_sheet(origin,customer,data,filename)
	return send_file(filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', attachment_filename='Price_sheet_'+customer.replace(' ','_')+'.xlsx', as_attachment=True)


@dashboard.route('/payroll')
# @login_required
def payroll():
	return render_template('payroll.html')

@dashboard.route('/create-payroll-pdf', methods=['GET','POST'])
def create_payroll_pdf():
	try:
		date = datetime.strptime(request.args.get('date'), '%m/%d/%Y')
		date = date - timedelta(days=date.weekday())
	except:
		flash('Invalid date')
		return redirect(request.referrer)
	aliases = [a['alias'] for a in app.config['DRIVERS'].find()]
	loads = list(app.config['LOADS'].find({'driver':{'$in':aliases},'date':{'$gte':date,'$lt':date+timedelta(days=5)}}))
	html = render_template('payroll-pdf.html', date=date, drivers=app.config['DRIVERS'].find(), loads=loads)
	options = {
		'page-size': 'Letter',
		'orientation': 'Landscape',
		'encoding': 'UTF-8',
		'zoom': 0.9,
		'quiet': ''
	}
	filename = '/download/payroll.pdf'
	try:
		pdfkit.from_string(html, filename, options=options)
		return send_file(filename, mimetype='application/pdf', attachment_filename='payroll_'+date.strftime('%m-%d-%Y')+'.pdf', as_attachment=True)
	except Exception as e:
		print(e)
		flash('There was an error rendering the PDF')
		return redirect(request.referrer)

@dashboard.route('/create-payroll-xlsx', methods=['GET','POST'])
def create_payroll_xlsx():
	try:
		date = datetime.strptime(request.args.get('date'), '%m/%d/%Y')
		date = date - timedelta(days=date.weekday())
	except:
		flash('Invalid date')
		return redirect(request.referrer)

	filename = '/download/payroll.xlsx'
	create_payroll(date, filename)
	return send_file(filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', attachment_filename='payroll_'+date.strftime('%m-%d-%Y')+'.xlsx', as_attachment=True)

@app.errorhandler(404)
def error_404(e):
	if request.url.split('://')[-1].split('.')[0] == 'dashboard':
		return render_template('error-404.html'), 404
	else:
		return render_template('splash-error-404.html'), 404

@app.errorhandler(500)
def error_500(e):
	if request.url.split('://')[-1].split('.')[0] == 'dashboard':
		return render_template('error-500.html', error=e), 500
	else:
		return render_template('splash-error-500.html'), 500

@lm.user_loader
def load_user(username):
	u = app.config['USERS'].find_one({'_id': username})
	if not u:
		return None
	return User(u['_id'])

app.register_blueprint(splash)
app.register_blueprint(dashboard)
