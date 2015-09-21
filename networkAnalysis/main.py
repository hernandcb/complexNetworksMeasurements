import sys
import time
import os
import networkx as nx
import fractalDimension.fractalDimension as fd
import random as rnd

if __name__ == '__main__':
    # Set the number of iterations per network
    iterations = 10000
    
    #Create the list of files to be processed
    basePath = "../data/realNetworks/" 
    networks = { 
    "test" : basePath + 'Dolphin social network/dolphins.gml' #,
	#"football" : basePath + 'American College football/football.gml',
	#"celegans" : basePath + 'Neural network/celegansneural.gml', 
	#"email" : basePath + 'Email network/email.gml',
	#"eColi" : basePath + 'EColi/EColi.gml', 
	#"power" : basePath + 'Power grid/power.gml'
	}
    
	
    #Specify the folder where the ouputs should be located
    currentTime = time.strftime("%d-%m-%Y")
	
    for netName, netPath in networks.items():
        folderPath = "../results/" + currentTime + "/"
        fileName = netName + '_fractalDimension.out'
        # Load the network
        dgraph = nx.read_gml(netPath) 
        graph = dgraph.to_undirected()
        max_box_size = nx.diameter(graph) + 1
        n = rnd.randint(1, 999999)
        result = fd.calculateFractalDimension(graph, max_box_size, iterations=50, seed = n)
        print(result)
"""		
        #Create folder if not exists
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        
        # Redirect the output to a file with the network name
        sys.stdout = open(folderPath + fileName, 'w+')
		# Load the network
        dgraph = nx.read_gml(netPath) 
		
		#  To test the algorithms we only will work with undirected graphs
        graph = dgraph.to_undirected()
			
        max_box_size = nx.diameter(graph) + 1
		#max_box_size = 30 
		#Print some info of the graph
        print("----------------------------------")
        print("Network: ", netName);
        print("Number of nodes: ", len(graph.nodes()))
        print("Number of edges: ", len(graph.edges()))
        print("Network diameter: ", max_box_size)
		
		# Information to be print is:
        print("Box size, number of boxes")
        sys.stdout.flush()
        
        for i in range(iterations):
        	fd.calculateFractalDimension(graph, max_box_size)
"""		