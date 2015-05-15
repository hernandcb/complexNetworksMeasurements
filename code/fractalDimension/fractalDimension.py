#
#Code in Python (written by Hernan Carvajal):
# 
#For this code to run you'll need to install Python (http://www.python.org)
#and Networkx (http://networkx.lanl.gov/).
# 
#File "fractalDimension.py" 
#
#Calculate the fractal dimension of a network by using the box covering algorithm

from .boxCovering.greedyColoring import *
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
 

def calculateFractalDimension(graph, max_box_size): 
	min_box_size = 1	
	array_size = max_box_size - min_box_size + 1
 
	# Create the arrays that will contain the values of the box size and number of boxes
	box_sizes       = np.empty(array_size, int)
	number_of_boxes = np.empty(array_size, int)
	
	boxes = greedyColoring(graph)

	# Run the box covering algorithm for the different box sizes
	for box_size in range(min_box_size, max_box_size+1):
		array_index = box_size - min_box_size
		
		# store the box size
		box_sizes[array_index] = box_size
		
		# store the number of boxes obtained for the box length 'box_size'
		number_of_boxes[array_index] = len(boxes[box_size -1])
		
		# Print the values calculated 
		print("{}, {} " . format( box_size, len(boxes[box_size -1])) )
		sys.stdout.flush()
	
	# Calculate the slope of the normalized values
	log_box_sizes = np.log(box_sizes)
	log_number_of_boxes = np.log(number_of_boxes)

	slope, intercept = np.polyfit( log_box_sizes, log_number_of_boxes, 1)
	
	print("fd, {}" . format( round( -1 * slope, 3) ))
	sys.stdout.flush()
    
    
""""
if __name__ == '__main__':
	networks = [ '../../data/realNetworks/Dolphin social network/dolphins.gml'
	#'../../data/realNetworks/American College football/football.gml'
	#'../../data/realNetworks/Neural network/celegansneural.gml', 
	#'../../data/realNetworks/Email network/email.gml'
	#'../../data/realNetworks/EColi/EColi.gml' 
	#'../../data/realNetworks/Power grid/power.gml'
	]
	
	for filename in networks:
		# Load the network
		dgraph = nx.read_gml(filename) 
		
		#  To test the algorithms we only will work with undirected graphs
		graph = dgraph.to_undirected()
			
		max_box_size = nx.diameter(graph) + 1
		#max_box_size = 30 
		#Print some info of the graph
		print("----------------------------------")
		print("Filename: ", filename);
		print("Number of nodes: ", len(graph.nodes()))
		print("Number of edges: ", len(graph.edges()))
		print("Network diameter: ", max_box_size)
		
		# Information to be print is:
		print("Box size, number of boxes")
		sys.stdout.flush()
        
		for i in range(10000):
			boxCovering.greedyColoring.calculateFractalDimension(graph, max_box_size)
"""