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
from config import *


##Function :  Send IPMB cmd via aardvark and return response data 
def send_ipmb_aardvark(ipmi , netfn, raw):
     DEBUG('Send IPMB raw cmd via Aardvark : raw 0x%x %s' % (netfn , raw))
     raw_bytes = array.array('B', [int(d, 0) for d in raw[0:]])
     rsp = ipmi.raw_command(lun, netfn, raw_bytes.tostring())
     DEBUG('Response Data: ' + ' '.join('%02x' % ord(d) for d in rsp))
     return rsp


## Function : 0x4BH, Get CPU and Memory Temperature
def get_cpu_mem_temp_4bh_py(ipmi, cpu_select,  cpu_set, mem_channel_set, request_format ):
     # Send 0x4Bh cmd
     netfn, get_cpu_mem_temp_4bh_raw =  get_cpu_mem_temp_4bh_raw_to_str_py( cpu_select, cpu_set, mem_channel_set, request_format )
     rsp = send_ipmb_aardvark(ipmi , netfn , get_cpu_mem_temp_4bh_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR
     # Decide which response byte is memory temp byte
     if(cpu_select == get_temp_4bh_no_cpu):
         read_offset = 5
         cpu_loop = 0
     else:
         read_offset = 9
         cpu_loop = 4

     if(request_format == get_temp_4bh_standard):
         cpu_temp_aray = []
         mem_temp_aray = []
         # Calculate temperature value from rsp value, total 1 bytes
         for i in range(0 , cpu_loop):
             cpu_temp_aray.append( calculate_byte_value_py(rsp, (i+5) , 1))
             if(cpu_temp_aray[i] == 255 ):
                 print'CPU%d temperture = %s' %( (i+cpu_set*4), 'Not Present' )
             else:
                 print'CPU%d temperture = %2d' %( (i+cpu_set*4), cpu_temp_aray[i] )

         for j in range(0, 4): # CPU 0~3
             for k in range(0, 4): # Channel 0~3
                 for l in range(0, 4): # DIMM 0~3
                     mem_temp_aray.append( calculate_byte_value_py(rsp, (read_offset + j*16 +  k*4 + l ), 1) )
                     if(mem_temp_aray[ 16*j + 4*k +l] == 255 ):
                         print'CPU%d , Channel%d , Dimm%d temperture = %s' %( (j+cpu_set*4), (k+mem_channel_set*4), l , 'Not Present' )
                     else:
                         print'CPU%d , Channel%d , Dimm%d temperture = %d' %( (j+cpu_set*4), (k+mem_channel_set*4), l , mem_temp_aray[ j*16 + k*4 + l ] )


     elif(request_format == get_temp_4bh_extended):
         cpu_temp_aray = []
         mem_temp_aray = []
         # Calculate temperature value from rsp value, total 1 bytes
         for i in range(0 , cpu_loop):
             cpu_temp_aray.append(  calculate_byte_value_py(rsp, (i+5), 1) )
             if(cpu_temp_aray[i] == 255 ):
                 print'CPU%d temperture = %s' %( (i+cpu_set*4), 'Not Present' )
             else:
                 print'CPU%d temperture = %2d' %( (i+cpu_set*4), cpu_temp_aray[i] )

         for j in range(0, 2): # CPU 0~3
             for k in range(0, 4): # Channel 0~3
                 for l in range(0, 8): # DIMM 0~7
                     mem_temp_aray.append( calculate_byte_value_py(rsp, (read_offset + j*32 +  k*8 + l), 1)  )
                     if(mem_temp_aray[32*j + 8*k + l] == 255 ):
                         print'CPU%d , Channel%d , Dimm%d temperture = %s' %( (j+cpu_set*4), (k+mem_channel_set*4), l , 'Not Present' )
                     else:
                         print'CPU%d , Channel%d , Dimm%d temperture = %d' %( (j+cpu_set*4), (k+mem_channel_set*4), l , mem_temp_aray[ j*32 + k*8 + l ] )


     return cpu_temp_aray, mem_temp_aray



## Function : 0xF0H, Set HW Protection Coefficiency
def set_hw_protection_coefficiency_py(ipmi, k_coefficiency ):
     # Coverter k_coefficiency int value to hex value for byte[4]- K Coefficiency %
     k_coeff = int_to_hex( k_coefficiency , 1 )
     netfn, f0h_set_k_coefficiency_raw = f0h_set_k_coefficiency_raw_to_str_py( k_coeff )
     rsp = send_ipmb_aardvark(ipmi , netfn , f0h_set_k_coefficiency_raw )
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR
     return rsp


## Function : 0xCBH, Set NM Power Draw Range
def set_nm_power_draw_range_py(ipmi, domain, min_power_draw_range, max_power_draw_range):
     # Coverter minimum power draw range  int value to hex value for byte[6:5]
     min_pwr_range_str = int_to_hex( min_power_draw_range, 2 )
     # Coverter maximum power draw range  int value to hex value for byte[8:7]
     max_pwr_range_str = int_to_hex( max_power_draw_range, 2 )
     # Send 0xCBh cmd
     netfn, cbh_raw =  cbh_raw_to_str_py(domain, min_pwr_range_str, max_pwr_range_str )
     rsp = send_ipmb_aardvark(ipmi , netfn , cbh_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR

     return SUCCESSFUL


## Function : 0x60H, Set PTU Launch Request
def set_ptu_launch_request_py(ipmi, request ):
     netfn, ptu_launch_60h_raw = ptu_launch_60h_raw_to_str_py( request )
     rsp = send_ipmb_aardvark(ipmi , netfn , ptu_launch_60h_raw )
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR
     return rsp

## Function : 0x61H, Set PTU Launch Request
def get_ptu_launch_result_py(ipmi, domain ):
     netfn, ptu_result_61h_raw = ptu_result_61h_raw_to_str_py( domain )
     rsp = send_ipmb_aardvark(ipmi , netfn , ptu_result_61h_raw )
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR
     # Calculate max power from rsp Byte[10:9] value, total 2 bytes
     max_power = calculate_byte_value_py(rsp, 9, 2)
     DEBUG('max_power = %6d' %max_power)
     min_power = calculate_byte_value_py(rsp, 11, 2)
     DEBUG('min_power = %6d' %min_power)
     eff_power = calculate_byte_value_py(rsp, 13, 2)
     DEBUG('eff_power = %6d' %eff_power)

     return max_power, min_power, eff_power


## Function : PECI cmd : GetTemp() configure
def peci_raw_get_temp():
     peci_raw_data = []
     peci_raw_data.append('0x'+ format(GET_TEMP,'02x'))
     DEBUG('peci_raw_data =')
     DEBUG(peci_raw_data)

     return peci_raw_data

## Function : 0xD9H, Send RAW PMbus Write Cmd
def send_raw_pmbus_write_cmd_extend_py(ipmi, msg_type , pec_report, pec_en, sensor_bus, target_addr, mux_addr, mux_ch, mux_config, trans_protocol, write_len, read_len, command):
     netfn, d9h_raw = d9h_set_raw_to_str_py(msg_type , pec_report, pec_en, sensor_bus, target_addr, mux_addr, mux_ch, mux_config, trans_protocol, write_len, read_len, command)
     # Send 0xDFh with command option
     rsp = send_ipmb_aardvark(ipmi , netfn , d9h_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR

     return rsp

## Function : 0xD9H, Send RAW PMbus Cmd
def send_raw_pmbus_cmd_extend_py(ipmi, msg_type , pec_report, pec_en, sensor_bus, target_addr, mux_addr, mux_ch, mux_config, trans_protocol, write_len, read_len, command):
     netfn, d9h_raw = d9h_raw_to_str_py(msg_type , pec_report, pec_en, sensor_bus, target_addr, mux_addr, mux_ch, mux_config, trans_protocol, write_len, read_len, command)
     # Send 0xDFh with command option
     rsp = send_ipmb_aardvark(ipmi , netfn , d9h_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR

     return rsp

## Function : PECI cmd : RdPkgConfig() configure
def peci_raw_rdpkgconfig(device_info, index, parameter1, parameter2 ):
     peci_raw_data = []
     # Setup Byte3 = Cmd_Code = 0xA1
     peci_raw_data.append('0x'+ format(RdPkgConfig,'02x'))
     # Setup Byte4 = Device Info
     peci_raw_data.append('0x'+ format(device_info,'02x'))
     # Setup Byte5 = Index
     peci_raw_data.append('0x'+ format(index,'02x'))
     # Setup Byte6 = parameter1 , low byte
     peci_raw_data.append('0x'+ format(parameter1,'02x'))
     # Setup Byte7 = parameter2, high byte
     peci_raw_data.append('0x'+ format(parameter2,'02x'))
     DEBUG('peci_raw_data =')
     DEBUG(peci_raw_data)

     return peci_raw_data

## Function :NM cmd = 0x40h - Send RAW PECI CMD  , PECI PROXY cmd by interface select
def send_raw_peci_py(ipmi, client_addr, interface, write_length, read_length, peci_cmd ):
     netfn, peci_40h_raw = peci_40h_raw_to_str_py( client_addr, interface, write_length, read_length, peci_cmd)
     # Send PECI PROXY to ME
     rsp = send_ipmb_aardvark(ipmi , netfn , peci_40h_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR

     return rsp

## Function : RECOVERY PSU SETTING IN CASE PSU Continuous ERROR ALEERT after testing
def SMART_PSU_RECOVERY(ipmi, default_ot_warm_low_byte, default_ot_warm_high_byte , bus , target_addr ):
     #Restor PSU OT_WARM_LIMIT value to default, suppose PROHOC event should gone!
     # Send PMbus Proxy cmd to write current Over Temperature Threshold value =  default_ot_warm value
     print('Start Recovery PSU Default Settings.....')
     write_len = 3
     read_len = 0
     pmbus_cmd_aray = [PMBUS_READ_WRITE_OT_WARM_LIMIT, default_ot_warm_low_byte , default_ot_warm_high_byte]
     rsp = send_raw_pmbus_write_cmd_extend_py(ipmi, d9h_trans_type_write_word, d9h_pec_report, d9h_pec_en, bus , target_addr , 0 , 0 , 0 , d9h_trans_potocol_pmbus , write_len , read_len , pmbus_cmd_aray)
     # Check pmbus rsp  data
     if(rsp == ERROR):
         print('ERROR!!! send pmbus error ! respond data error')
         return ERROR

     return SUCCESSFUL

## Function : 0x65H, Get CUPS Data , parameter_select = 01 means get CUPS index, = 02 means get load factctor.
def get_cups_data_65h_py( ipmi, parameter_selector):
	netfn, raw = get_cups_data_65h_raw_to_str_py( parameter_selector)
	rsp = send_ipmb_aardvark(ipmi , netfn , raw )
	sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
	if(sts != SUCCESSFUL ):
		return ERROR
	if(parameter_selector == 1):
		cups_index = calculate_byte_value_py(rsp, 5, 2)
		return cups_index
	elif(parameter_selector == 2):
		cpu_load_factor = calculate_byte_value_py(rsp, 5, 2)
		mem_load_factor = calculate_byte_value_py(rsp, 7, 2)
		io_load_factor = calculate_byte_value_py(rsp, 9, 2)		 
		return cpu_load_factor, mem_load_factor, io_load_factor
	else:
		return ERROR
		
		
## Function : 0xC8H, Get Platform Power Read 5 times and provide average reading feedback
def read_power_py( ipmi, mode, domain, power_domain, policy_id):
     netfn, c8h_raw = c8h_raw_to_str_py( mode, domain, power_domain, policy_id)
     rsp = send_ipmb_aardvark(ipmi , netfn , c8h_raw )
     current_power = calculate_byte_value_py(rsp, 5, 2)
     return current_power

## Function : IPMI Get Sensor Reading Cmd
def get_sensor_reading_py(ipmi, sensor_number):
     sn_number = int_to_hex( sensor_number, 1 )
     netfn, get_sensor_reading_raw = get_sensor_reading_raw_to_str_py(sn_number)
     # Send PECI PROXY to ME
     rsp = send_ipmb_aardvark(ipmi , netfn , get_sensor_reading_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), Sensor )
     if(sts != SUCCESSFUL ):
         return ERROR
     # Check if sensor available : byte3 bit[5] = 1 means sensor unabailable. = 0 means sensor abailable
     available_bit = get_bits_data_py( ord(rsp[2]) , 5, 1)
     DEBUG('get_sensor_reading : Available Bit = %d' %available_bit)
     # Check sensor scan settings : byte3 bit[6] = 0 means sensor scan disable. = 1 means sensor scan enable.
     scan_bit = get_bits_data_py( ord(rsp[2]), 6, 1)
     DEBUG('get_sensor_reading : Scan Bit = %d' %scan_bit)
     # Check event message settings : byte3 bit[7] = 0 means sensor event message disable. = 1 means sensor event message enable.
     event_message_bit = get_bits_data_py( ord(rsp[2]), 7 ,1)
     DEBUG('get_sensor_reading : Event Message Bit = %d' %event_message_bit)
     # Check if sensor abailable
     if(available_bit == 1):
         DEBUG('get_sensor_reading : Sensor number %2x not abailable' %sensor_number )
         return ERROR
     # Calculate sensor reading value Byte2 of respond message , total 1 byte
     sensor_reading = calculate_byte_value_py(rsp, 2, 1)

     return sensor_reading
	 

## Function : 0xC1H, Set NM Policy
def set_nm_power_policy_py(ipmi, domain, policy_enable, policy_id, policy_trigger_type, policy_add, aggressive, storage_mode, alert, shutdown, power_domain, limit_value, min_correction_time, trigger_limit, report_period ):
     # Coverter Limit int value to hex value for byte[9:8]- Policy Target Limit
     limit = int_to_hex( limit_value, 2 )
     # Coverter Correction time Setting from int to hex for byte[13:10]- Correction Time Limit
     correction = int_to_hex( min_correction_time, 4 )
     # Trigger limit Byte[15:14]
     trigger_point = int_to_hex( trigger_limit, 2 )
     if(policy_trigger_type == 0 or policy_trigger_type == 4 or policy_trigger_type == 6 ):
         #trigger_limit = c1h_trigger_limit_null
         trigger_limit = c1h_trigger_limit_null
         DEBUG('set_nm_power_policy note: This policy trigger type %2d is no need to input trigger limit point , so force use default settings = 0' %policy_trigger_type)
         tirgger_point = int_to_hex( trigger_limit, 2 )
     elif(policy_trigger_type == 2 or policy_trigger_type == 3):
         DEBUG('set_nm_power_policy: This trigger type %2d will use 0.1sec be single unit for policy trigger point, so policy trigger point =%2d secs ' %(policy_trigger_type, trigger_limit/10))
         trigger_point = int_to_hex( trigger_limit, 2 )
     elif(policy_trigger_type == 1):
         DEBUG('set_nm_power_policy: This trigger type %2d will use 1 Celsiu be single unit for policy trigger point, so policy trigger point =%2d secs ' %(policy_trigger_type, trigger_limit))
         trigger_point = int_to_hex( trigger_limit, 2 )
     else:
         DEBUG('set_nm_power_policy: ERROR !!! No support this policy trigger type %d' %policy_trigger_type)
         return ERROR
     # Byte[17:16] = Statistics Reporting Period in second = 1sec
     if(report_period > 65535):
         DEBUG('set_nm_power_policy: ERROR!!! report_period settings value %6d to hurge !!' %report_period)
         return ERROR
     statistic_period = int_to_hex( report_period, 2 )
     # Send 0xC1h cmd
     netfn, c1h_raw =  c1h_raw_to_str_py(domain, policy_enable, policy_id, policy_trigger_type, policy_add, aggressive, storage_mode, alert, shutdown, power_domain, limit, correction, trigger_point, statistic_period )
     rsp = send_ipmb_aardvark(ipmi , netfn , c1h_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR

     return SUCCESSFUL

## Function : 0xC9H, Get NM capability and platform power Draw Range
def get_platform_power_draw_range_py(ipmi, c9h_domain, c9h_policy_trigger_type, c9h_policy_type, c9h_power_domain):
     netfn, c9h_raw = c9h_raw_to_str_py( c9h_domain, c9h_policy_trigger_type, c9h_policy_type, c9h_power_domain)
     # Send 0xC9h to know Power Draw Rnage
     rsp = send_ipmb_aardvark(ipmi , netfn , c9h_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )	 

     if(sts != SUCCESSFUL ):
         return ERROR, ERROR, ERROR, ERROR
     # Calculate Max power draw range Byte[7:6] value, total 2 bytes
     max_draw_range = calculate_byte_value_py(rsp, 6, 2)
     DEBUG('max_draw_range = %6d' %max_draw_range)
     # Calculate Min power draw range Byte[9:8] value, total 2 bytes
     min_draw_range = calculate_byte_value_py(rsp, 8, 2)
     DEBUG('min_draw_range = %6d' %min_draw_range)
     if(max_draw_range > 0):
         DEBUG('Get Power Draw Range OK')
     else:
         DEBUG('!!! Get Power Draw Range Fail !!!')
         return ERROR, ERROR, ERROR, ERROR
     # Calculate Min correcction time Byte[13:10] value, total 4 bytes
     min_correction_time = calculate_byte_value_py(rsp, 10, 4)
     DEBUG('minimun correction time = %6d' %min_correction_time)
     # Calculate Max correcction time Byte[17:14] value, total 4 bytes
     max_correction_time = calculate_byte_value_py(rsp, 14, 4)
     DEBUG('maxmun correction time = %6d' %max_correction_time)
     if(min_correction_time > 0):
         DEBUG('Get correction time value OK')
     else:
         DEBUG('!!! Get correction time Fail !!!')
         return ERROR, ERROR, ERROR, ERROR


     return  max_draw_range, min_draw_range, min_correction_time, max_correction_time

## Function : 0x6AH, Set Performance Policy
def set_performance_policy_py(ipmi, control_scope, scope, min_ratio_bias, max_ratio, performance_preference  ):
     # Coverter min_ratio int value to hex value for byte[7]- minimal performance ratio or bias
     min_ratio_bias_hex = int_to_hex( min_ratio_bias, 1 )
     # Coverter min_ratio int value to hex value for byte[8]- maximal performance ratio
     max_ratio_hex = int_to_hex( max_ratio, 1 )
     # Coverter min_ratio int value to hex value for byte[9]- preference performance ratio
     performance_preference_hex = int_to_hex( performance_preference, 1 )
     # Send 0xC1h cmd
     netfn, hwpm_6ah_raw =  hwpm_6ah_raw_to_str_py(control_scope, scope, min_ratio_bias_hex, max_ratio_hex, performance_preference_hex )
     rsp = send_ipmb_aardvark(ipmi , netfn , hwpm_6ah_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR

     return SUCCESSFUL
