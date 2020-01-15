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
        print' Useage $ sudo python cpu_mem_thermal.py [function_parameter] [ cpu_select ] [ dimm_select]'
        print' [function_parameter] = standard/extended'
        print' [cpu_select] = cpu_domain0 (CPU0~CPU3)/cpu_domain1 (CPU4~CPU7)'
        print' [dimm_select] = dimm_domain0 (channel0~channel3)/ dimm_domain1 (channel4~channel 7) / all (check all dimm channels)'
        print' example of cpu_mem_thermal.py standard mode:$ sudo python cup_mem_thermal.py standard cpu_domain0 all'
        print' example of cpu_mem_thermal.py extended mode:$ sudo python cup_mem_thermal.py extended cpu_domain0 all'

        return

## Define Input parameters lenth check
def parameter_check(parameter):
        if( len(parameter) != 4  ):
                print'input parameter error, please check usage as below. '
                usage()
                return ERROR
        else:
                if(str(parameter[1]) == 'standard' ):
			function = get_temp_4bh_standard
                        if(str(parameter[2]) == 'cpu_domain0' ):
                                cpu_select = get_temp_4bh_cpu_domain0
				if(str(parameter[3]) == 'dimm_domain0' ):
					dimm_select = get_temp_4bh_mem_domain0
                                	return PASS, function, cpu_select, dimm_select
				elif(str(parameter[3]) == 'dimm_domain1'):
                                        dimm_select = get_temp_4bh_mem_domain1
                                        return PASS, function, cpu_select, dimm_select
				elif(str(parameter[3]) == 'all'):
                                        dimm_select = 'all'
                                        return PASS, function, cpu_select, dimm_select
				else:
					print'dimm_select parameter in correct , please refer to usage.'
					return ERROR

			elif(str(parameter[2]) == 'cpu_domain1'):
                                cpu_select = get_temp_4bh_cpu_domain1
                                if(str(parameter[3]) == 'dimm_domain0' ):
                                        dimm_select = get_temp_4bh_mem_domain0
                                        return PASS, function, cpu_select, dimm_select
                                elif(str(parameter[3]) == 'dimm_domain1'):
                                        dimm_select = get_temp_4bh_mem_domain1
                                        return PASS, function, cpu_select, dimm_select
                                elif(str(parameter[3]) == 'all'):
                                        dimm_select = 'all'
                                        return PASS, function, cpu_select, dimm_select
                                else:
                                        print'dimm_select parameter in correct , please refer to usage.'
                                        return ERROR
                        else:
                                print' Check parameter cpu_select settings incorrect !'
                                usage()
                                return ERROR

                elif(str(parameter[1]) == 'extended' ):
                        function = get_temp_4bh_extended
                        if(str(parameter[2]) == 'cpu_domain0' ):
                                cpu_select = get_temp_4bh_cpu_domain0
                                if(str(parameter[3]) == 'dimm_domain0' ):
                                        dimm_select = get_temp_4bh_mem_domain0
                                        return PASS, function, cpu_select, dimm_select
                                elif(str(parameter[3]) == 'dimm_domain1'):
                                        dimm_select = get_temp_4bh_mem_domain1
                                        return PASS, function, cpu_select, dimm_select
                                elif(str(parameter[3]) == 'all'):
                                        dimm_select = 'all'
                                        return PASS, function, cpu_select, dimm_select
                                else:
                                        print'dimm_select parameter in correct , please refer to usage.'
                                        return ERROR

                        elif(str(parameter[2]) == 'cpu_domain1'):
                                cpu_select = get_temp_4bh_cpu_domain1
                                if(str(parameter[3]) == 'dimm_domain0' ):
                                        dimm_select = get_temp_4bh_mem_domain0
                                        return PASS, function, cpu_select, dimm_select
                                elif(str(parameter[3]) == 'dimm_domain1'):
                                        dimm_select = get_temp_4bh_mem_domain1
                                        return PASS, function, cpu_select, dimm_select
                                elif(str(parameter[3]) == 'all'):
                                        dimm_select = 'all'
                                        return PASS, function, cpu_select, dimm_select
                                else:
                                        print'dimm_select parameter in correct , please refer to usage.'
                                        return ERROR
                        else:
                                print' Check parameter cpu_select settings incorrect !'
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
sts, function, cpu_select, dimm_select = parameter_check(sys.argv)

if(sts == PASS):
        if(function == get_temp_4bh_standard ):
		if(dimm_select == 'all'):
	                cup_temp_arry, mem_temp_arry = get_cpu_mem_temp_4bh_py(ipmi, get_temp_4bh_all_cpu, cpu_select, get_temp_4bh_mem_domain0, function)
        	        cup_temp_arry, mem_temp_arry = get_cpu_mem_temp_4bh_py(ipmi, get_temp_4bh_no_cpu , cpu_select, get_temp_4bh_mem_domain1, function)
		else:
			cup_temp_arry, mem_temp_arry = get_cpu_mem_temp_4bh_py(ipmi, get_temp_4bh_all_cpu, cpu_select, dimm_select, function)

        elif(function == get_temp_4bh_extended ):
		if(dimm_select == 'all'):
	                cup_temp_arry, mem_temp_arry = get_cpu_mem_temp_4bh_py(ipmi, get_temp_4bh_all_cpu, cpu_select, get_temp_4bh_mem_domain0, function)
        	        cup_temp_arry, mem_temp_arry = get_cpu_mem_temp_4bh_py(ipmi, get_temp_4bh_no_cpu , cpu_select, get_temp_4bh_mem_domain1, function)

		else:
                	cup_temp_arry, mem_temp_arry = get_cpu_mem_temp_4bh_py(ipmi, get_temp_4bh_all_cpu, cpu_select, dimm_select, function)

        else:
                print'Please Try again...'

else:
        print' Please Try again...'

