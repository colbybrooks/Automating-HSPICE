# scrptinghspice-python
Built a python scripts that automates running hspice.  Given a parameter value
for the number of fans and inverters, the code is designed to also automate creating
the spice .sp files for each iteration of fan and inverters.  After each .sp file is created
using the subprocess command to output a text so unix will run the .sp file with hspice
The code is iterated to find the smallest time delay

# Prerequisites
Python 3.7 used (any Python3 should work)
Anacondas Environment
HSPICE
