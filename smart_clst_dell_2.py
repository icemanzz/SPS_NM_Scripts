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


## Function : SMART_001 Test Process: Verify SMART/CLST  function.
def SMART_001_AUTO(ipmi, psu_addr):

     # Prepare Package Thermal Status MSR0x1B1  : RdpkgConfig , index 0x14 
     raw_peci = peci_raw_rdpkgconfig(0, 20 , 0, 0 )
     # Send Package Thermal Status via ME RAW PECI proxy: Write length = 5 byte , Read_Length = 5 bytes
     resp = send_raw_peci_py(ipmi, peci_40h_client_addr_cpu0, peci_40h_interface_fall_back, 5, 5, raw_peci )
     if(resp == ERROR):
         print('ERROR!!! send_raw_peci(): respond data error')
         return ERROR
     #Check Thermal Status before SMART testing
     if(ord(resp[4]) != 0x40):
         print('ERROR!!! send_raw_peci(): PCU respond data error')
         return ERROR
     elif((ord(resp[5])!= 0) or (ord(resp[6])!= 0)):
         print(' send_raw_peci(): CPU Thermal status incorrect , probabaly already have thermal event happen before test.')
         #return ERROR

     # Read PSU Over Temperature Threshold value via PMbus Proxy
     write_len = 1
     read_len = 2
     bus = d9h_sml1
     target_addr = int(psu_addr)
     pmbus_cmd = PMBUS_READ_WRITE_OT_WARM_LIMIT
     # Send PMbus Proxy cmd to get current Over Temperature Threshold value
     rsp = send_raw_pmbus_cmd_extend_py(ipmi, d9h_trans_type_read_word, d9h_pec_report, d9h_pec_en, bus , target_addr , 0 , 8 , 1 , d9h_trans_potocol_pmbus , write_len , read_len , pmbus_cmd)
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR
     # Transfer value to real value is linear data format , X = Y*2^N
     # Calculate N : High Byte bit[7:3]
     N  = get_bits_data_py( ord(rsp[5]) , 3 , 5)
     # Transfer N data to 2's complement value
     N_2complement = two_complement(N , 5)
     # Calculate Y : High Byte bit[2:0]
     Y1  = get_bits_data_py( ord(rsp[5]) , 0 , 3)
     Y1  = Y1 * 256
     Y2  = ord(rsp[4])
     Y   = Y1 + Y2   
     # Calculate ot_warm value from rsp Byte[6:5] value, total 2 bytes
     default_ot_warm_high_byte = ord(rsp[5])
     default_ot_warm_low_byte = ord(rsp[4])
     default_ot_warm = Y*math.pow(2,N_2complement)
     print('Current default OT WARM temp value = %6d' %default_ot_warm) 
     # Run load on host system with PTU 100% loading
     print('/////////////////////////////////////////////////////////////////////////')
     print('Please run WinPTU stress tool...... wait 3 secs...')
     print('/////////////////////////////////////////////////////////////////////////')
     time.sleep(3)
     print('Read current heavy loading platform power......')
     # Read Platform Power via 0xC8h cmd
     power_average_stress = read_power_py(ipmi , global_power_mode, platform_domain,AC_power_side, 0 )
     if(power_average_stress == ERROR):
         print('Platform power reading error!!!')
         return ERROR
     # Power Reading OK
     print('Platform Power Reading OK')
     print('Currently Full Stress Average Platform Power Reading = %6d watts' %power_average_stress)     
     # Change OT_WARM_LIMIT value to 10 degree
     # Send PMbus Proxy cmd to write current Over Temperature Threshold value = 10 degree C
     write_len = 3
     read_len = 0
     pmbus_cmd_aray = [PMBUS_READ_WRITE_OT_WARM_LIMIT, 0x14 , 0xf8]
     rsp = send_raw_pmbus_write_cmd_extend_py(ipmi, d9h_trans_type_write_word, d9h_pec_report, d9h_pec_en, bus , target_addr , 0 , 0xa , 1 , d9h_trans_potocol_pmbus , write_len , read_len , pmbus_cmd_aray)
     # Check pmbus rsp  data
     if(rsp == ERROR):
         print('ERROR!!! send pmbus error ! respond data error')
         SMART_PSU_RECOVERY(ipmi,default_ot_warm_low_byte, default_ot_warm_high_byte, bus, target_addr )
         return ERROR
     # Delay 3 secs , make sure event triggered
     time.sleep(3)
     # Send Package Thermal Status again via ME RAW PECI proxy. Check event happen
     resp = send_raw_peci_py(ipmi, peci_40h_client_addr_cpu0, peci_40h_interface_fall_back, 5, 5, raw_peci )
     if(resp == ERROR):
         print('ERROR!!! send_raw_peci(): respond data error')
         SMART_PSU_RECOVERY(ipmi,default_ot_warm_low_byte, default_ot_warm_high_byte, bus, target_addr )
         return ERROR
     #Check Thermal Status to make sure CPU prohot event happen
     if(ord(resp[4]) != 0x40):
         print('ERROR!!! send_raw_peci(): PCU respond data error')
         SMART_PSU_RECOVERY(ipmi,default_ot_warm_low_byte, default_ot_warm_high_byte, bus, target_addr )
         return ERROR
     prochot_sts        = get_bits_data_py( ord(resp[5]) , 2 , 1)
     prochot_sts_log    = get_bits_data_py( ord(resp[5]) , 3 , 1)
     print('prochot_sts = %d , prochot_sts_log =%d ' %(prochot_sts, prochot_sts_log))
     if( (prochot_sts == 0) and (prochot_sts_log==0)):
         print('SMART/CLST Fail! No PROCHOT event happen after event triggered ')
         print('ERROR!!! send_raw_peci(): respond data error')
         print('ERROR!!! send_raw_peci(): PCU respond data error')
         SMART_PSU_RECOVERY(ipmi,default_ot_warm_low_byte, default_ot_warm_high_byte, bus, target_addr )
         return ERROR
     #Check ME limiting value in PL2, suppose should be 0 watts
     if(ord(resp[6]) != 0x80):
         print('ERROR!!!  PL2 limiting value unexpected')
         SMART_PSU_RECOVERY(ipmi,default_ot_warm_low_byte, default_ot_warm_high_byte, bus, target_addr )
         return ERROR
     #Restor PSU OT_WARM_LIMIT value to default, suppose PROHOC event should gone!
     # Send PMbus Proxy cmd to write current Over Temperature Threshold value =  default_ot_warm value
     SMART_PSU_RECOVERY(ipmi,default_ot_warm_low_byte, default_ot_warm_high_byte, bus, target_addr )
     # Check pmbus rsp  data
     if(rsp == ERROR):
         print('ERROR!!! send pmbus error ! respond data error')
         return ERROR 
     #Delay 30 secs for PSU restore , then check if System go back to normal
     print('Restore PSU back to defulat')
     time.sleep(3)
     power_average_cap = read_power_py(ipmi, global_power_mode , platform_domain, AC_power_side, 0)
     if(power_average_cap == ERROR):
         print('Platform power reading error  !!!')
         return ERROR
     if(power_average_cap < 0.8*power_average_stress):
         print ('ERROR!! After release SMART/CLST event, system no go back to normal')
         return ERROR

     return SUCCESSFUL


## Define CLST PSU Temperature test function
def clst(ipmi, psu_addr ,ot_temp):
     # Change OT_WARM_LIMIT value to ot_temp degree
     # Send PMbus Proxy cmd to write current Over Temperature Threshold value = 10 degree C
     write_len = 3
     read_len = 0
     bus = d9h_sml1
     target_addr = int(psu_addr)
     pmbus_cmd_aray = [PMBUS_READ_WRITE_OT_WARM_LIMIT, ot_temp , 0xf8]
     rsp = send_raw_pmbus_write_cmd_extend_py(ipmi, d9h_trans_type_write_word, d9h_pec_report, d9h_pec_en, bus , target_addr , 0 , 0xa , 1 , d9h_trans_potocol_pmbus , write_len , read_len , pmbus_cmd_aray)
     # Check pmbus rsp  data
     if(rsp == ERROR):
         print('ERROR!!! send pmbus error ! respond data error')
         return ERROR

     return SUCCESSFUL

## Define Clearing PSU Status Register function
def psu_clear_status(ipmi, psu_addr, psu_status_register):
     # Send PMbus Proxy cmd to clear PSU status registers
     write_len = 5
     read_len = 0
     bus = d9h_sml1
     target_addr = int(psu_addr)
     pmbus_cmd_aray = [PMBUS_PAGE_PLUS_WRITE, PMBUS_PAGE_PLUS_WRITE_BYTE_COUNT , PMBUS_PSU_ME_PAGE, psu_status_register , 0xff ] # 0xff means clear all of bits in this status register.
     rsp = send_raw_pmbus_write_cmd_extend_py(ipmi, d9h_trans_type_block_write , d9h_pec_report, d9h_pec_en, bus , target_addr , 0 , 0xa , 1 , d9h_trans_potocol_pmbus , write_len , read_len , pmbus_cmd_aray)
     # Check pmbus rsp  data
     if(rsp == ERROR):
         print('ERROR!!! send pmbus error ! respond data error')
         return ERROR

     return SUCCESSFUL

## Define Check PSU Status Register function
def psu_status(ipmi, psu_addr):
     # PMBUS_STATUS_REGISTERS
     PMBUS_STATUS_REGISTERS = [PMBUS_STATUS_WORD_79H, PMBUS_STATUS_IOUT_7BH, PMBUS_STATUS_INPUT_7CH, PMBUS_STATUS_TEMPERATURE_7DH, PMBUS_STATUS_FANS_81H]
     # Send PMbus Proxy cmd to Read all of PSU status registers
     write_len = 4
     #read_len = 2
     bus = d9h_sml1
     target_addr = int(psu_addr)
     #pmbus_cmd_aray = [PMBUS_PAGE_PLUS_READ, PMBUS_PAGE_PLUS_READ_BYTE_COUNT, PMBUS_PSU_ME_PAGE, psu_status_register ]
     for register in PMBUS_STATUS_REGISTERS:
     	pmbus_cmd_aray = [PMBUS_PAGE_PLUS_READ, PMBUS_PAGE_PLUS_READ_BYTE_COUNT, PMBUS_PSU_ME_PAGE, register ]
     	if(register == PMBUS_STATUS_WORD_79H):
     		read_len = 3
     	else:
     		read_len = 2
     	rsp = send_raw_pmbus_write_cmd_extend_py(ipmi, d9h_trans_type_block_wr_pro_call , d9h_pec_report, d9h_pec_en, bus , target_addr , 0 , 0xa , 1 , d9h_trans_potocol_pmbus , write_len , read_len , pmbus_cmd_aray)
     	# Check pmbus rsp  data
     	if(rsp == ERROR):
         	print('ERROR!!! send pmbus error ! respond data error')
         	return ERROR
     	else:
     		if(register == PMBUS_STATUS_WORD_79H):
     			print(' PSU STATUS 0x%2s : Low_Byte= %2X , High_Byte = %2X' %( format(register,'02x'), ord(rsp[5]), ord(rsp[6])) )
			psu_79h_cml          =  get_bits_data_py( ord(rsp[5]) , 1 , 1)
                        psu_79h_temperature  =  get_bits_data_py( ord(rsp[5]) , 2 , 1)
			psu_79h_vin_uv       =  get_bits_data_py( ord(rsp[5]) , 3 , 1)
			psu_79h_iout_oc      =  get_bits_data_py( ord(rsp[5]) , 4 , 1)
			psu_79h_fans         =  get_bits_data_py( ord(rsp[6]) , 2 , 1)
			psu_79h_input        =  get_bits_data_py( ord(rsp[6]) , 5 , 1)
			psu_79h_iout_pout    =  get_bits_data_py( ord(rsp[6]) , 6 , 1)
			psu_79h_vout         =  get_bits_data_py( ord(rsp[6]) , 7 , 1)
			print(' PSU STATUS 0x%2s , CML              = %d' %( format(register,'02x') , psu_79h_cml ))
                        print(' PSU STATUS 0x%2s , TEMPERATURE      = %d' %( format(register,'02x') , psu_79h_temperature ))
                        print(' PSU STATUS 0x%2s , VIN_UV           = %d' %( format(register,'02x') , psu_79h_vin_uv ))
                        print(' PSU STATUS 0x%2s , IOUT_OC          = %d' %( format(register,'02x') , psu_79h_iout_oc ))
                        print(' PSU STATUS 0x%2s , FANS             = %d' %( format(register,'02x') , psu_79h_fans ))
                        print(' PSU STATUS 0x%2s , INPUT            = %d' %( format(register,'02x') , psu_79h_input ))
                        print(' PSU STATUS 0x%2s , IOUT/POUT        = %d' %( format(register,'02x') , psu_79h_iout_pout ))
                        print(' PSU STATUS 0x%2s , VOUT             = %d' %( format(register,'02x') , psu_79h_vout ))

     		elif(register == PMBUS_STATUS_IOUT_7BH):
                        print(' PSU STATUS 0x%2s : status = %2X ' %( format(register,'02x'), ord(rsp[5]) ) )
                        psu_7Bh_pout_op_warning        =  get_bits_data_py( ord(rsp[5]) , 0 , 1)
                        psu_7Bh_pout_op_fault          =  get_bits_data_py( ord(rsp[5]) , 1 , 1)
                        psu_7Bh_iout_oc_warning        =  get_bits_data_py( ord(rsp[5]) , 5 , 1)
                        psu_7Bh_iout_oc_fault          =  get_bits_data_py( ord(rsp[5]) , 7 , 1)
                        print(' PSU STATUS 0x%2s , Pout OP warning  = %d' %( format(register,'02x') , psu_7Bh_pout_op_warning ))
                        print(' PSU STATUS 0x%2s , Pout OP fault    = %d' %( format(register,'02x') , psu_7Bh_pout_op_fault ))
                        print(' PSU STATUS 0x%2s , Iout OC warning  = %d' %( format(register,'02x') , psu_7Bh_iout_oc_warning ))
                        print(' PSU STATUS 0x%2s , IOUT_OC fault    = %d' %( format(register,'02x') , psu_7Bh_iout_oc_fault ))

                elif(register == PMBUS_STATUS_INPUT_7CH):
                        print(' PSU STATUS 0x%2s : status= %2X ' %( format(register,'02x'), ord(rsp[5]) ) )
                        psu_7Ch_pin_over_power_warning   =  get_bits_data_py( ord(rsp[5]) , 0 , 1)
                        psu_7Ch_iin_over_current_warning =  get_bits_data_py( ord(rsp[5]) , 1 , 1)
                        psu_7Ch_unit_off_ac_loss         =  get_bits_data_py( ord(rsp[5]) , 3 , 1)
                        psu_7Ch_vin_uv_fault             =  get_bits_data_py( ord(rsp[5]) , 4 , 1)
                        psu_7Ch_vin_uv_warning           =  get_bits_data_py( ord(rsp[5]) , 5 , 1)
                        print(' PSU STATUS 0x%2s , Pin over power warning          = %d' %( format(register,'02x') , psu_7Ch_pin_over_power_warning ))
                        print(' PSU STATUS 0x%2s , Iin over current warning        = %d' %( format(register,'02x') , psu_7Ch_iin_over_current_warning ))
                        print(' PSU STATUS 0x%2s , Unit off for insufficient input = %d' %( format(register,'02x') , psu_7Ch_unit_off_ac_loss ))
                        print(' PSU STATUS 0x%2s , Vin UV fault                    = %d' %( format(register,'02x') , psu_7Ch_vin_uv_fault ))
                        print(' PSU STATUS 0x%2s , Vin UV warning                  = %d' %( format(register,'02x') , psu_7Ch_vin_uv_warning ))

                elif(register == PMBUS_STATUS_TEMPERATURE_7DH):
                        print(' PSU STATUS 0x%2s : Low_Byte = %2X' %( format(register,'02x'), ord(rsp[5]) ) )
                        psu_7Dh_ot_warning        =  get_bits_data_py( ord(rsp[5]) , 6 , 1)
                        psu_7Dh_ot_fault          =  get_bits_data_py( ord(rsp[5]) , 7 , 1)
                        print(' PSU STATUS 0x%2s , OT warning       = %d' %( format(register,'02x') , psu_7Dh_ot_warning ))
                        print(' PSU STATUS 0x%2s , OT fault         = %d' %( format(register,'02x') , psu_7Dh_ot_fault ))

                elif(register == PMBUS_STATUS_FANS_81H):
                        print(' PSU STATUS 0x%2s : status = %2X' %( format(register,'02x'), ord(rsp[5]) ) )
                        psu_81h_fan2_warning      =  get_bits_data_py( ord(rsp[5]) , 4 , 1)
                        psu_81h_fan1_warning      =  get_bits_data_py( ord(rsp[5]) , 5 , 1)
                        psu_81h_fan2_fault        =  get_bits_data_py( ord(rsp[5]) , 6 , 1)
                        psu_81h_fan1_fault        =  get_bits_data_py( ord(rsp[5]) , 7 , 1)
                        print(' PSU STATUS 0x%2s , Fan2 warning     = %d' %( format(register,'02x') , psu_81h_fan2_warning ))
                        print(' PSU STATUS 0x%2s , Fan1 warning     = %d' %( format(register,'02x') , psu_81h_fan1_warning  ))
                        print(' PSU STATUS 0x%2s , Fan2 fault       = %d' %( format(register,'02x') , psu_81h_fan2_fault  ))
                        print(' PSU STATUS 0x%2s , Fan1 fault       = %d' %( format(register,'02x') , psu_81h_fan1_fault ))
		else:
			return ERROR

     return SUCCESSFUL


def usage():
        # Description of how to use this script
        print' Useage $ sudo python smart_clst.py [auto/samrt/clst/clear_psu]'
        print' exapmle auto : sudo python smart_clst.py auto [psu_addr]'
        print' exapmle clst : sudo python smart_clst.py clst [PSU slave address ] [Set PSU OT_Temperature] , OT_TEMP from 0 to Maximum 95 degree C '
        print'                $sudo python smart_clst.py clst 0xb0 10 '
        print' exapmle clear_status : sudo python smart_clst.py clear_status [PSU slave address] [PSU STATUS REGISTER,NOTE:0X79=STATUS_WORD,0X7B=STATUS_IOUT,0X7C=STATUS_INPUT,0X7D= STATUS_TEMPERATURE,0X81=STATUS_FANS]'
        print'                $sudo python smart_clst.py clst 0xb0 0x7D '
        print' exapmle status : sudo python smart_clst.py status [PSU slave address ]'
        print'                $sudo python smart_clst.py status 0xb0 '

	return

## Define Domain check function
def mode_check(parameter):
	if(len(parameter) < 2):
		usage()
		sts =ERROR
		return ERROR
        if(str(parameter[1]) == 'auto'):
                mode = 'auto'
                if(parameter[2] == None):
			usage()
                        sts = ERROR
                        return sts
		else:
			psu_addr = int(parameter[2], 16)
			sts = PASS
			return sts, mode, psu_addr, None
        elif(str(parameter[1]) == 'clst'):
                mode = 'clst'
                if(parameter[2] == None or parameter[3] == None):
			usage()
                        sts = ERROR
                        return sts
		else:
			psu_addr = int(parameter[2], 16)
			# Convert int value to hex stress , PSU Temp format : X= Y*2(-N) => 0xF8XX => X = (XX)/2
                	ot_temp = int_to_hex_string( int(parameter[3])*2 )
                	print('ot_temp settings = %2s' %ot_temp)
                	sts = PASS
			return sts, mode, psu_addr, ot_temp
        elif(str(parameter[1]) == 'clear_status'):
                mode = 'clear_status'
                if(parameter[2] == None or parameter[3] == None):
                        usage()
			sts = ERROR
			return sts
		else:
			psu_addr =  int(parameter[2], 16)
                	psu_status_register = parameter[3]
                	sts = PASS
                	return sts, mode, psu_addr, psu_status_register
        elif(str(parameter[1]) == 'status'):
                mode = 'status'
                if(parameter[2] == None):
                        usage()
                        sts = ERROR
                        return sts
                else:
                        psu_addr =  int(parameter[2], 16)
                        sts = PASS
                        return sts, mode, psu_addr, None

        else:
                sts = ERROR
                return sts



## _Main_ ##

# Initial aardvark
ipmi = aardvark_ipmi_init(target_me_addr, target_me_bridge_channel)


# Check input parameters
sts, mode, parameter2, parameter3 = mode_check(sys.argv)


# START TEST
if(sts == PASS):
	if(mode == 'auto'):
		sts = SMART_001_AUTO(ipmi, parameter2)
		if(sts == SUCCESSFUL):
			print'SMART_001 test Pass'
		else:
			print 'SMART_001 test Fail'

	elif(mode == 'clst'):
		sts = clst(ipmi, parameter2, parameter3)  ## parameter2 = psu_addr, parameter3= ot_temp
                if(sts == SUCCESSFUL):
                        print'clst psu command Pass'
                else:
                        print 'clst psu command Fail'

	elif(mode == 'clear_status'):
		sts = psu_clear_status(ipmi, parameter2, parameter3 )
                if(sts == SUCCESSFUL):
                        print'Clearing PSU Status Register Pass'
                else:
                        print 'Clearing PSU Status Register Fail'
        elif(mode == 'status'):
                sts = psu_status(ipmi, parameter2 )
                if(sts == SUCCESSFUL):
                        print'Check PSU Status Register Pass'
                else:
                        print 'Check PSU Status Register Fail'

	else:
		sts = ERROR

else:
        # Description of how to use this script
        print' Input parameters error!!! Please try again.'


