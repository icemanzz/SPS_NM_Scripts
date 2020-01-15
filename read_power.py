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

## Define Get Power Reading
def read_power(ipmi, domain):
        # Read Platform Power via 0xC8h cmd
        power_average_stress = read_power_py(ipmi , global_power_mode, domain ,AC_power_side, 0 )
        if(power_average_stress == ERROR):
                sts = ERROR
                print('Platform power reading error!!!')
                return sts

        else:
                sts = PASS
                print(power_average_stress)

	return sts


def usage():
        # Description of how to use this script
        print' Useage $ sudo python read_power.py [domain_parameter]'
        print' [domain_parameter] = platform_ac/cpu/mem/platform_dc/hpio/'

        return



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

## Define Input parameters lenth check
def parameter_check(parameter):
        if(len(parameter) != 2  ):
                usage()
                sts =ERROR
                return ERROR
	else:
		return PASS


## _Main_ ##

# Initial aardvark
ipmi = aardvark_ipmi_init(target_me_addr, target_me_bridge_channel)

# Check domain parameter
sts = parameter_check(sys.argv)
if(sts == PASS):
	sts, domain = domain_check(str(sys.argv[1]))
else:
	sts = ERROR

if(sts == PASS):
	print'Get power reading in %s' %str(sys.argv[1])
	run = True
	while run:
		sts = read_power(ipmi, domain)
		if(sts == ERROR ):
			run = False
			break
else:
	print' Done! '

