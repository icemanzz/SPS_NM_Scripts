import pyipmi
import pyipmi.interfaces
import time
import os
import glob
import os.path as path
import shutil
import math
import numpy
import mmap
import array
import getopt
import sys

from os_parameters_define import *
from utility_function import *
from nm_ipmi_raw_to_str import *
from error_messages_define import *
from nm_functions import *
from config import *



def aardvark_ipmi_init(target_addr, channel):
    ## Test pyIPMI
    opts, args = getopt.getopt(sys.argv[1:], 't:hvVI:H:U:P:o:b:')
    interface_name = 'aardvark'
    name = 'pullups'
    value = 'off'
    aardvark_pullups = False
    aardvark_serial = None
    aardvark_target_power = False
    target_address = target_addr
    target_routing = [(target_addr ,channel)]
    ###
    interface = pyipmi.interfaces.create_interface(interface_name, serial_number=aardvark_serial)
    ipmi = pyipmi.create_connection(interface)
    ipmi.target = pyipmi.Target(target_address)
    #ipmi.target.set_routing(target_routing)

    return ipmi


# Define print program usage for user
def usage():
        # Description of how to use this script
        print' Useage $ sudo python nm_ptu.py [function_parameter] [select_parameter]'
	print' [function_parameter] = run/read'
        print' [fuction_parameter] = run + [select_parameter] = 0 (do not launch PTU)/ 1 (launch after platform reset)/ 2(launch PTU when HW change)'
        print' [fuction_parameter] = read + [select_parameter] = platform/cpu/mem'
        print' example of launch NM PTU after reset : $ sudo python nm_ptu.py run 1  (reset your system and wait system EOP)'
        print' example of read NM PTU result after platform reset: $  sudo python nm_ptu.py read platform'
        return


## Define Input parameters lenth check
def parameter_check(parameter):
        if(len(parameter) != 3  ):
		print'input parameter error, please check usage as below. '
                usage()
                return ERROR
        else:
		if(str(parameter[1]) == 'run' ):
			if( int(parameter[2]) > 2 or int(parameter[2]) < 0 ):
				print' select parameter input error , please input a number between 0~2 , as below usage'
				usage()
				return ERROR
			else:
				print ' check run usage parameters input is PASS'
				function = 'run'
				select = int(parameter[2])
				return PASS, function, select
		elif(str(parameter[1]) == 'read'):
			if(str(parameter[2]) == 'platform' ):
                                print ' check read usage parameters input is PASS'
                                function = 'read'
                                select = nmptu_61h_platform
                                return PASS, function, select
			elif(str(parameter[2]) == 'cpu' ):
                                print ' check read usage parameters input is PASS'
                                function = 'read'
                                select = nmptu_61h_cpu
                                return PASS, function, select
			elif(str(parameter[2]) == 'mem' ):
                                print ' check read usage parameters input is PASS'
                                function = 'read'
                                select = nmptu_61h_memory
                                return PASS, function, select
			else:
				print'input read parameter error, please input string as below example'
				usage()
				return ERROR
		else:
			print('input parameter error, please check usage as below.')
			usage()
			return ERROR

                return ERROR

## _Main_ ##

# Initial aardvark
ipmi = aardvark_ipmi_init(target_me_addr, target_me_bridge_channel)

# Check input parameters
sts, function, select = parameter_check(sys.argv)

if(sts == PASS):
        if(function == 'run'):
		# Send PTU Launch
		sts = set_ptu_launch_request_py(ipmi, select )
		if(sts == ERROR):
			print('NM PTU lanuch fail !!!')
		else:
			print('Set NM PTU successfully. Please reset your system or change HW to start NM PTU')

	elif(function == 'read'):
		# Get NM PTU Result via 0x61h cmd
		print' NM PTU Result Read : %s ' %str(sys.argv[2])
		max_power, min_power, eff_power = get_ptu_launch_result_py(ipmi, select)
		print' Maximum Range = %d ' %max_power
		print' Minimum Rnage = %d ' %min_power
		print' Efficiency Range = %d' %eff_power
	else:
		print'Please Try again...'

else:
	print' Please Try again...'

