# This script install the required dependencies of the library on a Debian 8 system

# Install no-python dependences
# LAPACK
apt-get install liblapack-dev
apt-get install libatlas-base-dev gfortran
apt-get install scons

# Install pip 
apt-get install python3-pip 

#  Install networkit dependences
pip install networkx
pip install tabulate
pip install scipy
pip install cython
pip install pandas 
pip install seaborn sklearn
pip install ipython
apt-get install python3-matplotlib

# Install networkit
pip install networkit
