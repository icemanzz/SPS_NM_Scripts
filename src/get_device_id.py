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
sys.path.append('../')
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



def get_device_id_py(ipmi):
     netfn, get_did_raw = get_did_raw_to_str_py()
     # Send Get DID to ME
     rsp = send_ipmb_aardvark(ipmi , netfn , get_did_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), App )
     if(sts != SUCCESSFUL ):
         return ERROR
     # Analyst get did resp data format
     # Get Major Version = resp byte4 bits[6:0]
     DEBUG('Get Major Version:')
     marjor_version    = get_bits_data_py( ord(rsp[3]) , 0 , 7)
     DEBUG('get_me_device_id : Marjor_version = %d' %marjor_version)
     # Get Device Available bit : byte4 bit[7] = 1 = device in boot loader mode. = 0 = normal operation mode.
     available_bit     = get_bits_data_py( ord(rsp[3]) , 7 , 1)
     DEBUG('get_me_device_id : Available Bit = %d' % available_bit)
     # Get Minor version (byte5 bit[7:4]) and Milestone version (byte5 bits[3:0])number
     milestone_version     = get_bits_data_py( ord(rsp[4]) , 0 , 4)
     DEBUG('get_me_device_id : milestone_version = %d' %milestone_version)
     minor_version         = get_bits_data_py( ord(rsp[4]) , 4 , 4)
     DEBUG('get_me_device_id : minor_version = %d' %minor_version)
     # Get Build version number byte14=A.B and byte15 bit[7:4] =C, build version = 100A+10B+C
     build_version_AB  = get_bits_data_py( ord(rsp[13]) , 0 , 8)
     DEBUG('get_me_device_id : build_version_AB = %d' %build_version_AB)
     build_version_C   = get_bits_data_py( ord(rsp[14]) , 4 , 4)
     DEBUG('get_me_device_id : build_version_C Bit = %d' %build_version_C)
     sps_version = format(marjor_version, '02x') + '.' + format(minor_version, '02x') + '.' + format(milestone_version, '02x') + '.' + format(build_version_AB,'02x')+format(build_version_C, 'x')
     DEBUG('Current SPS FW version = ' + sps_version )
     # Get byte11 bit[7:0] platform SKU
     platform = get_bits_data_py( ord(rsp[10]) , 0 , 8)
     DEBUG('get_me_device_id : platform = %d' %platform)
     # Get byte13 bit[3:0] DCMI version, bytes13 bit[7:4] = NM version
     nm = get_bits_data_py( ord(rsp[12]) , 0 , 4)
     DEBUG('get_me_device_id : nm = %d' %nm)
     dcmi   = get_bits_data_py( ord(rsp[12]) , 4 , 4)
     DEBUG('get_me_device_id : dcmi = %d' %dcmi)
     # Get byte16 bit[1:0] image flag
     image = get_bits_data_py( ord(rsp[15]) , 0 , 2)
     DEBUG('get_me_device_id : image_sts = %d' %image)

     sts = PASS

     return sts, sps_version, platform , dcmi , nm , image


def usage():
        # Description of how to use this script
        print' Useage $ sudo python get_device_id.py [delay_time (sec)] [loop_number]'
	print' ex: sudo python get_device_id.py 1 100'

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

# Initial aardvark
ipmi = aardvark_ipmi_init(target_me_addr, target_me_bridge_channel)

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
	print 'Start to Send Get Device ID..'
        while loop_number :
		sts, sps_version, platform, dcmi, nm, image  = get_device_id_py(ipmi)
                # Add delay time 5 secs to make sure me go back to stable mode
                time.sleep(delay_time)
		# Show Result
		print('SPS Version = '+ sps_version)
		print('platform = %d' %platform  )
		print('dcmi =%d' %dcmi)
		print('nm = %d' %nm)
		print('image = %d' %(image))

		if( loop_number == 'loop' ):
			loop_number = True
		else:
			loop_number = loop_number -1

                if(sts == ERROR ):
                        loop_number = False
                        break
else:
        print' Done! '

