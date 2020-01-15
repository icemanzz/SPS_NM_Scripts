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

## Manually Define Efficiency Capping ratio , Default 0% , the higher value means weak target capping value. Value can be -5 , -8 , -10(-5% , -8%, -10% ) or 5 (5%)...
efficiency_ratio =  0
## Manually Set Power Draw Range , enable this settings will ignore automatically power draw range detection. Add this setting in case system no NM PTU support.
manually_platform_draw_range_enable = True
platform_max_power = 258  #Ubuntu 220 #Win2016 Cstate off = 265 # Legacy
platform_min_power = 125  #Ubuntu 110 #Win2016 Cstate off = 110 # Legacy
## Manually select power control mechanism NM/HWPM
control_mechanism = 'NM'
## Manually Pkg C6 state fine tune, c6_fine_tune = 1 to enable C state power fine turn function. c6_fine_tune = 0 disable c state power fine turn function.
c6_fine_tune = 0
## Power Reading Scan Rate per sec
pwr_scan_rate = 1
## Define the power log save path and name
pwr_log_file = 'performance_power_result_ratio_'+str(efficiency_ratio)+'_'+str(time.time())+'.csv'
#pwr_log_file = 'performance_power_result_ratio_'+str(time.time())+'.csv'
## Define the CPU workload data offset (%). In case CUPS CPU workload sensor not accuracy , this is a workaround to increase CUPS sensor accuracy to mach OS CPU workload.
cups_core_loading_offset = 7
## Define max/min EPP value
max_epp_range = 255
min_epp_range = 0


## system NM settings check to make sure all necessary functions are ready to test efficiency capping.
def nm_enviornment_check(ipmi):
	# Read Platform Power via 0xC8h cmd
	power_average_stress = read_power_py(ipmi , global_power_mode, platform_domain,AC_power_side, 0 )
	if(power_average_stress == ERROR):
		sts = ERROR
		print('Platform power reading error!!!')
		return sts
	else:
		sts = PASS
		print(power_average_stress)
		
	# Detect CUPS sensor#
	cups_core_workload = get_sensor_reading_py(ipmi, cups_core)
	if(cups_core_workload == ERROR):
		sts = ERROR
		print('CUPS core Workload Sensor number: %2s not exist' %cups_core_workload)
		return sts
	else:
		sts = PASS
		print('CPU CORE CUPS Workload Reading = %2d' %cups_core_workload)
		
	# CUPS Index
	cups_index = get_cups_data_65h_py(ipmi, cups_65h_cups_index)
	if(cups_index == ERROR):
		sts = ERROR
		print('CUPS index: %2s not exist' %cups_index)
		return sts
	else:
		sts = PASS
		print('cups index = %2d' %cups_index)

	# CUPS Loading factors
	cpu_load_factor, mem_load_factor, io_load_factor = get_cups_data_65h_py(ipmi, cups_65h_dynamic_load_factors)
	if(cups_index == ERROR):
		sts = ERROR
		print('CUPS index: %2s not exist' %cpu_load_factor)
		return sts
	else:
		sts = PASS
		print('cpu loading factor = %2d' %cpu_load_factor)
		print('mem loading factor = %2d' %mem_load_factor)
		print('io loading factor = %2d' %io_load_factor)
	
	return sts



## Define initialization of aardvark ipmi        
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

## Formula to calculate current efficiency power capping value
def get_efficiency_capping_vaule( max_draw_range, min_draw_range, cpu_utility, capping_offset):
	capping_offset_percentage = efficiency_ratio    # how many percentage % change can be manually define.
	capping_capability = max_draw_range - min_draw_range
	capping_offset = (capping_capability/100)*capping_offset_percentage
	cap_value = (capping_capability*cpu_utility/100) + min_draw_range + capping_offset
        # Check if cap value out of power draw range. if yes, replace to min/max power range.
	if(cap_value < min_draw_range):
		cap_value = min_draw_range
	elif(cap_value > max_draw_range):
		cap_value = max_draw_range

	print('Efficiency Power Capping = %2d' %(cap_value))

	return cap_value


## Formula to calculate current efficiency epp policy value
def get_efficiency_epp_vaule(cpu_utility, capping_offset):
        capping_offset_percentage = efficiency_ratio    # how many percentage % change can be manually define.
        capping_capability = max_epp_range - min_epp_range
        capping_offset = (capping_capability/100)*capping_offset_percentage
        epp_value = (capping_capability*cpu_utility/100) + min_epp_range + capping_offset
        # Check if cap value out of epp range. if yes, replace to epp range.
        if(epp_value < min_epp_range):
                epp_value = min_epp_range
        elif(epp_value > max_epp_range):
                epp_value = max_epp_range

        print('Efficiency EPP Capping = %2d' %(epp_value))

        return epp_value




def log_power_data(count_start_time, presult):
        # Check if time meet scan rate
	current_time = time.time()
	go = current_time - count_start_time
	if( go >=  pwr_scan_rate ):
		print(go)
		count_start_time = current_time # update for next read power time.
        	# Read Platform power via 0xC8h cmd
		power = read_power_py(ipmi , global_power_mode, platform_domain,AC_power_side, 0 )
		if(power == ERROR):
			sts = ERROR
			print('Platform power reading error!!!')
			return sts
		else:
			sts = PASS
			print(power)

        	# Save time and power data to csv file
		RESULT_file = open(presult, 'a') # open and append power data to result file
		RESULT_file.write(str(current_time)+','+str(power)+ '\n')
		RESULT_file.close() # Close and write result file for each test loading level.
	else:
		print('not ready')
		sts = PASS

	return sts, count_start_time



## Below is __Main__
# Pre-edit power log
presult = pwr_log_file  # Save this test result file name for loop test.
pwr_result_file = open(presult , 'w')   # Open this result file.
pwr_result_file.write('time,power'+'\n') # Write columns data to this result file.
pwr_result_file.close()

# Initial aardvark
ipmi = aardvark_ipmi_init(target_me_addr, target_me_bridge_channel)

sts = nm_enviornment_check(ipmi)
#Check Initialize status
if(sts == PASS):
	if(manually_platform_draw_range_enable == True):
		# Read Power Draw Range and Correction time via 0xC9h cmd
                max_draw_range, min_draw_range, min_correction_time, max_correction_time = get_platform_power_draw_range_py( ipmi, platform_domain, 0, 1, 0)
		max_draw_range = platform_max_power   # Replace max_draw_range , because now is manually settings mode.
		min_draw_range = platform_min_power   # Replace min_draw_range , because now is manually settings mode.
                if(min_correction_time == ERROR ):
                        print('Get Correction Time Settings cmd Error: data not exist')
                        run = False
                else:
                        print('Manually Set Platform max_draw_range = %2d' %max_draw_range)
                        print('Manually Set Platform min_draw_range = %2d' %min_draw_range)
                        run = True
	else: # Use NM Power Draw Range settings to detect system max and min power range, system must support NM PTU to make sure range is correct.
		# Read Power Draw Range and Correction time via 0xC9h cmd
		max_draw_range, min_draw_range, min_correction_time, max_correction_time = get_platform_power_draw_range_py( ipmi, platform_domain, 0, 1, 0)
		if(max_draw_range == ERROR ):
        		print('Get Platform Power Draw Range Error: data not exist')
        		run = False
		else:
        		print('Platform max_draw_range = %2d' %max_draw_range)
        		print('Platform min_draw_range = %2d' %min_draw_range)
			run = True
else:
    run = False

# Start Efficiency Capping Process
count_start_time = time.time()
while run:

	# Save Current Platform Power Reading
	sts, count_start_time = log_power_data(count_start_time, presult)
	# Detect CUPS sensor#
	cups_core_workload = get_sensor_reading_py(ipmi, cups_core)
	if(cups_core_workload == ERROR):
		print(' CUPS core Workload Sensor number: %2s not exist' %cups_core_workload)

	else:
		# Detect current CPU workload via CUPS sensor
		cpu_utility = cups_core_workload*100/255 + cups_core_loading_offset # add offset for cups
		print('CPU CORE CUPS Workload Reading = %2d' %cpu_utility)
		# Calculate efficiency capping vlaue
		if(control_mechanism == 'NM'):
			# Dynamic capping offset settings
			if(cpu_utility > 30):
				capping_offset = 10
			#elif(35 >= cpu_utility >= 8 ):
			#	capping_offset = 5
			else:
				capping_offset = 0
			# Determet cap value
			cap_value = get_efficiency_capping_vaule( max_draw_range, min_draw_range, cpu_utility, capping_offset )

			if(cpu_utility > 35 and c6_fine_tune == 1): # For Win2016 C state fine turn
				# Remove Power Policy via 0xC1h cmd
				print('Disable NM policy and change to performance policy!')
				sts = set_nm_power_policy_py(ipmi, c1h_platform_domain, c1h_policy_disable, 3, c1h_no_policy_trigger, c1h_remove_policy, c1h_auto_aggressive, c1h_presistent, c1h_alert_enable, c1h_shutdown_disable, AC_power_side, cap_value, min_correction_time, c1h_trigger_limit_null, c1h_minimum_report_period )
				# Change to HWPM control in heavy load
				epp_value = get_efficiency_epp_vaule( cpu_utility )
                        	# Set Performance Policy via 0x6Ah cmd.
                        	sts = set_performance_policy_py(ipmi, hwpm_6ah_performance_preference , hwpm_6ah_scope_entire_platform , 0 , epp_value , epp_value  )
			else:
				# Set Power Capping via 0xC1h cmd in police id #3,  correction time = minimum support correction time
				sts = set_nm_power_policy_py(ipmi, c1h_platform_domain, c1h_policy_enable, 3, c1h_no_policy_trigger, c1h_add_policy, c1h_auto_aggressive, c1h_presistent, c1h_alert_enable, c1h_shutdown_disable, AC_power_side, cap_value, min_correction_time, c1h_trigger_limit_null, c1h_minimum_report_period )

		elif(control_mechanism == 'HWPM'): # Currently HWPM mode only in Purley platform support
			epp_value = get_efficiency_epp_vaule( cpu_utility , capping_offset)
			# Set Performance Policy via 0x6Ah cmd.
			sts = set_performance_policy_py(ipmi, hwpm_6ah_performance_preference , hwpm_6ah_scope_entire_platform , 0 , epp_value , epp_value  )

	if(sts == ERROR):
		print('Set efficiency control fail !!!')
