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




## Function : Netfun: 0x30 , CMD :0x26H, MESDC Get Version cmd
def mesdc_get_version_py(ipmi):
     netfn, mesdc_26h_raw = mesdc_26h_raw_to_str_py()
     # Send MESDC 0x26h with command option
     rsp = send_ipmb_aardvark(ipmi , netfn , mesdc_26h_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), Controller_OEM )
     if(sts != SUCCESSFUL ):
         return ERROR
     print('mesdc_get_version_py : fwsts1 HFS = 0x%x%x%x%x' %(ord(rsp[15]),ord(rsp[14]) ,ord(rsp[13]) ,ord(rsp[12])))
     print('mesdc_get_version_py : fwsts2 = 0x%x%x%x%x' %(ord(rsp[19]),ord(rsp[18]) ,ord(rsp[17]) ,ord(rsp[16])))

     # Response byte 0
     current_status    = get_bits_data_py( ord(rsp[12]) , 0 , 4)
     DEBUG('mesdc_get_version_py : current_status = %d' %current_status)
     manufacture_mode    = get_bits_data_py( ord(rsp[12]) , 4 , 1)
     DEBUG('mesdc_get_version_py : manufacture_mode = %d' %manufacture_mode)
     fpt_bad    = get_bits_data_py( ord(rsp[12]) , 5 , 1)
     DEBUG('mesdc_get_version_py : fpt_bad = %d' %fpt_bad)
     operation_state1    = get_bits_data_py( ord(rsp[12]) , 6 , 2)
     # Response byte 1
     operation_state2    = get_bits_data_py( ord(rsp[13]) , 0 , 1)
     operation_state     = operation_state2*4 + operation_state1
     DEBUG('mesdc_get_version_py : operation_state = %d' %operation_state)
     init_complete       = get_bits_data_py( ord(rsp[13]) , 1 , 1)
     DEBUG('mesdc_get_version_py : init_complete = %d' %init_complete)
     recv_fault       = get_bits_data_py( ord(rsp[13]) , 2 , 1)
     DEBUG('mesdc_get_version_py : recv_fault = %d' %recv_fault)
     update_in_process       = get_bits_data_py( ord(rsp[13]) , 3 , 1)
     DEBUG('mesdc_get_version_py : update_in_process = %d' %update_in_process)
     error_code       = get_bits_data_py( ord(rsp[13]) , 4 , 4)
     DEBUG('mesdc_get_version_py : error_code = %d' %error_code)
     # Response byte 2
     operating_mode       = get_bits_data_py( ord(rsp[14]) , 0 , 4)
     DEBUG('mesdc_get_version_py : operating_mode = %d' %operating_mode)
     me_reset_count       = get_bits_data_py( ord(rsp[14]) , 4 , 4)
     DEBUG('mesdc_get_version_py : me_reset_count = %d' %me_reset_count)
     # Response byte 3
     fd0v_status       = get_bits_data_py( ord(rsp[15]) , 0 , 1)
     DEBUG('mesdc_get_version_py : fd0v_status = %d' %fd0v_status)
     cpu_dbg_policy       = get_bits_data_py( ord(rsp[15]) , 1 , 1)
     DEBUG('mesdc_get_version_py : cpu_dbg_policy = %d' %cpu_dbg_policy)
     sku_vio_status       = get_bits_data_py( ord(rsp[15]) , 2 , 1)
     DEBUG('mesdc_get_version_py : sku_vio_status = %d' %sku_vio_status)
     current_bios_region       = get_bits_data_py( ord(rsp[15]) , 3 , 1)
     DEBUG('mesdc_get_version_py : current_bios_region = %d' %current_bios_region)
     d0i3       = get_bits_data_py( ord(rsp[15]) , 7 , 1)
     DEBUG('mesdc_get_version_py : d0i3 = %d' %d0i3)
     # Response byte 5
     eop        = get_bits_data_py( ord(rsp[17]) , 3 , 1)
     DEBUG('mesdc_get_version_py : EOP = %d' %eop)

     sts = PASS

     return sts, rsp, current_status, operation_state , eop



def usage():
        # Description of how to use this script
        print' Useage $ sudo python mesdc_26h_get_version.py [delay_time] [loop_number]'
        print' ex: sudo python mesdc_26h_get_version.py 1 100'

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
#ipmi = aardvark_ipmi_init(target_me_addr, target_me_bridge_channel)

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
        print 'Start to Send MESDC 0x26h Get Version Cmd...'
        while loop_number :
		# Send IPMB
		sts, rsp, current_status, operation_state , eop = mesdc_get_version_py(ipmi)
                # Add delay time
                time.sleep(delay_time)
                # Show Result
                print('SPS Current_Status = '+ str(current_status))
                print('SPS Operation_State ='+ str(operation_state))
                print('EOP =' + str(eop))

                if( loop_number == 'loop' ):
                        loop_number = True
                else:
                        loop_number = loop_number -1

                if(sts == ERROR ):
                        loop_number = False
                        break
else:
        print' Done! '

