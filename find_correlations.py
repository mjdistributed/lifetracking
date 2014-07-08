# find correlations between independent variable (productivity) and dependent

import json
import json_parsing
from json_parsing import *
import matplotlib.pyplot as plt
import math
import numpy as np
from ols_0_2 import ols 	#SciPy Ordinary Least Squares
from array import array
from numpy import array as nparray
import statsmodels.api as sm

# directory = "Reporter-App"
# dates = ['2014-02-08', '2014-02-09', "2014-02-10", "2014-02-11", "2014-02-12", "2014-02-13", "2014-02-14", "2014-02-17", "2014-02-19", "2014-02-20", "2014-02-27", "2014-03-03", "2014-03-09", "2014-03-13", "2014-03-14", "2014-03-15", "2014-03-16", "2014-03-17", "2014-03-18"]
directory = "karina_data"
dates = ["CLEANED-karina_jun1"]
# dates = ["copy"]


def first_order(var_name, sub_field_name):
	""" return a list of (x,y) pairs that correspond to (independent, dependent) variables where independent is var_name and dependent is replies to 'are you working'"""
	vals = list() # list of (x,y) pairs
	for date in dates:		
		curr_file = open(directory + "/" + date + "-reporter-export.json")
		curr_str = curr_file.read()
		curr_data = json.loads(curr_str)
		curr = Data.deserialize(curr_data)
		for snap in curr.snapshots:
			if not filter(lambda x : x.questionPrompt == "Are you working?", snap.responses):
				continue 	# only care about the ones where we reported productivity
			x_val = snap.__getattr__(var_name)
			if(sub_field_name != ""):
				x_val = x_val.__getattr__(sub_field_name)
			if(type(x_val) is colander._drop):
				continue # only care about the ones where we reported our query variable
			y_val = filter(lambda x : x.questionPrompt == "Are you working?", snap.responses)[0].answeredOptions[0]
			vals.append((x_val,y_val))
	return vals

def standardize(correlation, bucket_size):
	""" Takes a list of (x,y) values and returns a histogram of (x,y) pairs where y is the fraction of times x created a yes reponse"""
	new_correlation = list()
	for tup in correlation: # should be able to convert to a map statement
		x_val = tup[0]
		y_val = 1 if tup[1] == 'Yes' else 0
		new_correlation.append((x_val, y_val))
	x_vals = set(map(lambda tup: tup[0], new_correlation))
	buckets = np.arange(min(x_vals), max(x_vals), bucket_size)
	standardized = list()
	for x in buckets: # create a histogram of how many times each x value created a "yes" response
		num_success = len(filter(lambda tup: (tup[0] >= x) and (tup[0] < (x+bucket_size)) and (tup[1] == 1), new_correlation))
		total_num = len(filter(lambda tup: (tup[0] >= x) and (tup[0] < (x+bucket_size)), new_correlation))
		fraction_success = num_success*1.0/total_num if total_num > 0 else 0.0
		standardized.append((x+bucket_size/2.0,fraction_success))
	return standardized

def separate_vals(correlation):
	correlation = sorted(correlation, key=lambda tup: tup[0])
	x_vals = map(lambda tup: tup[0], correlation)
	y_vals = map(lambda tup: tup[1], correlation)
	return (x_vals, y_vals)

def plot(correlation):
	(x_vals, y_vals) = separate_vals(correlation)
	plt.plot(x_vals, y_vals)
	plt.show()

def analyze_firstOrder(field, subfield="", bucket_size=1):
	correlation = first_order(field, subfield)
	correlation = standardize(correlation, bucket_size)
	plot(correlation)
	return correlation

# will substitute for ML optimum for now
# this is the ML step
def guess_optimums(x_vars, y_vars):
	"""Determines the "optimum y" for the query x, given a simple best-fit line for the data"""
	reorder = sorted(range(len(x_vars)), key = lambda ii: x_vars[ii])
	x_vars = [x_vars[ii] for ii in reorder]
	y_vars = [y_vars[ii] for ii in reorder]
	plt.scatter(x_vars, y_vars, s=30, alpha=0.15)
	# determine best fit line
	par = np.polyfit(x_vars, y_vars, 1, full=True)

	slope=par[0][0]
	intercept=par[0][1]
	(x0, x1) = [min(x_vars), max(x_vars)]
	y_vals = [slope*x0 + intercept, slope*x1 + intercept]
	estimated_y = [y_vals[0] + slope*i for i in range(int(x0),int(math.ceil(x1)))]

	plt.plot([x0,x1], y_vals, '-r')
	plt.show()
	return(range(int(x0),int(math.ceil(x1))), estimated_y)

# return a mapping of multiple independent variables to one dependent variable
def get_multiple_regression_vars(query_x_vals, query_x_vals_sub_field_names):
	#aggregate data
	x_vals = list()	# will be multi-dimensional array of x-values
	y_vals = list()	# array of y-values
	for date in dates:		
		curr_file = open(directory + "/" + date + "-reporter-export.json")
		curr_str = curr_file.read()
		curr_data = json.loads(curr_str)
		curr = Data.deserialize(curr_data)
		for snap in curr.snapshots:
			if not filter(lambda x : x.questionPrompt == "Are you working?", snap.responses):
				continue 	# only care about the ones where we reported productivity
			curr_x_vals = list()
			to_break = False
			for i in range(len(query_x_vals)):
				x_val = snap.__getattr__(query_x_vals[i])
				sub_field_name = query_x_vals_sub_field_names[i]
				if(sub_field_name != ""):
					x_val = x_val.__getattr__(sub_field_name)
				if(type(x_val) is colander._drop):
					x_val = 0
				curr_x_vals.append(x_val)
			x_vals.append(curr_x_vals)
			y_val = filter(lambda x : x.questionPrompt == "Are you working?", snap.responses)[0].answeredOptions[0]
			y_vals.append(y_val)
	return (x_vals, y_vals)

# find a best-fit for one dependent variable and more than one independent variable
def multiple_regression(x_vars, y_vars):
	print(x_vars)
	print(y_vars)
	mymodel = ols(nparray(y_vars),nparray(x_vars),"Working_YN_Responses",["battery", "audio"])
	print(mymodel.summary())
	print(mymodel.b);

# using Statsmodels API, find a best-fit for one dependent variable and more than one independent variable
# returns a mapping from field -> scale parameter
def alternative_multiple_regression(x_vars, y_vars):
	x_vars = sm.add_constant(x_vars)
	est = sm.OLS(y_vars, x_vars)
	est = est.fit()
	print(est.summary())
	params = est.params
	(primary_fields, sub_fields) = get_fields()
	paramDict = {}
	for i in range(len(params)):
		paramDict[primary_fields[i] + "." + sub_fields[i]] = params[i]
	return paramDict

def get_fields():
	primary_fields = list(["battery", "location", "location", "steps", "day", "audio", "audio", "sync", "connection", "background", "dwellStatus", "draft", "weather", "weather", "weather", "weather", "weather", "weather", "weather", "weather", "weather", "weather", "weather", "weather"])
	sub_fields = list(["", "longitude", "latitude", "", "", "avg", "peak", "", "", "", "", "", "windMPH", "tempF", "precipTodayIn", "visibilityMi", "feelsLikeF", "windGustMPH", "pressureIn", "pressureMb", "windKPH", "windDegrees", "uv", "dewpointC"])
	return (primary_fields, sub_fields)

# takes a list of lists and returns a list of tuples
def list_to_tuple(x_vars_list):
	tuples = list()
	for i in range(len(x_vars_list)):
		curr_vals = x_vars_list[i]
		new_tuple = tuple(curr_vals)
		tuples.append(new_tuple)
	return tuples

# return the most influential variables, using a mapping from parameter -> scale parameter
def find_most_influential_vars(paramDict, numTop):
	# convert dictionary to list of tuples
	tup_list = list()
	for key in paramDict.keys():
		tup_list.append((key, paramDict[key]))
	# sort this list of tuples
	sorted_list = sorted(tup_list, lambda (x,y), (a,b): -1 if math.fabs(y) < math.fabs(b) else 1)
	return sorted_list[len(sorted_list) - numTop:]





(primary_fields, sub_fields) = get_fields()
(x_vals, y_vals) = get_multiple_regression_vars(primary_fields, sub_fields)
x_vals = list_to_tuple(x_vals)
y_vals = map(lambda x: 1 if x == "Yes" else 0, y_vals)
paramDict = alternative_multiple_regression(x_vals, y_vals)
print(paramDict)
most_influential = find_most_influential_vars(paramDict, 5)
print(most_influential)
# print(x_vals)
# (x_vals, y_vals) = get_multiple_regression_vars(list(["battery", "audio"]), list(["", "avg"]))
#multiple_regression(x_vals, y_vals)
# (x_vals,y_vals) = separate_vals(analyze_firstOrder("battery"))
# (x, test_y) = guess_optimums(x_vals, y_vals)
# print(test_y[2])
# analyze_firstOrder("weather", subfield="tempF", bucket_size=5)
# analyze_firstOrder("battery", bucket_size=0.1)
# correlation = [(1, "Yes"), (2,"No"), (3,"Yes"), (4,"Yes")]
# print(standardize(correlation,4))
