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
        print' Useage $ sudo python hw_protection.py [function_parameter] [ select_parameter ]'
        print' [function_parameter] = psu_check/limit/k_coefficiency'
        print' [select_parameter] = psu_addr/limit_value/k_coefficiency_vaule'
        print' example of hw_protection PSU/HSC cmd capability check:$ sudo python hw_protection.py psu_check 0xb0'
        print' example of hw_protection limit via power draw range:$ sudo python hw_protection.py limit 150'
        print' example of hw_protection limit via PSU K-Coefficiency:$ sudo python hw_protection.py k_coefficiency 10'

        return
## Define Input parameters lenth check
def parameter_check(parameter):
        if( len(parameter) != 3  ):
                print'input parameter error, please check usage as below. '
                usage()
                return ERROR
        else:
                if(str(parameter[1]) == 'psu_check' ):
                	if(parameter[2] > 0 ):
                                psu_addr = int(parameter[2], 16)
                        	print ' check hw_protection psu_check parameters input is PASS'
				function = 'psu_check'
				select = psu_addr
                        	return PASS, function, select
                	else:
				print' Check parameter PSU address incorrect !'
				usage()
                        	return ERROR

                elif(str(parameter[1]) == 'limit'):
                        if(int(parameter[2]) >= 0 ):
                                limit_value = int(parameter[2])
                                print ' check hw_protection limit usage parameters input is PASS'
                                function = 'limit'
                                select = limit_value
                                return PASS, function, select
                        else:
                                print' Check limit value incorrect !'
                                usage()
                                return ERROR


                elif(str(parameter[1]) == 'k_coefficiency'):
                        if(int(parameter[2]) >= 0 ):
                                k_coeff = int(parameter[2])
                                print ' check hw_protection k_coefficiency usage parameters input is PASS'
                                function = 'k_coefficiency'
                                select = k_coeff
                                return PASS, function, select
                        else:
                                print' Check limit value incorrect !'
                                usage()
                                return ERROR

                else:
                        print('input parameter error, please check usage as below.')
                        usage()
                        return ERROR

                return ERROR


## Define Check PSU Status Register function
def psu_check(ipmi, psu_addr):
     # Send PMbus Proxy cmd to Read all of PSU status registers
#     write_len = 1
#     read_len = 7
#     bus = d9h_sml1
#     target_addr = int(psu_addr)
#     pmbus_cmd_aray = [PMBUS_READ_EOUT]
#     rsp = send_raw_pmbus_write_cmd_extend_py(ipmi, d9h_trans_type_block_read , d9h_pec_report, d9h_pec_en, bus , target_addr , 0 , 0 , 0 , d9h_trans_potocol_pmbus , write_len , read_len , pmbus_cmd_aray)
     write_len = 1
     read_len = 7
     bus = d9h_sml1
     target_addr = int(psu_addr)
     pmbus_cmd = PMBUS_READ_EOUT
     rsp = send_raw_pmbus_cmd_extend_py(ipmi, d9h_trans_type_block_read, d9h_pec_report, d9h_pec_en, bus , target_addr , 0 , 0 , 0 , d9h_trans_potocol_pmbus , write_len , read_len , pmbus_cmd)

     # Check pmbus rsp  data
     if(rsp == ERROR):
             print('ERROR!!! send pmbus error ! respond data error')
             return ERROR
     else:
             print('PSU Read_Ein 0x87H: Block_Count= %2X, E_LOW=%2X, E_High=%2X, RollOver=%2X, S1=%2X, S2=%2X, S3=%2X' %( ord(rsp[4]), ord(rsp[5]), ord(rsp[6]), ord(rsp[7]), ord(rsp[8]), ord(rsp[9]), ord(rsp[10]) ) )
             return SUCCESSFUL



## _Main_ ##
# This test base on NM_014 : Fast NM Limiting  test process
# Note :  1. XML file set : Configuation -> Node Manager -> NM Fast Limiting -> NM Fast Limiting Enable = True , Poling Interval = 10msec
# Note :  2. PSU PMbus FW support Read_Eout = 0x87h cmd
# Note:   3. Platform Power Source from PSU or HSC with 100mesc polling reate in SDR (  BMC is not support this function )

# Initial aardvark
ipmi = aardvark_ipmi_init(target_me_addr, target_me_bridge_channel)

# Check input parameters
sts, function, select = parameter_check(sys.argv)

if(sts == PASS):
        if(function == 'psu_check'):
		# Check PSU/HSC support 0x87h Read_Ein cmd
		sts = psu_check(ipmi, select)
                if(sts == SUCCESSFUL):
                        print'psu/hsc 0x87H read_ein check command Pass'
                else:
                        print 'psu/hsc 0x87H read_ein command Fail'

        elif(function == 'limit'):
		# Read DC side Power Draw Range and Correction time via 0xC9h cmd
		max_draw_range, min_draw_range, min_correction_time, max_correction_time = get_platform_power_draw_range_py( ipmi, hw_protection_domain , 0, 1, 0)
		#Set Power Draw range via 0xCBh cmd in HW protection domain :  maximum power drange range in domain 3 = 80% of power_average_stress
		sts = set_nm_power_draw_range_py(ipmi, cbh_hw_protection_domain , min_draw_range , select )
		if(sts == ERROR):
			print('set_nm_power_draw_range 0xCBh fail !!!')
		else:
			# Read DC side Power Draw Range and Correction time via 0xC9h cmd Again
                	max_draw_range, min_draw_range, min_correction_time, max_correction_time = get_platform_power_draw_range_py( ipmi, hw_protection_domain , 0, 1, 0)
			print('Set Maximum DC side Power = %2d' %max_draw_range)
			print('Set Power Draw range for HW protection function Successfully !')

        elif(function == 'k_coefficiency'):
                # Get CUPS Load Factor Result via 0x65h cmd
                print' Get CUPS Load Factors Result :'
                rsp = set_hw_protection_coefficiency_py( ipmi, select)
                if(rsp == ERROR):
                        print'Set K coefficiency Fail'
                else:
                        print 'Set K Coefficiency Pass'

        else:
                print'Please Try again...'

else:
        print' Please Try again...'


