from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from .st_classes import STTime, STRoute

MAX_TRAVEL_DISTANCE = 1609*1000 #1000 miles
MAX_WAIT_TIME = 15 #30 mins
MAX_TRAVEL_TIME = 60*10 #10 hours
VEHICLE_CAPACITY = 100
VEHICLE_LOAD_TIME = 30

''' Generates data object '''
def create_data(dm, tm, tw, v):
	n = len(tm)
	assert (n%2 != 0)
	data = {}
	data['distance_matrix'] = []
	data['time_matrix'] = tm
	# data['time_windows'] = [(STTime(300),STTime(MAX_TRAVEL_TIME)) for i in range(n)]
	data['time_windows'] = tw
	data['pickups_deliveries'] = [(i*2+1, i*2+2) for i in range(int(n/2))]
	data['demands'] = [0] + [VEHICLE_CAPACITY*((-1)**i) for i in range(n-1)]
	data['capacities'] = [VEHICLE_CAPACITY for i in range(v)]
	data['num_vehicles'] = v
	data['depot'] = 0
	data['vehicle_load_time'] = VEHICLE_LOAD_TIME
	return data

''' Generates test data object '''
def test_data():
	data = {}
	# data['distance_matrix'] = [
	# 	[0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875],
	# 	[2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589],
	# 	[713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262],
	# 	[1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466],
	# 	[1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796],
	# 	[1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547],
	# 	[2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724],
	# 	[213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038],
	# 	[2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744],
	# 	[875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0]
	# ]
	# data['distance_matrix'] = []
	data['time_matrix'] = [
		[0, 6, 9, 8, 7, 3, 6, 2, 3, 2],
		[6, 0, 8, 3, 2, 6, 8, 4, 8, 8],
		[9, 8, 0, 11, 10, 6, 3, 9, 5, 8],
		[8, 3, 11, 0, 1, 7, 10, 6, 10, 10],
		[7, 2, 10, 1, 0, 6, 9, 4, 8, 9],
		[3, 6, 6, 7, 6, 0, 2, 3, 2, 2],
		[6, 8, 3, 10, 9, 2, 0, 6, 2, 5],
		[2, 4, 9, 6, 4, 3, 6, 0, 4, 4],
		[3, 8, 5, 10, 8, 2, 2, 4, 0, 3],
		[2, 8, 8, 10, 9, 2, 5, 4, 3, 0]
	]
	'''
	data['time_windows'] = [
		(0, 5),  # depot
		(7, 12),  # 1
		(10, 15),  # 2
		(16, 18),  # 3
		(10, 13),  # 4
		(0, 5),  # 5
		(5, 10),  # 6
		(0, 4),  # 7
		(5, 10),  # 8
		(0, 3)  # 9
	]
	'''
	data['time_windows'] = [
		(0,6000),(0,6000),(0,6000),(0,6000),(0,6000),(0,6000),(0,6000),(0,6000),(0,6000),(0,6000)
	]
	data['pickups_deliveries'] = [
		(1,2),
		(3,4),
		(5,6),
		(7,8),
	]
	data['demands'] = [0,100,-100,100,-100,100,-100,100,-100,100]
	data['capacities'] = [100,100,100,100]
	data['num_vehicles'] = 4
	data['depot'] = 0
	return data

''' Generates optimized route based on data '''
def or_route(data):
	assert data['num_vehicles'] <= len(data['capacities'])
	assert len(data['time_matrix']) <= len(data['time_windows'])

	# Create the routing index manager
	manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']), data['num_vehicles'], data['depot'])

	# Create Routing Model
	routing = pywrapcp.RoutingModel(manager)

	def distance_callback(from_index, to_index):
		from_node = manager.IndexToNode(from_index)
		to_node = manager.IndexToNode(to_index)
		return data['distance_matrix'][from_node][to_node]

	def time_callback(from_index, to_index):
		from_node = manager.IndexToNode(from_index)
		to_node = manager.IndexToNode(to_index)
		return data['time_matrix'][from_node][to_node]

	def demand_callback(from_index):
		from_node = manager.IndexToNode(from_index)
		return data['demands'][from_node]


	''' CONSTRAINTS '''
	# Add distance constraint.
	# distance_callback_index = routing.RegisterTransitCallback(distance_callback)
	# routing.AddDimension(distance_callback_index, 0, MAX_TRAVEL_DISTANCE, True, 'Distance')
	# distance_dimension = routing.GetDimensionOrDie('Distance')
	# distance_dimension.SetGlobalSpanCostCoefficient(100)

	# Add time constraint
	time_callback_index = routing.RegisterTransitCallback(time_callback)
	routing.AddDimension(time_callback_index, MAX_WAIT_TIME, MAX_TRAVEL_TIME, False, 'Time')
	time_dimension = routing.GetDimensionOrDie('Time')

	# Set Arc Cost Evaluator
	routing.SetArcCostEvaluatorOfAllVehicles(time_callback_index)
	
	# Add time window constraints for each location except depot
	for i, window in enumerate(data['time_windows']):
		if i == 0:
			continue
		index = manager.NodeToIndex(i)
		time_dimension.CumulVar(index).SetRange(int(window[0]), int(window[1]))

	for v in range(data['num_vehicles']):
		index = routing.Start(v)
		time_dimension.CumulVar(index).SetRange(int(data['time_windows'][0][0]), int(data['time_windows'][0][1]))

	for v in range(data['num_vehicles']):
		routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.Start(v)))
		routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(v)))

	# Add pickup/delivery constraints
	assert data['pickups_deliveries'] != None
	for pair in data['pickups_deliveries']:
		pi = manager.NodeToIndex(pair[0])
		di = manager.NodeToIndex(pair[1])
		routing.AddPickupAndDelivery(pi, di)
		routing.solver().Add(routing.VehicleVar(pi) == routing.VehicleVar(di))
		routing.solver().Add(time_dimension.CumulVar(pi) <= time_dimension.CumulVar(di))

	# Add capacity constraint
	demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
	routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, data['capacities'], True, 'Capacity')

	# Add disjunction
	penalty = 1000
	for node in range(1, len(data['time_matrix'])):
		routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

	''' SOLVING '''
	search_parameters = pywrapcp.DefaultRoutingSearchParameters()
	search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

	solution = routing.SolveWithParameters(search_parameters)

	line = '\n>========================<\n'
	print(line)
	print('Solver status:', routing.status())

	# Return solution
	if solution:
		or_print_dropped_nodes(data, manager, routing, solution)
		or_print_time_solution(data, manager, routing, solution)
		print(line)
		return or_stroute_time_solution(data, manager, routing, solution), or_array_dropped_nodes(data, manager, routing, solution)
	else:
		print('No solution', line)
		return None

''' Prints distance-constrained solution to console '''
def or_print_distance_solution(data, manager, routing, solution):
	max_route_distance = 0
	for vehicle_id in range(data['num_vehicles']):
		index = routing.Start(vehicle_id)
		plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
		route_distance = 0
		while not routing.IsEnd(index):
			plan_output += ' {} -> '.format(manager.IndexToNode(index))
			previous_index = index
			index = solution.Value(routing.NextVar(index))
			route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
			
		plan_output += '{}\n'.format(manager.IndexToNode(index))
		plan_output += 'Distance of the route: {}m\n'.format(route_distance)
		print(plan_output)
		max_route_distance = max(route_distance, max_route_distance)

	print('Maximum of the route distances: {}m'.format(max_route_distance))

''' Returns array for distance-constrained solution '''
def or_array_distance_solution(data, manager, routing, solution):
	routes = {}
	for vehicle_id in range(data['num_vehicles']):
		index = routing.Start(vehicle_id)
		routes[vehicle_id] = {}
		routes[vehicle_id]['legs'] = []
		route_distance = 0

		while not routing.IsEnd(index):
			routes[vehicle_id]['legs'].append(manager.IndexToNode(index))
			previous_index = index
			index = solution.Value(routing.NextVar(index))
			route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
		
		routes[vehicle_id]['legs'].append(manager.IndexToNode(index))
		routes[vehicle_id]['distance'] = route_distance
	return routes

''' Prints time-constrained solution to console '''
def or_print_time_solution(data, manager, routing, solution):
  time_dimension = routing.GetDimensionOrDie('Time')
  total_time = 0
  for vehicle_id in range(data['num_vehicles']):
    index = routing.Start(vehicle_id)
    plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
    while not routing.IsEnd(index):
      time_var = time_dimension.CumulVar(index)
      plan_output += '{0} Time({1},{2}) -> '.format(manager.IndexToNode(index),solution.Min(time_var),solution.Max(time_var))
      index = solution.Value(routing.NextVar(index))
    time_var = time_dimension.CumulVar(index)
    plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),solution.Min(time_var),solution.Max(time_var))
    plan_output += 'Time of the route: {}min\n'.format(solution.Min(time_var))
    print(plan_output)
    total_time += solution.Min(time_var)
  print('Total time of all routes: {}min'.format(total_time))

''' Returns array for time-constrained solution '''
def or_array_time_solution(data, manager, routing, solution):
	time_dimension = routing.GetDimensionOrDie('Time')
	total_time = 0
	routes = {}

	for vid in range(data['num_vehicles']):
		routes[vid] = {}
		routes[vid]['stops'] = []
		index = routing.Start(vid)

		while not routing.IsEnd(index):
			time_var = time_dimension.CumulVar(index)
			location_index = manager.IndexToNode(index)
			min_time = STTime(solution.Min(time_var))
			max_time = STTime(solution.Max(time_var))
			routes[vid]['stops'].append((location_index,min_time,max_time))
			index = solution.Value(routing.NextVar(index))

		time_var = time_dimension.CumulVar(index)
		location_index = manager.IndexToNode(index)
		min_time = STTime(solution.Min(time_var))
		max_time = STTime(solution.Max(time_var))
		routes[vid]['stops'].append((location_index,min_time,max_time))

		total_time += solution.Min(time_var)

	routes[vid]['total_time'] = total_time
	return routes

''' Returns STRounte object for time-constrained solution '''
def or_stroute_time_solution(data, manager, routing, solution):
	time_dimension = routing.GetDimensionOrDie('Time')
	routes = []

	for vid in range(data['num_vehicles']):
		obj = STRoute()
		index = routing.Start(vid)

		while not routing.IsEnd(index):
			time_var = time_dimension.CumulVar(index)
			location_index = manager.IndexToNode(index)
			min_time = STTime(solution.Min(time_var))
			max_time = STTime(solution.Max(time_var))
			obj.add_stop((location_index,min_time,max_time))
			index = solution.Value(routing.NextVar(index))

		time_var = time_dimension.CumulVar(index)
		location_index = manager.IndexToNode(index)
		min_time = STTime(solution.Min(time_var))
		max_time = STTime(solution.Max(time_var))
		obj.add_stop((location_index,min_time,max_time))
		
		if not obj.is_empty():
			routes.append(obj)

	return routes

''' Prints dropped nodes to console '''
def or_print_dropped_nodes(data, manager, routing, solution):
	dropped_nodes = 'Dropped nodes:'
	for node in range(routing.Size()):
		if routing.IsStart(node) or routing.IsEnd(node):
			continue
		if solution.Value(routing.NextVar(node)) == node:
			dropped_nodes += ' ({})'.format(manager.IndexToNode(node))
	print(dropped_nodes)

''' Returns array of dropped nodes '''
def or_array_dropped_nodes(data, manager, routing, solution):
	dropped_nodes = []
	for node in range(routing.Size()):
		if routing.IsStart(node) or routing.IsEnd(node):
			continue
		if solution.Value(routing.NextVar(node)) == node:
			dropped_nodes.append(manager.IndexToNode(node))
	return dropped_nodes

