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
from termcolor import colored


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



## Function : 0xEAH, Get Host CPU Data (NM Configuration Data from BIOS HECI message)
def eah_get_host_cpu_data_py(ipmi, eah_domain ):
     netfn, eah_raw = eah_raw_to_str_py( eah_domain)
     # Send 0xEAh to ME
     rsp = send_ipmb_aardvark(ipmi , netfn , eah_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR, ERROR, ERROR, ERROR

     # Analyst get Host CPU Data format
     # NM already activated regular power limit bit = resp byte5 bits[3]
     nm_activate = get_bits_data_py( ord(rsp[4]) , 3 , 1)
     DEBUG('get_host_cpu_data : nm_activate = %d' %nm_activate)
     # Host CPU Discovery data bit = resp byte5 bits[4]
     host_discovery = get_bits_data_py( ord(rsp[4]) , 4 , 1)
     DEBUG('get_host_cpu_data : host_discovery = %d' %host_discovery)
     # EOP bit = resp byte5 bits[7]
     eop = get_bits_data_py( ord(rsp[4]) , 7 , 1)
     DEBUG('get_host_cpu_data : eop = %d' %eop)
     if(host_discovery == 1):
     	# Number of P-State Support Byte[6] value, total 1 bytes
     	p_states = calculate_byte_value_py(rsp, 6, 1)
	if(p_states == 0):
		print colored( 'ERROR, P-states are disabled by user','red')
	elif(p_states == 1):
                print colored( 'ERROR, CPU not support more P-states','red')
	else:
                print colored( 'PASS, p-states = %6d' %p_states,'green')

        # Number of T-State Support Byte[7] value, total 1 bytes
        t_states = calculate_byte_value_py(rsp, 7, 1)
        if(t_states == 0):
                print colored( 'ERROR, T-states are disabled by user','red')
        else:
                print colored( 'PASS, t-states = %6d' %t_states,'green')

        # Number of CPU sockets Byte[8] value, total 1 bytes
        cpu_numbers = calculate_byte_value_py(rsp, 8, 1)
	DEBUG('get_host_cpu_data : cpu_numbers = %d' %cpu_numbers)
        # HWP Capability Highest Byte[9] value, total 1 bytes
        hwp_highest = calculate_byte_value_py(rsp, 9, 1)
        DEBUG('get_host_cpu_data : hwp_highest = %d' %hwp_highest)
        # HWP Capability Gurranteed Performance Byte[10] value, total 1 bytes
        hwp_guar_performance = calculate_byte_value_py(rsp, 10, 1)
        DEBUG('get_host_cpu_data : hwp_guar_performance = %d' %hwp_guar_performance)
        # HWP Capability Most Efficiency Performance Byte[11] value, total 1 bytes
        hwp_eff_performance = calculate_byte_value_py(rsp, 11, 1)
        DEBUG('get_host_cpu_data : hwp_eff_performance = %d' %hwp_eff_performance)
        # HWP Capability Lowest Performance Byte[12] value, total 1 bytes
        hwp_low_performance = calculate_byte_value_py(rsp, 12, 1)
        DEBUG('get_host_cpu_data : hwp_low_performance = %d' %hwp_low_performance)

     else: ## no received Host CPU data from BIOS HECI message
	print colored( 'ERROR, ME not received Host CPU Data from BIOS HECI message ','red')
	p_states = 0
	t_states = 0
	cpu_numbers = 0
	hwp_highest = 0
	hwp_guar_performance = 0
	hwp_eff_performance = 0
	hwp_low_performance = 0

     sts = PASS

     return sts, nm_activate, host_discovery, eop, p_states, t_states, cpu_numbers, hwp_highest, hwp_guar_performance, hwp_eff_performance, hwp_low_performance




## Function : 0xD4H, Get Number of P/T states
def get_number_of_pt_states(ipmi, control_knob ):
     netfn, d4h_raw = d4h_raw_to_str_py( control_knob )
     rsp = send_ipmb_aardvark(ipmi , netfn , d4h_raw )
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR, ERROR
     if( control_knob == 0):
         p_states = ord(rsp[4])
         t_states = ord(rsp[5])
         return p_states, t_states
     elif(control_knob == 1):
         logical_processor_number =  ord(rsp[4])
         return logical_processor_number
     else:
         DEBUG('control_knob = %d settings error!! ' %control_knob)
         return ERROR, ERROR
     return ERROR, ERROR


## Function : 0xD3H, Get Maximum allowed  P/T states
def get_max_allowed_pt_states(ipmi, control_knob ):
     netfn, d3h_raw = d3h_raw_to_str_py( control_knob )
     rsp = send_ipmb_aardvark(ipmi , netfn , d3h_raw )
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR, ERROR
     if( control_knob == 0):
         max_allowed_p_states = ord(rsp[4])
         max_allowed_t_states = ord(rsp[5])
         return max_allowed_p_states, max_allowed_t_states
     elif(control_knob == 1):
         max_allowed_logical_processor_number =  ord(rsp[4])
         return max_allowed_logical_processor_number
     else:
         DEBUG('control_knob = %d settings error!! ' %control_knob)
         return ERROR, ERROR
     return ERROR, ERROR

## Function : 0xD2H, Set Maximum allowed  P/T states
def set_max_pt_states_py(ipmi, control_knob , max_p_states, max_t_states ):
     netfn, d2h_raw = d2h_raw_to_str_py( control_knob, max_p_states, max_t_states)
     rsp = send_ipmb_aardvark(ipmi , netfn , d2h_raw )
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR
     return rsp


## Function : 0xD0H, Set Total Power Budget
def set_total_power_budget_py(ipmi, domain , control , power_budget , component_id ):
     netfn, d0h_raw = d0h_raw_to_str_py( domain , control , power_budget , component_id )
     rsp = send_ipmb_aardvark(ipmi , netfn , d0h_raw )
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR

     return rsp

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


## Function : 0xF2H, Get Limiting Policy ID
def get_limiting_policy_id(ipmi, domain ):
     netfn, f2h_raw = f2h_raw_to_str_py( domain )
     rsp = send_ipmb_aardvark(ipmi , netfn , f2h_raw )
     sts = ipmi_resp_analyst_py( ord(rsp[0]), OEM )
     if(sts != SUCCESSFUL ):
         return ERROR
     limit_policy_id = ord(rsp[4])

     return limit_policy_id



## Function : Restore SPS FW to manufacture default
def facture_default_py(ipmi, command):
     # Send 0xDFh with command to ME
     sts = force_me_recovery_py(ipmi, command)
     if(sts != SUCCESSFUL ):
         return ERROR
     if(command == 1):
         # Add delay time 5 secs to make sure me go back to stable mode
         time.sleep(10)
         # Check if SPS FW boot into recovery mode.
         # Send Get DID cmd to ME
         sps_version, platform, dcmi, nm, image = get_device_id_py(ipmi)
         # Check resp byte16 - image flag to see if SPS FW run in recover mode
         if(image == get_did_recovery):
              DEBUG('!! SPS FW already running in recovery mode')
              return SUCCESSFUL
         elif(image == get_did_op1):
              DEBUG('SPS FW go back to operation mode and restore to default successfully')
              return ERROR
         elif(image == get_did_op2):
              DEBUG('SPS FW go back to operation mode but OP1 seems borken !!!')
              return ERROR
         elif(image == get_did_flash_err):
              DEBUG('SPI flash seems borken !!!')
              return ERROR
         else:
              DEBUG('COMMAND FAIL !!!')
              return ERROR
     elif(command == 2):
         # Add delay time 5 secs to make sure me go back to stable mode
         time.sleep(10)
         # Check if SPS FW back to operation mode.
         # Send Get DID cmd to ME
         sps_version, platform, dcmi, nm, image  = get_device_id_py(ipmi)
         DEBUG('facture_default : sps run in status = %d ' %image)
         # Check resp byte16 - image flag to see if SPS FW back to operation mode
         if(image == get_did_recovery):
              DEBUG('!! SPS FW still running in recovery mode after restore to default!!')
              return ERROR
         elif(image == get_did_op1):
              DEBUG('SPS FW go back to operation mode and restore to default successfully')
              return SUCCESSFUL
         elif(image == get_did_op2):
              DEBUG('SPS FW go back to operation mode but OP1 seems borken !!!')
              return ERROR
         elif(image == get_did_flash_err):
              DEBUG('SPI flash seems borken !!!')
              return ERROR
         else:
              DEBUG('COMMAND FAIL !!!')
              return ERROR
     elif(command == 3):
         # Check if PTT status is operational.
         return ERROR
     else:
         DEBUG('The byte4: command parameter is not in support list')
         return ERROR

     return ERROR


## Function : STANDARD IPMI GET SEL TIME CMD
def get_sel_time_py(ipmi):
     netfn, get_sel_time_raw = get_sel_time_raw_to_str_py()
     # Send Get SEL TIME to ME
     rsp = send_ipmb_aardvark(ipmi , netfn , get_sel_time_raw )
     # Check if rsp data correct
     sts = ipmi_resp_analyst_py( ord(rsp[0]), App )
     if(sts != SUCCESSFUL ):
         return ERROR
     # Calculate RTC TIME value Byte[5:2] value, total 4 bytes
     rtc_time = calculate_byte_value_py(rsp, 2, 4)
     DEBUG('rtc_time = %6d' %rtc_time)
     if(rtc_time > 4294967294):
          print('ERROR !!! ME CANNOT get Valid time from system RTC')
          print('!!! Check SYSTEM BIOS RTC TIME RANGE MUST between 1/Jan/2010 to 31/Dec/2079')
          return ERROR
     return rtc_time

## Function : PECI cmd : GetTemp() configure
def peci_raw_get_temp():
     peci_raw_data = []
     peci_raw_data.append('0x'+ format(GET_TEMP,'02x'))
     DEBUG('peci_raw_data =')
     DEBUG(peci_raw_data)

     return peci_raw_data

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
     DEBUG('PECI GetTemp() = Tmargin = %6d' %Tmargin)
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
     DEBUG('CPU0 Tjmax = %6d' %Tjmax)
     # Calculate current CPU Die Temperature = Tjmax - Tmargin
     CPU_Temperature = Tjmax - Tmargin
     DEBUG('Current CPU Die Temperature = %6d' %CPU_Temperature )

     return CPU_Temperature

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



