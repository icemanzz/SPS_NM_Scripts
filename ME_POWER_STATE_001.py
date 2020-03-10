import pyipmi
import pyipmi.interfaces
import os
import re
import datetime
import os.path
import time
import math
import numpy
import mmap
import array
import getopt
import sys
from termcolor import colored

#Import path
from os_parameters_define import *
from utility_function import *
from nm_ipmi_raw_to_str import *
from error_messages_define import *
from nm_functions import *
from config import *

# Import src
sys.path.append('src/')
from mesdc_26h_get_version import *



## _Main_ ##

print 'Start to Test ME_POWER_STATES_001...'
sts, rsp, current_status, operation_state , eop = mesdc_get_version_py(ipmi)

if(sts == PASS ):
        # Show Result
        print('SPS Current_Status = '+ str(current_status))
        print('SPS Operation_State ='+ str(operation_state))
        print('EOP =' + str(eop))

        if(current_status != 5 ):
                print colored ('ME_POWER_STATES_001 Fail, SPS ME not in operation mode' , 'red')
	elif(operation_state != 1):
                print colored ('ME_POWER_STATES_001 Fail, SPS ME not in M0 with UMA state' , 'red')
        elif(eop != 1):
                print colored ('ME_POWER_STATES_001 Fail, SPS ME not receive EOP' , 'red')

        else:
                print colored ('ME_POWER_STATES_001 Pass' , 'green')
else:
         print colored ('ME_POWER_STATES_001 Fail, Aardvark data transfer error or initial error ' , 'red')

