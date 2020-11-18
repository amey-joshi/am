import math
import numpy as np
import pandas as pd

data = pd.read_csv('consolidated-1.csv')
time_window = '3min' 
time_window_size = int(time_window[0])
data['Avg-time'] = data['Avg-time'].fillna(0)

# The rolling window size has nothing to do with the time window.
# It just determines the number of past readings one should use to 
# estimate lambda.
data['lambda'] = data['ncalls'].rolling(window=5).mean() 

data.set_index('Create-time', inplace=True)
data['mu'] = data['Avg-time']/(time_window_size * 60) 
data['E'] = data['lambda']*data['mu'] # Ordered traffic in erlangs

def prob_of_wait(E, m):
	"""
	E:	  traffic
	m:	  # agents.
	Reference: https://en.wikipedia.org/wiki/Erlang_(unit)
	"""
	p = 1
	
	if math.isnan(E):
		p = 0
	elif m > E:
		numerator = (m * E**m)/(math.factorial(m) * (m - E))
		denominator = 0

		for i in range(m):
			denominator += E**i/math.factorial(i)

			denominator += numerator

			p = numerator/denominator

	return p

def calculate_ASA(wait_prob, mu, nagents, E):
	a_large_number = 1000

	if nagents > E:
		return wait_prob * mu/(nagents - E) * time_window_size
	else:
		return a_large_number

def find_nagents(E, m):
	start = m

	if not math.isnan(E):
		threshold = 0.8

		try:
			if prob_of_wait(E, m) > threshold:
				while prob_of_wait(E, start) > threshold:
					start += 1
			else:
				while prob_of_wait(E, start) < threshold:
					start -= 1
		except OverflowError:
			print(f'Overflow at E = {E} and m = {m}.')

	return start
	
def exp_wait_time(E, nagents, nagents_reqd, avg_time):
	d = avg_time * nagents
	x = 0
	
	if d != 0:
		x = (E - nagents_reqd + 1)/d
		
	return x * time_window_size * 60

data['wait-prob'] = data.apply(lambda r: prob_of_wait(r['E'], r['nagents']), axis=1)
#data['asa'] = data.apply(lambda r: calculate_ASA(r['wait-prob'], r['mu'], r['nagents'], r['E']), axis=1)
data['nagents_reqd'] = data.apply(lambda r: find_nagents(r['E'], r['nagents']), axis = 1)
data['rolling-wait-prob'] = data['wait-prob'].rolling(window=5).mean() 
data['exp-wait-time'] = data.apply(lambda r: exp_wait_time(r['E'], r['nagents'], r['nagents_reqd'], r['mu']), axis=1) 
data.reset_index(level=0, inplace=True)
data.to_csv('wait_prob_1.csv', index=False, float_format = '%.3f')
#data.to_excel('wait_prob_1.xlsx', index=False, float_format = '%.3f')

