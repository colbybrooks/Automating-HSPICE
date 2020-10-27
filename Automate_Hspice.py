################################################################################
# Colby Brooks                                                              #
# Built a python scripts that automates running hspice.  Given a parameter value
# for the number of fans and inverters, the code is designed to also automate creating
# the spice .sp files for each iteration of fan and inverters.  After each .sp file is created
# using the subprocess command to output a text so unix will run the .sp file with hspice
# The code is iterated to find the smallest time delay.
# Inverters <= 25
###############################################################################
# Last Section is commented to run without HSpice.  If you have Hspice, you can
# delete the Holding_Block to run
################################################################################

import numpy as np  # package needed to read the results file
import subprocess  # package needed to lauch hspice
import shutil       # package needed to copy a file

################################################################################
# Start the main program here.                                                 #
################################################################################

numfan = 20
numinv = 25             # Can only be Odd numbers
import string           # Import string
num2alpha = dict(zip(range(1, 27), string.ascii_lowercase))    # Creates a number to string function; 1 = a , 26 = z
min_tph = 100       # Creates big time delay
optimal_fan = ()        # Creates blank array
optimal_inverter = ()
# For loop for number of fans and inverters
for fan in range(2, numfan+1):
    for inv in range(1, numinv+2, 2):
        shutil.copy("InvChain.sp", "inv.sp")        # Copy invchain to new file inv
        f = open('inv.sp', 'a')                     # open inv.sp
        text = '.param fan = {}\n'.format(fan)      # creates text for fan and writes it
        f.write(text)
        if (numinv == 1): # If statemnt to add a z if numinv == 1
            text = 'Xinv1 a z inv M=1\n'
        if (numinv > 1): # If statement for if numinv is greater than 1
            text = 'Xinv1 a b inv M=1\n'
            f.write(text) # To add the first line for (a b) if numinv  is greater than 1

            for index in range(3, inv + 2, 2): # Text addition for numinv > 1 past the first line
                text = 'Xinv{} {} {} inv M=fan**{}\n'.format(index-1, num2alpha[index-1], num2alpha[index], index - 2)
                # Text to write inverters greater than 1
                f.write(text)
                if(index == numinv):  # If on the last inverter, this makes the last letter equal to z
                    zindex = 26
                    text = 'Xinv{} {} {} inv M=fan**{}\n'.format(index, num2alpha[index], num2alpha[zindex], index - 1)
                    f.write(text)
        f.write('.end') # closing end statement
        f.close() # close the appending

# Delete Holding_Block if you do have Hspice, also delete terminating ''' at the bottom
Holding_Block = '''

        proc = subprocess.Popen(["hspice", "inv.sp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #output, err = proc.communicate()

        # extract tphl from the output file
        data = np.recfromcsv("inv.mt0.csv", comments="$", skip_header=3)
        tphl = data["tphl_inv"]
        print("Fan =", fan,"\t inverter =", inv, "\t tph1 =", tphl) # print statements out for each iteration
        if (tphl < min_tph): # if statement to compare current time delay to the minimum
            # set the optimal conditions
            min_tph = tphl
            optimal_fan = fan
            optimal_inverter = inv

# Print statements for min time delay and coreesponding fan and inverters
print("The Lowest Time Delay is ", min_tph)
print("The optimal fan count is ", optimal_fan)
print("The optimal inverter count is ", optimal_inverter)

'''