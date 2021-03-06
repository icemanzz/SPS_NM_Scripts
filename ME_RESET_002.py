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


## _Main_ ##
print 'Start to Test ME_RESET_002...'

#Wait for Host Reset
print colored( 'Please Warm Reset DUT system .... (UEFI shell: mm CF9 6)' , 'green')

try:
    input("Wait DUT Warm Reset .... Press Enter when system reset back to S0...")
except SyntaxError:
    pass

# Import src
sys.path.append('src/')
from get_device_id import *
from mesdc_26h_get_version import *

sts, rsp, current_status, operation_state , eop = mesdc_get_version_py(ipmi)
sts, sps_version, platform, dcmi, nm, image  = get_device_id_py(ipmi)

if(sts == PASS ):
        # Show Result
        print('SPS Version = '+ sps_version)
        print('platform = %d' %platform  )
        print('dcmi =%d' %dcmi)
        print('nm = %d' %nm)
        print('image = %d' %(image))
        print('SPS Current_Status = '+ str(current_status))
        print('SPS Operation_State ='+ str(operation_state))
        print('EOP =' + str(eop))

        if(current_status != 5 ):
                print colored ('ME_RESET_002 Fail, SPS ME not in operation mode' , 'red')
	elif(operation_state != 1):
                print colored ('ME_RESET_002 Fail, SPS ME not in M0 with UMA state' , 'red')
        elif(eop != 1):
                print colored ('ME_RESET_002 Fail, SPS ME not receive EOP' , 'red')
	elif(image == 0 ):
                print colored ('ME_RESET_002 Fail, SPS ME not in operation mode' , 'red')

        else:
                print colored ('ME_RESET_002 Pass' , 'green')
else:
         print colored ('ME_RESET_002 Fail, Aardvark data transfer error or initial error ' , 'red')

