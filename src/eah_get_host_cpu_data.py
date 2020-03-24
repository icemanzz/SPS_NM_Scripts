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



## Function : 0xEAH, Get Host CPU Data (NM Configuration Data from BIOS HECI message)
def eah_get_host_cpu_data_py(ipmi, eah_domain ):
     netfn, eah_raw = eah_raw_to_str_py( eah_domain)
     # Send 0xEAh to ME
     rsp = send_ipmb_aardvark(ipmi , netfn , eah_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR, ERROR, ERROR, ERROR

     # Analyst get Host CPU Data format
     # NM already activated regular power limit bit = resp byte5 bits[3]
     nm_activate = get_bits_data_py( ord(rsp[4]) , 3 , 1)
     DEBUG('get_host_cpu_data : nm_activate = %d' %nm_activate)
     # Host CPU Discovery data bit = resp byte5 bits[4]
     host_discovery = get_bits_data_py( ord(rsp[4]) , 4 , 1)
     DEBUG('get_host_cpu_data : host_discovery = %d' %host_discovery)
     # EOP bit = resp byte5 bits[7]
     eop = get_bits_data_py( ord(rsp[4]) , 7 , 1)
     DEBUG('get_host_cpu_data : eop = %d' %eop)
     if(host_discovery == 1):
     	# Number of P-State Support Byte[6] value, total 1 bytes
     	p_states = calculate_byte_value_py(rsp, 6, 1)
	if(p_states == 0):
		print colored( 'ERROR, P-states are disabled by user','red')
	elif(p_states == 1):
                print colored( 'ERROR, CPU not support more P-states','red')
	else:
                print colored( 'PASS, p-states = %6d' %p_states,'green')

        # Number of T-State Support Byte[7] value, total 1 bytes
        t_states = calculate_byte_value_py(rsp, 7, 1)
        if(t_states == 0):
                print colored( 'ERROR, T-states are disabled by user','red')
        else:
                print colored( 'PASS, t-states = %6d' %t_states,'green')

        # Number of CPU sockets Byte[8] value, total 1 bytes
        cpu_numbers = calculate_byte_value_py(rsp, 8, 1)
	DEBUG('get_host_cpu_data : cpu_numbers = %d' %cpu_numbers)
        # HWP Capability Highest Byte[9] value, total 1 bytes
        hwp_highest = calculate_byte_value_py(rsp, 9, 1)
        DEBUG('get_host_cpu_data : hwp_highest = %d' %hwp_highest)
        # HWP Capability Gurranteed Performance Byte[10] value, total 1 bytes
        hwp_guar_performance = calculate_byte_value_py(rsp, 10, 1)
        DEBUG('get_host_cpu_data : hwp_guar_performance = %d' %hwp_guar_performance)
        # HWP Capability Most Efficiency Performance Byte[11] value, total 1 bytes
        hwp_eff_performance = calculate_byte_value_py(rsp, 11, 1)
        DEBUG('get_host_cpu_data : hwp_eff_performance = %d' %hwp_eff_performance)
        # HWP Capability Lowest Performance Byte[12] value, total 1 bytes
        hwp_low_performance = calculate_byte_value_py(rsp, 12, 1)
        DEBUG('get_host_cpu_data : hwp_low_performance = %d' %hwp_low_performance)

     else: ## no received Host CPU data from BIOS HECI message
	print colored( 'ERROR, ME not received Host CPU Data from BIOS HECI message ','red')
	p_states = 0
	t_states = 0
	cpu_numbers = 0
	hwp_highest = 0
	hwp_guar_performance = 0
	hwp_eff_performance = 0
	hwp_low_performance = 0

     sts = PASS

     return sts, nm_activate, host_discovery, eop, p_states, t_states, cpu_numbers, hwp_highest, hwp_guar_performance, hwp_eff_performance, hwp_low_performance


def usage():
        # Description of how to use this script
        print' Useage $ sudo python eah_get_host_cpu_data.py [delay_time (sec)] [loop_number]'
        print' ex: sudo python eah_get_host_cpu_data.py 1 100'

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
        print 'Start to Send Get Host CPU Data..'
        while loop_number :
                sts, nm_activate, host_discovery, eop, p_states, t_states, cpu_numbers, hwp_highest, hwp_guar_performance, hwp_eff_performance, hwp_low_performance  = eah_get_host_cpu_data_py(ipmi , eah_platform_domain )
                # Add delay time to make sure me go back to stable mode
                time.sleep(delay_time)
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


                if( loop_number == 'loop' ):
                        loop_number = True
                else:
                        loop_number = loop_number -1

                if(sts == ERROR ):
                        loop_number = False
                        break
else:
        print' Done! '

