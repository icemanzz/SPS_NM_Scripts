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
        print' Useage $ sudo python cups.py [function_parameter]'
        print' [function_parameter] = sdr/index/load/workload'
        print' example of cups sdr list: $ sudo python cups.py sdr'
        print' example of get cups index: $ sudo python cups.py index'
        print' example of get cups load_factors: $ sudo python cups.py load'
        print' example of get cups workload: $ sudo python cups.py workload'

        return

## Define Input parameters lenth check
def parameter_check(parameter):
        if( len(parameter) != 2  ):
                print'input parameter error, please check usage as below. '
                usage()
                return ERROR
        else:
                if(str(parameter[1]) == 'sdr' ):
                        print ' check CUPS sdr usage parameters input is PASS'
                        function = 'sdr'
                        return PASS, function
                elif(str(parameter[1]) == 'index'):
                        print ' check CUPS index usage parameters input is PASS'
			function = cups_65h_cups_index
                        return PASS, function
                elif(str(parameter[1]) == 'load'):
                        print ' check CUPS load factors usage parameters input is PASS'
			function = cups_65h_dynamic_load_factors
                        return PASS, function
                elif(str(parameter[1]) == 'workload'):
                        print ' check CUPS workload usage parameters input is PASS'
			function = 'workload'
                        return PASS, function
                else:
                        print('input parameter error, please check usage as below.')
                        usage()
                        return ERROR

                return ERROR



## _Main_ ##
# Initial aardvark
ipmi = aardvark_ipmi_init(target_me_addr, target_me_bridge_channel)

# Check input parameters
sts, function = parameter_check(sys.argv)

if(sts == PASS):
        if(function == 'sdr'):
                # send get CUPS CPU Workload sdr reading cmd
		cups_core_workload = get_sensor_reading_py(ipmi, cups_core)
		if(cups_core_workload == ERROR):
			print('CUPS core Workload Sensor number: %2s not exist' %cups_core_workload)
		else:
			print('CPU CORE CUPS Workload SDR Reading = %2d' %cups_core_workload)

                # send get CUPS Memory Workload sdr reading cmd
                cups_mem_workload = get_sensor_reading_py(ipmi, cups_mem)
                if(cups_mem_workload == ERROR):
                        print('CUPS mem Workload Sensor number: %2s not exist' %cups_mem_workload)
                else:
                        print('CUPS mem Workload SDR Reading = %2d' %cups_mem_workload)

                # send get CUPS IO Workload sdr reading cmd
                cups_io_workload = get_sensor_reading_py(ipmi, cups_io)
                if(cups_io_workload == ERROR):
                        print('CUPS io Workload Sensor number: %2s not exist' %cups_io_workload)
                else:
                        print('CUPS io Workload SDR Reading = %2d' %cups_io_workload)

        elif(function == cups_65h_cups_index):
                # Get CUPS Index Result via 0x65h cmd
                print' Get CUPS Index Result :'
		cups_index = get_cups_data_65h_py( ipmi, cups_65h_cups_index)
                print' cups_index = %d' %cups_index

        elif(function == cups_65h_dynamic_load_factors):
                # Get CUPS Load Factor Result via 0x65h cmd
                print' Get CUPS Load Factors Result :'
                cpu_load_factor, mem_load_factor, io_load_factor = get_cups_data_65h_py( ipmi, cups_65h_dynamic_load_factors)
                print' CPU Load Factor = %d' %cpu_load_factor
                print' MEM Load Factor = %d' %mem_load_factor
                print' IO  Load Factor = %d' %io_load_factor

        elif(function == 'workload'):
                # send get CUPS CPU Workload sdr reading cmd
                cups_core_workload = get_sensor_reading_py(ipmi, cups_core)
                if(cups_core_workload == ERROR):
                        print('CUPS core Workload Sensor number: %2s not exist' %cups_core_workload)
                else:
			cups_core_utilization = cups_core_workload*100/255
                        print('CPU CORE CUPS Workload Reading = %2d percentage' %cups_core_utilization)

                # send get CUPS Memory Workload sdr reading cmd
                cups_mem_workload = get_sensor_reading_py(ipmi, cups_mem)
                if(cups_mem_workload == ERROR):
                        print('CUPS mem Workload Sensor number: %2s not exist' %cups_mem_workload)
                else:
                        cups_mem_utilization = cups_mem_workload*100/255
                        print('CUPS mem Workload Reading = %2d percentage' %cups_mem_utilization)

                # send get CUPS IO Workload sdr reading cmd
                cups_io_workload = get_sensor_reading_py(ipmi, cups_io)
                if(cups_io_workload == ERROR):
                        print('CUPS io Workload Sensor number: %2s not exist' %cups_io_workload)
                else:
                        cups_io_utilization = cups_io_workload*100/255
                        print('CUPS io Workload Reading = %2d percentage' %cups_io_utilization)

        else:
                print'Please Try again...'

else:
        print' Please Try again...'



