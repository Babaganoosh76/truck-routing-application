from app import app
from flask import Blueprint, request, make_response, redirect, render_template, url_for, flash, json, jsonify, send_file
import requests
import re
import os

from .ortools import *
from .st_classes import *

GMAPS_KEY = os.getenv('GMAPS_API')
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

''' APP ROUTES '''
@app.route('/', methods=['GET'])
def index():
	return redirect(url_for('route'))

@app.route('/route', methods=['GET'])
def route():
	return render_template('route.html')

@app.route('/route-result', methods=['GET', 'POST'])
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
			return redirect(url_for('route'))

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