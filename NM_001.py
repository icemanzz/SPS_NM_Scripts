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
print 'Start to Test NM_001...'

#Wait for Host Reset
#print colored('Please make sure DUT already EOP (boot into OS or UEFI Shell) ', 'green')

#try:
#    input("Press Enter when you want to start...")
#except SyntaxError:
#    pass

sts, nm_activate, host_discovery, eop, p_states, t_states, cpu_numbers, hwp_highest, hwp_guar_performance, hwp_eff_performance, hwp_low_performance  = eah_get_host_cpu_data_py(ipmi , eah_platform_domain )
# Send D4h Get Number of P/T states support in this platform
d4_p_states, d4_t_states = get_number_of_pt_states(ipmi, d4h_ctl_knob_max_pt )


if(sts == PASS ):
        # Show Result
        print('NM Activated = %d' %nm_activate )
        print('Host Discovery = %d' %host_discovery  )
        print('EOP =%d' %eop)
        print('P-States = %d' %p_states)
        print('T-States = %d' %t_states)
        print('CUP Numbers = %d' %cpu_numbers)
        print('HWP Highest = %d' %hwp_highest)
        print('HWP Gurantee Performance = %d' %hwp_guar_performance)
        print('HWP Efficiency Performance = %d' %hwp_eff_performance)
        print('HWP Lowest Performance = %d' %hwp_low_performance)
        print('P-States D4h = %d' %d4_p_states)
        print('T-States D4h = %d' %d4_t_states)

        if(host_discovery != 1 ):
                print colored ('NM_001 Fail, SPS ME No Receive HOST CPU DATA HECI MESSAGE From BIOS' , 'red')
	elif(eop != 1):
                print colored ('NM_001 Fail, SPS ME No Receive BIOS EOP Message' , 'red')
        elif(p_states <= 1):
                print colored ('NM_001 Fail, SPS ME P-States not enabled in BIOS' , 'red')
	elif(t_states <= 0 ):
                print colored ('NM_001 Fail, SPS ME T-States not enabled in BIOS' , 'red')
        elif( p_states != d4_p_states):
                print colored ('NM_001 Fail, SPS ME P-States not match BIOS Host CPU HECI Message settings' , 'red')
        elif( t_states != d4_t_states):
                print colored ('NM_001 Fail, SPS ME T-States not match BIOS Host CPU HECI Message settings' , 'red')
        else:
                print colored ('NM_001 Pass' , 'green')
else:
         print colored ('NM_001 Fail, Aardvark data transfer error or initial error ' , 'red')

