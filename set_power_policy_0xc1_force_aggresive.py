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

## Define Domain check function
def domain_check(parameter):
        if(parameter == 'platform_ac'):
                domain = 0
                sts = PASS
        elif(parameter == 'cpu'):
                domain = 1
                sts = PASS
        elif(parameter == 'mem'):
                domain = 2
                sts = PASS
        elif(parameter == 'platform_dc'):
                domain = 3
                sts = PASS
        elif(parameter == 'hpio'):
                domain = 4
                sts = PASS
        else:
                domain = ERROR
                sts = ERROR
        return sts, domain


## Define policy id check function
def policy_id_check(policy_id):
        if( 0 <= policy_id <= 16 ):
                sts = PASS
        else:
		print'Error , policy_id out of range '
                policy_id = ERROR
                sts = ERROR
        return sts, policy_id

## Define cap value check function
def cap_range_check(ipmi, domain ,cap_value, correction_time):
	# Correction time unit is mini second
	correction_time = correction_time*1000
	# Read Power Draw Range and Correction time via 0xC9h cmd
	max_draw_range, min_draw_range, min_correction_time, max_correction_time = get_platform_power_draw_range_py( ipmi, domain , 0, 1, 0)
	if(max_draw_range == ERROR ):
		print('Get Platform Power Draw Range Error: data not exist')
		sts = ERROR
		correction_time = ERROR
		cap_value = ERROR
	else:
		print(' max_draw_range = %2d' %max_draw_range)
		print(' min_draw_range = %2d' %min_draw_range)
                print(' max_correction_time = %2d' %max_correction_time)
                print(' min_correction_time = %2d' %min_correction_time)
        	if( (min_draw_range <= cap_value <= max_draw_range) or cap_value == 0 ):
			if( min_correction_time <= correction_time <= max_correction_time):
                		sts = PASS
			else:
				print'Error , correction_time out of node manager max-min correction time range '
                        	cap_value = ERROR
                        	correction_time = ERROR
                        	sts = ERROR
        	else:
                	print'Error , cap_value out of node manager power draw range '
                	cap_value = ERROR
			correction_time = ERROR
                	sts = ERROR

        return sts, cap_value , correction_time


## Define Domain check function
def switch_check(switch):
        if(switch == 'on'): # enable and add
                enable_switch = 1
		create_switch = 1
                sts = PASS
        elif(switch == 'off'): # disable and remove
                enable_switch = 0
		create_switch = 0
                sts = PASS
	else:
		switch = ERROR
		sts = ERROR

        return sts, enable_switch, create_switch

## _Main_ ##

# Description of how to use this script
print'/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
print' Useage $ sudo python set_power_policy_0xc1.py [domain_parameter] [policy_id] [limit_power_value] [correction_time] [on/off]'
print' [domain_parameter] = platform_ac/cpu/mem/platform_dc/hpio/'
print' [policy_id] = 0, 1, 2, 3, ...., mex = 16 , policy_id = 0 by default be occupied by HW protection domain.'
print' [limit_power_value = 0 , 1 , 2, ..... ]'
print' [correction_time = 1 , 2, 3, .....  , unit is second]'
print' [on/off] = on , off ,  on = enable and add policy , off = disable and remove policy'
print' example $ sudo python set_power_policy_0xc1.py platform_ac 3 200 6 on'
print'////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'

# Initial aardvark
ipmi = aardvark_ipmi_init(target_me_addr, target_me_bridge_channel)

# Check input parameters
sts, domain = domain_check(str(sys.argv[1]))
sts, policy_id = policy_id_check(int(sys.argv[2]))
sts, cap_value, correction_time = cap_range_check(ipmi, domain, int(sys.argv[3]), int(sys.argv[4]))
sts, enable_switch, create_switch = switch_check(str(sys.argv[5]))

if(sts == PASS):
	print'Set power limit %2d watts in %s, correction_time = %2d seconds' % (int(sys.argv[3]) , str(sys.argv[1]), int(sys.argv[4]))
	# Set Power Capping via 0xC1h cmd
	sts = set_nm_power_policy_py(ipmi, domain, enable_switch , policy_id , c1h_no_policy_trigger, create_switch , c1h_force_aggressive, c1h_presistent, c1h_alert_enable, c1h_shutdown_disable, AC_power_side, cap_value, correction_time, c1h_trigger_limit_null, c1h_minimum_report_period )

else:
        # Description of how to use this script
        print' Useage $ sudo python set_power_policy_0xc1.py [domain_parameter] [policy_id] [limit_power_value] [correction_time] [on/off]'
        print' [domain_parameter] = platform_ac/cpu/mem/platform_dc/hpio/'
	print' [policy_id] = 0, 1, 2, 3, ...., mex = 16 , policy_id = 0 by default be occupied by HW protection domain.'
        print' [limit_power_value = 0 , 1 , 2, ..... ]'
        print' [correction_time = 1 , 2, 3, .....  , unit is second]'
	print' [on/off] = on , off ,  on = enable and add policy , off = disable and remove policy'
        print' example $ sudo python set_power_policy_0xc1.py platform_ac 3 200 6 on'

