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
from nm_functions_libs import *



## _Main_ ##
print 'Start to Test DELL PMbus Device Config Check...'

DELL_PMBUS_USER_INDEX = [ 0x00, 0x01, 0x04, 0x05 , 0x08, 0x09 ]


print('User_ID | smbus_addr | mux_addr | device_state | device_mode | device_type \n' )

for i in range(0, len(DELL_PMBUS_USER_INDEX)):

	sts, smbus_addr, mux_addr, device_state, device_mode, device_type = f4h_get_pmbus_device_config_py(ipmi , DELL_PMBUS_USER_INDEX[i] )


	if(sts == PASS ):
        	# Show Result
        	#print('User_ID | smbus_addr | mux_addr | device_state | device_mode | device_type \n' )
                print(' 0x%X |  0x%X   |  0x%X  |  %X  |  %X  |  %X  ' %(DELL_PMBUS_USER_INDEX[i],smbus_addr,mux_addr,device_state,device_mode,device_type) )

	else:
        	print colored ('DELL_PMBUS_F4 TEST Fail' , 'red')

