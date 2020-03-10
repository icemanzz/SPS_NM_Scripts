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


#Inmport path
sys.path.append('../src')
from aardvark_initial import *

#Inmport path
sys.path.append('../')
from os_parameters_define import *
from utility_function import *
from nm_ipmi_raw_to_str import *
from error_messages_define import *
from nm_functions import *
from config import *




## Fucntion : Send IPMI Cold reset
def cold_reset_py(ipmi):
     netfn, cold_reset_raw = cold_reset_raw_to_str_py()
     # Send cold reset
     rsp = send_ipmb_aardvark(ipmi , netfn , cold_reset_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), App )
     if(sts != SUCCESSFUL ):
         return ERROR

     return PASS



def usage():
        # Description of how to use this script
        print' Useage $ sudo python me_reset.py [delay_time (sec)] [loop_number]'
        print' ex: sudo python me_reset.py 1 100'

        return


## Define Delay Time check function
def delay_check(parameter):
        delay_time = int(parameter , 10)
        if(delay_time > 0 ):
                sts = PASS
        else:
                delay_time = ERROR
                sts = ERROR

        return sts, delay_time


## Define Delay Time check function
def loop_check(parameter):
        if(parameter == 'loop'):
                loop_number = 'loop'
                sts = PASS

        else:
                loop_number = int(parameter , 10)
                if(loop_number > 0 ):
                        sts = PASS
                else:
                        loop_number = ERROR
                        sts = ERROR

        return sts, loop_number



## Define Input parameters lenth check
def parameter_check(parameter):
        if(len(parameter) != 3  ):
                usage()
                sts =ERROR
                return ERROR
        else:
                return PASS


## _Main_ ##

# Check delay time parameter
sts = parameter_check(sys.argv)
if(sts == PASS):
        print 'Check Delay Time parameter setting'
        sts, delay_time = delay_check(str(sys.argv[1]))
        print ( "delay time =  %d "  %(delay_time) )
        sts, loop_number = loop_check(str(sys.argv[2]))
        print ("loop_number = " , loop_number)
else:
        sts = ERROR

if(sts == PASS):
        print 'Start to Send ME Reset..'
        while loop_number :
                sts = cold_reset_py(ipmi)
                # Add delay time 5 secs to make sure me go back to stable mode
                time.sleep(delay_time)

                if( loop_number == 'loop' ):
                        loop_number = True
                else:
                        loop_number = loop_number -1

                if(sts == ERROR ):
                        loop_number = False
                        break
else:
        print' Done! '

