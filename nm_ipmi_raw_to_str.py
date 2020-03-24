from os_parameters_define import *
from utility_function import *
from config import *


## Function : MESDC CMD Converter 0x26h cmd to str format
def mesdc_26h_raw_to_str_py( ):
     netfun  = 0x30
     cmd     = '0x26'
     # Setup 26h_raw
     mesdc_26h_raw = [cmd,'0x57','0x01','0x00','0x04','0x06','0x04', '0x00', '0xca', '0x01', '0x01']

     return netfun, mesdc_26h_raw	


## Function : MESDC CMD Converter 0x26h cmd to str format
def mesdc_26h_mctp_statistic_raw_to_str_py( ):
     netfun  = 0x30
     cmd     = '0x26'
     # Setup 26h_raw
     mesdc_26h_mctp_statistic_raw = [cmd,'0x57','0x01','0x00','0x04','0x06','0x04', '0x40', '0xf8', '0x00', '0x00']

     return netfun, mesdc_26h_mctp_statistic_raw

## Function : MESDC CMD Converter 0x26h cmd to str format
def mesdc_26h_read_power_data_raw_to_str_py( addr ):
     netfun  = 0x30
     cmd     = '0x26'
     addr_low_byte = addr[0]
     addr_high_byte = addr[1]
     # Setup 26h_raw
     mesdc_26h_read_power_data_raw = [cmd,'0x57','0x01','0x00','0x04','0x06','0x04', '0x9F', '0xB0', addr_low_byte, addr_high_byte]

     return netfun, mesdc_26h_read_power_data_raw


## Function : MESDC CMD Converter 0x26h cmd to str format : SUSRAM file for NONCE status  is ASCII CODE : fwnoncest => 66 77 6e 6f 6e 63 65 73 74 00
def mesdc_26h_susram_hmrfpo_nonce_raw_to_str_py( ):
     netfun  = 0x30
     cmd     = '0x26'
     # Setup 26h_raw
     mesdc_26h_susram_hmrfpo_nonce_raw = [cmd,'0x57','0x01','0x00','0x04','0x06','0x0F', '0xD3', '0x76', '0x00', '0x00', '0x20', '0x66', '0x77', '0x6E', '0x6F', '0x6E', '0x63', '0x65', '0x73', '0x74', '0x00',]

     return netfun, mesdc_26h_susram_hmrfpo_nonce_raw



## Function : MESDC CMD Converter 0x26h cmd to str format
def mesdc_26h_nm_ptu_launch_state_raw_to_str_py( ):
     netfun  = 0x30
     cmd     = '0x26'
     # Setup 26h_raw
     mesdc_26h_nm_ptu_launch_state_raw = [cmd,'0x57','0x01','0x00','0x04','0x06','0x02', '0xf5', '0x1a']

     return netfun, mesdc_26h_nm_ptu_launch_state_raw



## Function : Converter DFh cmd to str format
##            command: 01h = Recovery but no default.  02h= Restore facture default.  03h = PTT initial state restore.
def dfh_raw_to_str( command ):
     netfun  = OEM
     cmd     = ' 0xdf '
     manufacture_id = INTEL_MANUFACTURE_ID
     # Setup byte4 :Command
     byte4 = int_to_hex_string(command)
     # Setup dfh_raw
     dfh_raw = netfun + cmd + manufacture_id + byte4

     return dfh_raw

## Function : Converter 60h cmd to str format
##            request: 00h = No Launch.  01h= Launch at next boot 
def ptu_launch_60h_raw_to_str_py( request ):
     netfun  = 0x2e
     cmd     = '0x60'
     # Setup byte4 :Command
     byte4 = int_to_hex_string(request)
     # Setup dfh_raw
     ptu_60h_raw = [cmd,'0x57','0x01','0x00',byte4]

     return netfun ,ptu_60h_raw

## Function : Converter 61h cmd to str format
##            domain: 00h = platform .  01h= CPU , 02h = Memory
def ptu_result_61h_raw_to_str_py( domain ):
     netfun  = 0x2e
     cmd     = '0x61'
     # Setup byte4 :Domain
     byte4 = int_to_hex_string(domain)
     # Setup dfh_raw
     ptu_61h_raw = [cmd,'0x57','0x01','0x00',byte4]

     return netfun ,ptu_61h_raw


## Function : Converter 65h cmd to str format
##            domain: 01h = CUPS Index .  02h= Dynamic load factors
def get_cups_data_65h_raw_to_str_py( parameter_selector ):
     netfun  = 0x2e
     cmd     = '0x65'
     # Setup byte4 :parameter_selector
     byte4 = int_to_hex_string(parameter_selector)
     # Setup 65h_raw
     cups_65h_raw = [cmd,'0x57','0x01','0x00',byte4]

     return netfun ,cups_65h_raw

## Function : Converter 81h cmd to str format
def btg_80h_raw_to_str_py( ):
     netfun  = 0x2e
     cmd     = '0x80'
     # Setup 80h_raw
     btg_81h_raw = [cmd,'0x57','0x01','0x00']

     return netfun ,btg_80h_raw

## Function : Converter 81h cmd to str format
def btg_81h_raw_to_str_py( ):
     netfun  = 0x2e
     cmd     = '0x81'
     # Setup 81h_raw
     btg_81h_raw = [cmd,'0x57','0x01','0x00']

     return netfun ,btg_81h_raw

## Function : Converter 82h cmd to str format
def btg_82h_raw_to_str_py( ):
     netfun  = 0x2e
     cmd     = '0x82'
     # Setup 82h_raw
     btg_82h_raw = [cmd,'0x57','0x01','0x00']

     return netfun ,btg_82h_raw

## Function : Converter 70h cmd to str format
def ptt_70h_raw_to_str_py( ):
     netfun  = 0x2e
     cmd     = '0x70'
     # Setup 70h_raw
     ptt_70h_raw = [cmd,'0x57','0x01','0x00']

     return netfun ,ptt_70h_raw

## Function : Converter 71h cmd to str format
def ptt_71h_raw_to_str_py( ):
     netfun  = 0x2e
     cmd     = '0x71'
     # Setup 71h_raw
     ptt_71h_raw = [cmd,'0x57','0x01','0x00']

     return netfun ,ptt_71h_raw


## Function : Converter DFh cmd to str format
##            command: 01h = Recovery but no default.  02h= Restore facture default.  03h = PTT initial state restore.
def dfh_raw_to_str_py( command ):
     netfun  = 0x2e
     cmd     = '0xdf'
     # Setup byte4 :Command
     byte4 = int_to_hex_string(command)
     # Setup dfh_raw
     dfh_raw = [cmd,'0x57','0x01','0x00',byte4]

     return netfun ,dfh_raw
     
## Function : Converter D4h cmd to str format
##            control_knob = 0 , get p/t states number.  = 1 get logical processors number
def d4h_raw_to_str_py( control_knob ):
     netfun  = 0x2e
     cmd     = '0xd4'
     # Setup byte4 [5:4] :control knob
     control = bit_shift_left(control_knob , 4)
     byte4   = int_to_hex_string(control)
     # Setup d4h_raw
     d4h_raw = [cmd,'0x57','0x01','0x00',byte4]

     return netfun ,d4h_raw

## Function : Converter D3h cmd to str format
##            control_knob = 0 , get maximum allowed  p/t states number.  = 1 get get maximum allowed logical processors number
def d3h_raw_to_str_py( control_knob ):
     netfun  = 0x2e
     cmd     = '0xd3'
     # Setup byte4 [5:4] :control knob
     control = bit_shift_left(control_knob , 4)
     byte4   = int_to_hex_string(control)
     # Setup d4h_raw
     d3h_raw = [cmd,'0x57','0x01','0x00',byte4]

     return netfun ,d3h_raw
     
## Function : Converter D2h cmd to str format
##            control_knob = 0 , set p/t states number.  = 1 set logical processors number
def d2h_raw_to_str_py( control_knob , max_p_states, max_t_states):
     netfun  = 0x2e
     cmd     = '0xd2'
     # Setup byte4 [5:4] :control knob
     control = bit_shift_left(control_knob , 4)
     byte4   = int_to_hex_string(control)
     # Setup byte5  : maximum allowed p states or logical cores # note when control_knob = 0, byte5 = max_p_states, when control_knob=1, bytes5 = #of logical cores low byte
     byte5   = int_to_hex_string(max_p_states)
     # Setup byte6  : maximum allowed t states or logical cores # note when control_knob = 0, byte6 = max_t_states, when control_knob=1, bytes6 = #of logical cores high byte = 0
     byte6   = int_to_hex_string(max_t_states)
     # Setup d2h_raw
     d2h_raw = [cmd,'0x57','0x01','0x00',byte4 , byte5 , byte6 ]

     return netfun ,d2h_raw


## Function : Converter D0h cmd to str format
def d0h_raw_to_str_py( domain , control , power_budget , component_id ):
     netfun  = 0x2e
     cmd     = '0xd0'
     # Setup byte4
     # byte4 bit[7]: Per component control
     component_control = bit_shift_left(control , 7)
     byte4 = int_to_hex_string(domain | component_control)
     # Setup bytes[6:5] = Power Budget
     byte5 = power_budget[0]
     byte6 = power_budget[1]
     # Setup bytes7 = component_identifier
     byte7 = int_to_hex_string(component_id)
     # Setup d0h_raw
     d0h_raw = [cmd,'0x57','0x01','0x00',byte4 ,byte5, byte6, byte7 ]
     
     return netfun, d0h_raw
     
## Function : Converter C0h cmd to str format
def c0h_raw_to_str_py( flags, domain, policy_id):
     netfun  = 0x2e
     cmd     = '0xc0'
     # Setup byte4 : Flags, bits[2:0]
     byte4 = int_to_hex_string(flags)
     # Conbine for byte5
     byte5 = int_to_hex_string(domain)
     # Setup byte6 : Policy ID
     byte6 = int_to_hex_string(policy_id)
     # Setup c0h_raw
     c0h_raw = [cmd,'0x57','0x01','0x00',byte4,byte5,byte6]

     return netfun, c0h_raw	 



## Function : Converter C8h cmd to str format
##            mode = 1 = power mode /2 Inlet temp /3 Global throttle status / .....
##            domain = 0 platform domain / 1 CPU domain / 2 Memory domain / 3 HW Protection/ 4 HPIO
def c8h_raw_to_str( mode, domain, power_domain, policy_id):
     netfun  = OEM
     cmd     = ' 0xc8 '
     manufacture_id = INTEL_MANUFACTURE_ID
     # Setup byte4 : Mode, bits[4:0]
     byte4 = int_to_hex_string(mode)
     # Setup byte5 : Domain ID, bits[3:0]
     domain = domain
     # byte5 bit[4]: power domain
     power_domain = bit_shift_left(power_domain , 4)
     # Conbine for byte5
     byte5 = int_to_hex_string(domain | power_domain)
     # Setup byte6 : Policy ID
     byte6 = int_to_hex_string(policy_id)
     # Setup c8h_raw
     c8h_raw = netfun + cmd + manufacture_id + byte4 + ' ' + byte5 + ' '+ byte6

     return c8h_raw
	 
## Function : Converter C8h cmd to str format
##            mode = 1 = power mode /2 Inlet temp /3 Global throttle status / .....
##            domain = 0 platform domain / 1 CPU domain / 2 Memory domain / 3 HW Protection/ 4 HPIO
def c8h_raw_to_str_py( mode, domain, power_domain, policy_id):
     netfun  = 0x2e
     cmd     = '0xc8'
     manufacture_id = INTEL_MANUFACTURE_ID
     # Setup byte4 : Mode, bits[4:0]
     byte4 = int_to_hex_string(mode)
     # Setup byte5 : Domain ID, bits[3:0]
     domain = domain
     # byte5 bit[4]: power domain
     power_domain = bit_shift_left(power_domain , 4)
     # Conbine for byte5
     byte5 = int_to_hex_string(domain | power_domain)
     # Setup byte6 : Policy ID
     byte6 = int_to_hex_string(policy_id)
     # Setup c8h_raw
     c8h_raw = [cmd,'0x57','0x01','0x00',byte4,byte5,byte6]

     return netfun, c8h_raw	 


## Function : Converter C9h cmd to str format
##            domain = 0 platform domain / 1 CPU domain / 2 Memory domain / 3 HW Protection/ 4 HPIO
##            Total request 5bytes
def c9h_raw_to_str( domain, policy_trigger_type, policy_type, power_domain):
     DEBUG('c9h_raw_str:')
     netfun  = OEM
     cmd     = ' 0xc9 '
     manufacture_id = INTEL_MANUFACTURE_ID
     # Setup byte4
     byte4 = int_to_hex_string(domain)
     # Setup byte5 , bits[3:0]
     policy_trigger_type =  policy_trigger_type
     # bits[6:4]
     policy_type = bit_shift_left(policy_type , 4)
     # bit[7]
     power_domain = bit_shift_left(power_domain , 7)
     # Conbine for byte5
     byte5 = int_to_hex_string(policy_trigger_type | policy_type | power_domain)
     # Setup c9h_raw
     c9h_raw = netfun + cmd + manufacture_id + byte4 + ' ' + byte5
     DEBUG(c9h_raw)

     return c9h_raw

## Function : Converter C9h cmd to str format
##            domain = 0 platform domain / 1 CPU domain / 2 Memory domain / 3 HW Protection/ 4 HPIO
##            Total request 5bytes
def c9h_raw_to_str_py( domain, policy_trigger_type, policy_type, power_domain):
     DEBUG('c9h_raw_str:')
     netfun  = 0x2e
     cmd     = ' 0xc9 '
     # Setup byte4
     byte4 = int_to_hex_string(domain)
     # Setup byte5 , bits[3:0]
     policy_trigger_type =  policy_trigger_type
     # bits[6:4]
     policy_type = bit_shift_left(policy_type , 4)
     # bit[7]
     power_domain = bit_shift_left(power_domain , 7)
     # Conbine for byte5
     byte5 = int_to_hex_string(policy_trigger_type | policy_type | power_domain)
     # Setup c9h_raw
     c9h_raw = [cmd,'0x57','0x01','0x00',byte4,byte5]

     return netfun, c9h_raw     


## Function : Converter EAh cmd to str format
##            domain = 0 platform domain
def eah_raw_to_str_py(  domain ):
     netfun  = 0x2e
     cmd     = ' 0xea '
     manufacture_id = INTEL_MANUFACTURE_ID
     # Setup byte4 : Domain ID, bits[3:0]
     domain = domain
     # Conbine for byte4
     byte4 = int_to_hex_string(domain)
     # Setup eah_raw
     eah_raw = [ cmd, '0x57','0x01','0x00', byte4 ]

     return netfun, eah_raw




## Function : Converter 6Ah cmd to str format
##            
##            Total request 10bytes
def hwpm_6ah_raw_to_str_py(control_scope, scope, min_ratio_bias, max_ratio, performance_preference):
     DEBUG('6ah_raw_str:')
     netfun  = 0x2e
     cmd     = ' 0x6a '
     # Setup byte4 , bits[3:0]
     control_scope =  control_scope
     # bits[7:6]
     scope = bit_shift_left(scope , 6)
     # Conbine for byte4
     byte4 = int_to_hex_string(control_scope | scope )
     #Setup byte5 = 0
     byte5 = str(0)
     #Setup byte6 = 0
     byte6 = str(0)
     #Setup byte7
     byte7 = ' '.join(min_ratio_bias)
     #Setup byte8
     byte8 = ' '.join(max_ratio)
     #Setup byte9
     byte9 = ' '.join(performance_preference)
     #Setup byte10
     byte10 = str(0)
     # Setup 6ah_raw
     hwpm_6ah_raw = [cmd,'0x57','0x01','0x00',byte4,byte5, byte6, byte7, byte8, byte9, byte10]

     return netfun, hwpm_6ah_raw




## Function : Convert 0xC1 cmd to str format
def c1h_raw_to_str(domain, policy_enable, policy_id, policy_trigger_type, policy_add, aggressive, storage_mode, alert, shutdown, power_domain, limit, correction, trigger_limit, report_period ):
     netfun  = OEM
     cmd     = ' 0xc1 '
     manufacture_id = INTEL_MANUFACTURE_ID
     # Setup byte4 : Domain ID, bits[3:0]
     domain = domain
     # byte4 bit[4]: Policy Enable
     policy_enable = bit_shift_left(policy_enable , 4)
     # Conbine for byte4
     byte4 = int_to_hex_string(domain | policy_enable)
     # Setup byte5 : Policy ID
     byte5 = int_to_hex_string(policy_id)
     # Setup byte6 : Policy Type
     # byte6 bit[3:0] :Policy trigger type 
     policy_trigger_type = policy_trigger_type
     # byte6 bit[4] :Policy config action
     policy_add = bit_shift_left(policy_add , 4)
     # byte6 bit[6:5] :aggressive mode
     aggressive = bit_shift_left(aggressive , 5)
     # byte6 bit[7] : storage_mode
     storage_mode = bit_shift_left(storage_mode , 7)
     # Conbine for byte6
     byte6 = int_to_hex_string(policy_trigger_type | policy_add | aggressive | storage_mode | storage_mode)
     # Setup byte7 : Exception action
     # byte7 bit[0]: Send alert
     alert = alert
     # byte7 bit[1]: Shutdown
     shutdown = bit_shift_left(shutdown , 1)
     # byte7 bit[7]: power domain
     power_domain = bit_shift_left(power_domain , 7)
     # Conbine for byte6
     byte7 = int_to_hex_string(power_domain | shutdown | alert)
     # Setup bytes[9:8] = Target Limit value
     byte8_to_byte9 = ' '.join(limit)
     # Setup bytes[13:10] = Correction time
     byte10_to_byte13 = ' '.join(correction)
     # Setup bytes[15:14] =  Trigger Limit Point value
     byte14_to_byte15 = ' '.join(trigger_limit)
     # Setup bytes[17:16] =  Statistic Report Period in second
     byte16_to_byte17 = ' '.join(report_period)

     c1h_raw = netfun + cmd + manufacture_id + byte4 + ' ' + byte5 + ' ' + byte6 + ' ' + byte7 + ' ' + byte8_to_byte9 + ' ' + byte10_to_byte13 + ' ' + byte14_to_byte15 + ' ' + byte16_to_byte17

     return c1h_raw
     
## Function : Convert 0xCB cmd to str format
def cbh_raw_to_str_py(domain, min_power_draw_range, max_power_draw_range ):
     netfun  = 0x2e
     cmd     = '0xcb'
     # Setup byte4 : Domain ID, bits[3:0]
     byte4 = int_to_hex_string(domain)
     # Setup bytes[6:5] = Minimum Power Draw Range
     byte5 = min_power_draw_range[0]
     byte6 = min_power_draw_range[1]
     # Setup bytes[8:7] =  Minimum Power Draw Range
     byte7 = max_power_draw_range[0]
     byte8 = max_power_draw_range[1]

     cbh_raw = [cmd,'0x57','0x01','0x00', byte4, byte5, byte6, byte7 , byte8 ]
     
     return netfun, cbh_raw


## Function : Convert 0xC1 cmd to str format
def c1h_raw_to_str_py(domain, policy_enable, policy_id, policy_trigger_type, policy_add, aggressive, storage_mode, alert, shutdown, power_domain, limit, correction, trigger_limit, report_period ):
     netfun  = 0x2e
     cmd     = ' 0xc1 '
     # Setup byte4 : Domain ID, bits[3:0]
     domain = domain
     # byte4 bit[4]: Policy Enable
     policy_enable = bit_shift_left(policy_enable , 4)
     # Conbine for byte4
     byte4 = int_to_hex_string(domain | policy_enable)
     # Setup byte5 : Policy ID
     byte5 = int_to_hex_string(policy_id)
     # Setup byte6 : Policy Type
     # byte6 bit[3:0] :Policy trigger type 
     policy_trigger_type = policy_trigger_type
     # byte6 bit[4] :Policy config action
     policy_add = bit_shift_left(policy_add , 4)
     # byte6 bit[6:5] :aggressive mode
     aggressive = bit_shift_left(aggressive , 5)
     # byte6 bit[7] : storage_mode
     storage_mode = bit_shift_left(storage_mode , 7)
     # Conbine for byte6
     byte6 = int_to_hex_string(policy_trigger_type | policy_add | aggressive | storage_mode | storage_mode)
     # Setup byte7 : Exception action
     # byte7 bit[0]: Send alert
     alert = alert
     # byte7 bit[1]: Shutdown
     shutdown = bit_shift_left(shutdown , 1)
     # byte7 bit[7]: power domain
     power_domain = bit_shift_left(power_domain , 7)
     # Conbine for byte6
     byte7 = int_to_hex_string(power_domain | shutdown | alert)
     # Setup bytes[9:8] = Target Limit value
     byte8 = limit[0]
     byte9 = limit[1]
     # Setup bytes[13:10] = Correction time
     byte10 = correction[0]
     byte11 = correction[1]
     byte12 = correction[2]
     byte13 = correction[3]
     # Setup bytes[15:14] =  Trigger Limit Point value
     byte14 = trigger_limit[0]
     byte15 = trigger_limit[1]
     # Setup bytes[17:16] =  Statistic Report Period in second
     byte16 = report_period[0]
     byte17 = report_period[1]

     #c1h_raw = netfun + cmd + manufacture_id + byte4 + ' ' + byte5 + ' ' + byte6 + ' ' + byte7 + ' ' + byte8_to_byte9 + ' ' + byte10_to_byte13 + ' ' + byte14_to_byte15 + ' ' + byte16_to_byte17
     c1h_raw = [cmd,'0x57','0x01','0x00', byte4, byte5, byte6, byte7 , byte8, byte9 , byte10 , byte11, byte12, byte13, byte14, byte15, byte16, byte17 ]
     
     return netfun, c1h_raw



## Function : Convert 0xF0 cmd to str format
def f0h_set_k_coefficiency_raw_to_str_py( k_coefficiency ):
     netfun  = 0x2e
     cmd     = '0xf0'
     # Setup byte4 : Domain ID, bits[3:0]
     byte4 = k_coefficiency[0]

     f0h_raw = [cmd,'0x57','0x01','0x00', byte4 ]

     return netfun, f0h_raw


## Function : Convert 0xF2 cmd to str format
def f2h_raw_to_str_py(domain):
     netfun  = 0x2e
     cmd     = '0xf2'
     # Setup byte4 : Domain ID, bits[3:0]
     byte4 = int_to_hex_string(domain)

     f2h_raw = [cmd,'0x57','0x01','0x00', byte4 ]
     
     return netfun, f2h_raw


## Function : Converter 40h cmd : Send RAW PECI cmd to str format
##            PECI client address = 30h CPU0 / 31h CPU1 domain / 32h CPU2 / 33h CPU3
##                                  70h~73h cmd via PECI over DMI
##                                  B0h~B3h cmd via PECI wire
def peci_40h_raw_to_str( client_addr, interface , write_length, read_length, raw ):
     DEBUG('40h_raw_str:')
     netfun  = OEM
     cmd     = ' 0x40 '
     manufacture_id = INTEL_MANUFACTURE_ID
     # byte4 bit[7:6]: Interface select
     interface = bit_shift_left(interface , 6)
     # byte4 bit[5:0]: Client address
     client_addr = client_addr
     # Setup byte4
     byte4 = int_to_hex_string(client_addr | interface)
     # Setup byte5 : Write length
     byte5 = int_to_hex_string(write_length)
     # Setup byte6 : Read length
     byte6 = int_to_hex_string(read_length)
     # Setup byte7-byteN : raw PECI data
     byte7_byteN = ' '.join(raw)
     # Setup 40h_raw
     peci_40h_raw = netfun + cmd + manufacture_id + byte4 + ' ' + byte5 + ' ' + byte6 + ' ' + byte7_byteN
     DEBUG(peci_40h_raw)

     return peci_40h_raw

## Function : Converter 40h cmd : Send RAW PECI cmd to str format
##            PECI client address = 30h CPU0 / 31h CPU1 domain / 32h CPU2 / 33h CPU3
##                                  70h~73h cmd via PECI over DMI
##                                  B0h~B3h cmd via PECI wire
def peci_40h_raw_to_str_py( client_addr, interface , write_length, read_length, raw ):
     DEBUG('40h_raw_str:')
     netfun  = 0x2e
     cmd     = '0x40'
     # byte4 bit[7:6]: Interface select
     interface = bit_shift_left(interface , 6)
     # byte4 bit[5:0]: Client address
     client_addr = client_addr
     # Setup byte4
     byte4 = int_to_hex_string(client_addr | interface)
     # Setup byte5 : Write length
     byte5 = int_to_hex_string(write_length)
     # Setup byte6 : Read length
     byte6 = int_to_hex_string(read_length)
     # Setup 40h_raw
     peci_40h_raw = [cmd,'0x57','0x01','0x00', byte4, byte5, byte6 ]
     # Setup byte7-byteN : raw PECI data
     for loop in range(0 , len(raw)):
          peci_40h_raw.append(format(raw[loop]))
 
     DEBUG(peci_40h_raw)

     return netfun, peci_40h_raw
     
## Function : Converter d9h cmd : Send RAW PMbus extended cmd to str format
def d9h_raw_to_str_py( msg_type , pec_report, pec_en, sensor_bus, target_addr, mux_addr, mux_ch, mux_config, trans_protocol, write_len, read_len, command ):
     DEBUG('d9h_raw_str:')
     netfun  = 0x2e
     cmd     = '0xd9'
     # byte4 bit[3:1]: 
     msg_trans_type  = bit_shift_left(msg_type , 1)
     # byte4 bit[5:4]: extended address formet = 1
     extended_addr_format = bit_shift_left(d9h_extended_device_addr , 4)
     pec_rep    = bit_shift_left(pec_report , 6)
     pec_enable = bit_shift_left(pec_en , 7)
     # Setup byte4
     byte4 = int_to_hex_string(msg_trans_type | extended_addr_format | pec_rep | pec_enable )
     # Setup byte5 : Sensor Bus
     byte5 = int_to_hex_string(sensor_bus)
     # Setup byte6 : Target Addr
     byte6 = int_to_hex_string(target_addr)
     # Setup byte7 : Mux Addr
     byte7 = int_to_hex_string(mux_addr)
     # Setup byte8 : Mux Channel
     byte8 = int_to_hex_string(mux_ch)
     # Setup byte9 : Mux Config
     byte9 = int_to_hex_string(mux_config)
     # Setup byte10 : Transmission Protocol parameter
     trans_ptol = bit_shift_left(trans_protocol , 5)
     byte10 = int_to_hex_string(trans_ptol)
     # Setup byte11 : Write Length
     byte11 = int_to_hex_string(write_len)     
     # Setup byte12 : Read length
     byte12 = int_to_hex_string(read_len)
     # Setup byte13 : Command
     byte13 = int_to_hex_string(command)
     # Setup d9h_raw
     pmbus_d9h_raw = [cmd,'0x57','0x01','0x00', byte4, byte5, byte6 , byte7, byte8, byte9, byte10, byte11, byte12, byte13 ]

     return netfun, pmbus_d9h_raw

## Function : Converter d9h cmd : Send RAW PMbus extended cmd to str format
def d9h_set_raw_to_str_py( msg_type , pec_report, pec_en, sensor_bus, target_addr, mux_addr, mux_ch, mux_config, trans_protocol, write_len, read_len, command ):
     DEBUG('d9h_raw_str:')
     netfun  = 0x2e
     cmd     = '0xd9'
     # byte4 bit[3:1]: 
     msg_trans_type  = bit_shift_left(msg_type , 1)
     # byte4 bit[5:4]: extended address formet = 1
     extended_addr_format = bit_shift_left(d9h_extended_device_addr , 4)
     pec_rep    = bit_shift_left(pec_report , 6)
     pec_enable = bit_shift_left(pec_en , 7)
     # Setup byte4
     byte4 = int_to_hex_string(msg_trans_type | extended_addr_format | pec_rep | pec_enable )
     # Setup byte5 : Sensor Bus
     byte5 = int_to_hex_string(sensor_bus)
     # Setup byte6 : Target Addr
     byte6 = int_to_hex_string(target_addr)
     # Setup byte7 : Mux Addr
     byte7 = int_to_hex_string(mux_addr)
     # Setup byte8 : Mux Channel
     byte8 = int_to_hex_string(mux_ch)
     # Setup byte9 : Mux Config
     byte9 = int_to_hex_string(mux_config)
     # Setup byte10 : Transmission Protocol parameter
     trans_ptol = bit_shift_left(trans_protocol , 5)
     byte10 = int_to_hex_string(trans_ptol)
     # Setup byte11 : Write Length
     byte11 = int_to_hex_string(write_len)     
     # Setup byte12 : Read length
     byte12 = int_to_hex_string(read_len)
     # Setup d9h_raw
     pmbus_d9h_raw = [cmd,'0x57','0x01','0x00', byte4, byte5, byte6 , byte7, byte8, byte9, byte10, byte11, byte12 ]
     for loop in range(0 , len(command)):
          pmbus_d9h_raw.append(format(command[loop]))
 
     DEBUG(pmbus_d9h_raw)
     
     return netfun, pmbus_d9h_raw

## Function : Converter d7h cmd : Send RAW PMbus extended cmd to str format
def d7h_set_raw_to_str_py( domain, psu1_addr, psu2_addr, psu3_addr, psu4_addr, psu5_addr, psu6_addr, psu7_addr, psu8_addr ):
     netfun  = 0x2e
     cmd     = '0xd7'
     # Setup byte4
     byte4 = int_to_hex_string(domain)
     # Setup byte5 : PSU1 Slave addr
     byte5 = int_to_hex_string(psu1_addr)
     # Setup byte6 : PSU2 Slave addr
     byte6 = int_to_hex_string(psu2_addr)
     # Setup byte7 : PSU3 Slave addr
     byte7 = int_to_hex_string(psu3_addr)
     # Setup byte8 : PSU4 Slave addr
     byte8 = int_to_hex_string(psu4_addr)
     # Setup byte9 : PSU5 Slave addr
     byte9 = int_to_hex_string(psu5_addr)
     # Setup byte10 : PSU6 Slave addr
     byte10 = int_to_hex_string(psu6_addr)
     # Setup byte11 : PSU7 Slave addr
     byte11 = int_to_hex_string(psu7_addr)     
     # Setup byte12 :PSU8 Slave addr
     byte12 = int_to_hex_string(psu8_addr)
     # Setup d7h_raw
     d7h_raw = [cmd,'0x57','0x01','0x00', byte4, byte5, byte6 , byte7, byte8, byte9, byte10, byte11, byte12 ]
     
     return netfun, d7h_raw



## Function : Converter Get DID : (NetFun = App(0x06), CMD = 01h) to str format
def get_did_raw_to_str( ):
     netfun  = App
     cmd     = ' 0x01 '
     # Setup get_did_raw
     get_did_raw = netfun + cmd

     return get_did_raw

## Function : Converter Get DID : (NetFun = App(0x06), CMD = 01h) to str format
def get_did_raw_to_str_py():
     netfun  = 0x06
     cmd     = '0x01'
     # Setup get_did_raw
     get_did_raw = [cmd]

     return netfun, get_did_raw	


## Function : Converter Cold Reset : (NetFun = App(0x06), CMD = 02h) to str format
def cold_reset_raw_to_str_py():
     netfun  = 0x06
     cmd     = '0x02'
     # Setup get_did_raw
     cold_reset_raw = [cmd]

     return netfun, cold_reset_raw

## Function : Converter Get SEL TIME : (NetFun = Storage (0x0A), CMD = 48h) to str format
def get_sel_time_raw_to_str( ):
     netfun  = Storage
     cmd     = ' 0x48 '
     # Setup get_sel_time_raw
     get_sel_time_raw = netfun + cmd

     return get_sel_time_raw

## Function : Converter Get SEL TIME : (NetFun = Storage (0x0A), CMD = 48h) to str format
def get_sel_time_raw_to_str_py( ):
     netfun  = 0x0a
     cmd     = '0x48'
     # Setup get_sel_time_raw
     get_sel_time_raw = [cmd]


     return netfun, get_sel_time_raw

## Function : Convert Get Sensor Reading : (NetFun = Sensor (0x04), CMD = 2Dh) to str format
def get_sensor_reading_raw_to_str( sensor_number ):
     netfun  = Sensor
     cmd     = ' 0x2d '
     # Setup byte1 : sensor_number
     byte1 = ' '.join(sensor_number)
     # Setup get_sensor_reading_raw
     get_sensor_reading_raw = netfun + cmd + ' ' + byte1

     return get_sensor_reading_raw

## Function : Convert Get Sensor Reading : (NetFun = Sensor (0x04), CMD = 2Dh) to str format
def get_sensor_reading_raw_to_str_py( sensor_number ):
     netfun  = 0x04
     cmd     = '0x2d'
     # Setup byte1 : sensor_number
     byte1 = ' '.join(sensor_number)
     # Setup get_sensor_reading_raw
     get_sensor_reading_raw = [cmd, byte1]
          
     return netfun, get_sensor_reading_raw



## Function : Converter 01h cmd to str format: Get chassis status
def get_chassis_power_status_raw_to_str_py( ):
     netfun  = 0x00
     cmd     = '0x01'
     # Setup get_chassis_status_raw
     get_chassis_status_raw = [cmd]

     return netfun ,get_chassis_status_raw

## Function : Converter 02h cmd to str format: Get chassis status
def chassis_control_raw_to_str_py( control ):
     netfun  = 0x00
     cmd     = '0x02'
     # Setup byte1 : sensor_number
     byte1 = int_to_hex_string(control) 
     # Setup chassis_control_raw
     chassis_control_raw = [cmd, byte1]

     return netfun ,chassis_control_raw

## Function : Converter 4Bh cmd : Get CPU and Memory Temperature cmd to str format
def get_cpu_mem_temp_4bh_raw_to_str_py( cup_select, cpu_set, mem_channel_set, request_format ):
     DEBUG('4bh_raw_str:')
     netfun  = 0x2e
     cmd     = '0x4B'
     # byte4 bit[3:0]:
     cpu_sel  = cup_select
     # byte4 bit[5:4]: cup_set
     cup_domain = bit_shift_left(cpu_set , 4)
     # byte4 bit[6]: mem_set
     mem_domain = bit_shift_left(mem_channel_set , 6)
     # byte4 bit[7]: request format
     format = bit_shift_left(request_format , 7)
     # Setup byte4
     byte4 = int_to_hex_string(cpu_sel | cup_domain | mem_domain | format )
     # Byte5~ Byte12 for standard mode
     if(request_format == get_temp_4bh_standard):
          # CPU0 Channels
          byte5 = get_temp_4bh_channel_all
          byte6 = get_temp_4bh_channel_all
          # CPU1 Channels
          byte7 = get_temp_4bh_channel_all
          byte8 = get_temp_4bh_channel_all
          # CPU2 Channels
          byte9 = get_temp_4bh_channel_all
          byte10 = get_temp_4bh_channel_all
          # CPU3 Channels
          byte11 = get_temp_4bh_channel_all
          byte12 = get_temp_4bh_channel_all
          # Setup 4bh_raw
          get_cpu_mem_temp_4bh_raw = [cmd,'0x57','0x01','0x00', byte4, byte5, byte6 , byte7, byte8, byte9, byte10, byte11, byte12 ]

          DEBUG(get_cpu_mem_temp_4bh_raw)

          return netfun, get_cpu_mem_temp_4bh_raw
     # Byte5 ~ Byte20 for extended mode
     elif(request_format == get_temp_4bh_extended):
          # CPU0 Channels
          byte5 = get_temp_4bh_channel_all
          byte6 = get_temp_4bh_channel_all
          byte7 = get_temp_4bh_channel_all
          byte8 = get_temp_4bh_channel_all
          # CPU2 Channels
          byte9 = get_temp_4bh_channel_all
          byte10 = get_temp_4bh_channel_all
          byte11 = get_temp_4bh_channel_all
          byte12 = get_temp_4bh_channel_all
          # CPU3 Channels
          #byte13 = get_temp_4bh_channel_all
          #byte14 = get_temp_4bh_channel_all
          #byte15 = get_temp_4bh_channel_all
          #byte16 = get_temp_4bh_channel_all
          # CPU4 Channels
          #byte17 = get_temp_4bh_channel_all
          #byte18 = get_temp_4bh_channel_all
          #byte19 = get_temp_4bh_channel_all
          #byte20 = get_temp_4bh_channel_all
          # CPU3 Channels
          byte13 = get_temp_4bh_channel_none
          byte14 = get_temp_4bh_channel_none
          byte15 = get_temp_4bh_channel_none
          byte16 = get_temp_4bh_channel_none
          # CPU4 Channels
          byte17 = get_temp_4bh_channel_none
          byte18 = get_temp_4bh_channel_none
          byte19 = get_temp_4bh_channel_none
          byte20 = get_temp_4bh_channel_none


          # Setup 4bh_raw
          get_cpu_mem_temp_4bh_raw = [cmd,'0x57','0x01','0x00', byte4, byte5, byte6 , byte7, byte8, byte9, byte10, byte11, byte12, byte13, byte14, byte15, byte16, byte17, byte18, byte19, byte20]

          DEBUG(get_cpu_mem_temp_4bh_raw)

          return netfun, get_cpu_mem_temp_4bh_raw

