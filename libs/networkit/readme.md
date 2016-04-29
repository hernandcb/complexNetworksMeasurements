These files contains the implementation of the greedy coloring algorithm for the Networkit library. 
In order to make them function you should download the library (https://networkit.iti.kit.edu/data/uploads/networkit.zip) and place it in the same folder where is located this project. The files should be placed at:

 - ComplexNetworksMeasurements
 - Networkit/
    - networkit/_Networkit.cpp
    - networkit/cpp/graph/Graph.h
    - networkit/cpp/graph/Graph.cpp

Once you have replaced the files, you can compile the networkit library (Install all the dependences first https://networkit.iti.kit.edu/getting-started/):

python3 setup.py build_ext 
pip3 install -e ./
