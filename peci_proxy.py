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
        print' Useage $ sudo python peci_proxy.py [function_parameter] [cpu_addr] [interface] [select_parameter]'
        print' [function_parameter] = ping/get_temp/rdpkgconfig/'
        print' [cpu] = cpu_addr with peci interface select'
        print' [interface] = 0 (fallback), = 1 (inband) = 2 (peci wire)'
        print' [select_parameter] = index + parameter'
        print' [fuction_parameter] = get_temp + [cpu_id] = 0 (cpu0)/ 1 (cpu1)/ 2(cpu2) /3 (cpu3)'
        print' [fuction_parameter] = rdpkgconfig + [cpu_addr] + [select_parameter] = command index'
        print' example of send get cpu0 temp via Inband peci: $ sudo python peci_proxy.py get_temp 0 0'
        print' example of read : $  sudo python peci_proxy.py rdpkgconfig 0x30  '
        return

## Function : Calculate current CPU Die Temperature value via GetTemp() PECI proxy cmd
def get_cpu_temp_py(ipmi, cpu_id, peci_interface):
     if(cpu_id == CPU0):
         PECI_CLIENT_ADDR = peci_40h_client_addr_cpu0
     elif(cpu_id == CPU1):
         PECI_CLIENT_ADDR = peci_40h_client_addr_cpu1
     elif(cpu_id == CPU2):
         PECI_CLIENT_ADDR = peci_40h_client_addr_cpu2
     elif(cpu_id == CPU3):
         PECI_CLIENT_ADDR = peci_40h_client_addr_cpu3
     else:
         DEBUG('ERROR!!!! cpu_id out of range')
         return ERROR
     # Prepare GetTemp PECI raw data aray
     raw_peci = peci_raw_get_temp()
     # Send GetTemp via ME RAW PECI proxy: Write length = 1 byte , Read_Length = 2 bytes
     resp = send_raw_peci_py(ipmi , PECI_CLIENT_ADDR, peci_interface, 1, 2, raw_peci )
     if(resp == ERROR):
         DEBUG('ERROR!!! send_raw_peci(): respond data error')
         return ERROR
     # Ananlyst GetTemp Real value: GET PECI RESP DATA Byte[N:5] value, total 2 bytes = Read_Length
     get_temp_resp = calculate_byte_value_py(resp, 5, 2)
     # Transfer data to 2's complement value 4 bytes = 16 bits
     Tmargin = two_complement(get_temp_resp , 16)
     #  Tmargin is the DTS offset value to Tprohot.The resulotion is 1/64 degress C
     Tmargin = abs(( Tmargin / 64))
     print('PECI GetTemp() = Tmargin = %6d' %Tmargin)
     # Get Tprochot value
     # Prepare RdpkgConfig , index 16 , Thermal Target for Tjmax value
     raw_peci = peci_raw_rdpkgconfig(0, 16, 0, 0 )
     # Send GetTemp via ME RAW PECI proxy: Write length = 5 byte , Read_Length = 5 bytes
     resp = send_raw_peci_py(ipmi, PECI_CLIENT_ADDR, peci_interface, 5, 5, raw_peci )
     if(resp == ERROR):
         DEBUG('ERROR!!! send_raw_peci(): respond data error')
         return ERROR
     # Calculate Tjmax value Byte8 of PECI resp data , total 1 byte
     Tjmax = calculate_byte_value_py(resp, 8, 1)
     print('CPU0 Tjmax = %6d' %Tjmax)
     # Calculate current CPU Die Temperature = Tjmax - Tmargin
     CPU_Temperature = Tjmax - Tmargin
     print('Current CPU Die Temperature = %6d' %CPU_Temperature )

     return CPU_Temperature

# Define Get PECI client addr
def get_peci_client_addr(cpu_id):
     if(cpu_id == CPU0):
         PECI_CLIENT_ADDR = peci_40h_client_addr_cpu0
     elif(cpu_id == CPU1):
         PECI_CLIENT_ADDR = peci_40h_client_addr_cpu1
     elif(cpu_id == CPU2):
         PECI_CLIENT_ADDR = peci_40h_client_addr_cpu2
     elif(cpu_id == CPU3):
         PECI_CLIENT_ADDR = peci_40h_client_addr_cpu3
     else:
         DEBUG('ERROR!!!! cpu_id out of range')
         return ERROR

     return PECI_CLIENT_ADDR



## Define Input parameters lenth check
def parameter_check(parameter):
        if(len(parameter) < 4  ):
                print'input parameter error, please check usage as below. '
                usage()
                return ERROR
        else:
                if(str(parameter[1]) == 'get_temp' ):
                        if( int(parameter[2]) < 0   ):
                                print' select parameter input error , please input a number between 0~2 , as below usage'
                                usage()
                                return ERROR
                        else:
                                print ' check run usage parameters input is PASS'
                                function = 'get_temp'
                                cpu_addr = int(parameter[2], 16)
				interface = int(parameter[3])
                                return PASS, function, cpu_addr , interface , None
                elif(str(parameter[1]) == 'rdpkgconfig'):
                        if(int(parameter[2]) < 0 ):
                                print ' check read usage parameters input is PASS'
                                function = 'rdpkgconfig'
                                cpu_addr = int(parameter[2], 16)
				interface = int(parameter[3])
				index = int(parameter[4])
                                return PASS, function, cpu_addr, interface, index
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
sts, function, cpu_addr, interface , index = parameter_check(sys.argv)

if(sts == PASS):
        if(function == 'get_temp'):
                cpu_temp = get_cpu_temp_py(ipmi, cpu_addr, interface )
                if(sts == ERROR):
                        print('Send raw PECI cmd fail !!!')
                else:
			print('CPU temperature = %2d' %cpu_temp)
                        print('Send raw PECI cmd successfully !')

        elif(function == 'rdpkgconfig'):
		# Get Tprochot value
		PECI_CLIENT_ADDR = get_peci_client_addr(cpu_addr)
     		# Prepare RdpkgConfig , index 16 , Thermal Target for Tjmax value
		raw_peci = peci_raw_rdpkgconfig(0, index, 0, 0 )
     		# Send GetTemp via ME RAW PECI proxy: Write length = 5 byte , Read_Length = 5 bytes
		resp = send_raw_peci_py(ipmi, PECI_CLIENT_ADDR, peci_interface, 5, 5, raw_peci )
		if(resp == ERROR):
			print('ERROR!!! respond data error')


        else:
                print'Please Try again...'

else:
        print' Please Try again...'

