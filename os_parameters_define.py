## Parameters Define :
# Path of Test Item List
NM_TEST_LIST_LINUX = 'nm_test_list'
NM_TEST_FILE_LINUX = 'nm_test_list'
NM_TEST_LIST_WIN = 'nm_test_list'
NM_TEST_FILE_WIN = 'nm_test_list'
# Path of PTUGEN and PTUMON utility
PTU_MON_LOG  = 'ptumon_log'
## Below define empty path 
SSH_CMD_PATH_EMPTY  = ' '
##  SSH IGNORE HOST KEY CHECK 
SSH_IGNORE_HOST_KEY =' -o "StrictHostKeyChecking no" '
##Below define remote test system PTU path for Purley
PURLEY_PTUGEN_PATH  = '/root/PTU/PURLEY/ptugen'
PURLEY_PTUMON_PATH  = '/root/PTU/PURLEY/ptumon'
PURLEY_SSH_PTU_INIT_SCRIPT  = '/root/PTU/PURLEY/ptu_purley_init.sh'
##Below define remote test system  PTU path for Mehlow
MEHLOW_PTUGEN_PATH  = '/root/PTU/Mehlow/cflptugen'
MEHLOW_PTUMON_PATH  = '/root/PTU/Mehlow/cflptumon'
MEHLOW_SSH_PTU_INIT_SCRIPT  = '/root/PTU/Mehlow/ptu_mehlow_init.sh'
# Define spsinfo path in iso OS
SPS_INFO_PATH = '/root/build_centos_ios/SPS_Tools_4.2.86.64_int/SpsInfo/Linux64/spsInfoLinux64'
# Define HeciCmdsTool
HECI_TOOL_PATH = '/root/build_centos_ios/SPS_Tools_4.2.86.64_int/HeciCmdsTool/Linux64/HeciCmdsToolLinux64'
# Define HECI MEADDR
HECI_MEADDR = '0x20'
# Define HECI CMD
HECI_GET_ME_BIOS_INTERFACE_CMD = '01'
# Define offset of data from keywork in spsinfo tool
HECI_RESPOND_KEYWORD_OFFSET = 1
# Define spsinfo keyword registers 
SPS_INFO_FWSTS1 = 'FW Status Register 1:'
SPS_INFO_FWSTS2 = 'FW Status Register 2:'
SPS_INFO_FWSTS4 = 'FW Status Register 4:'
SPS_INFO_FWSTS6 = 'FW Status Register 6:'
# Define offset of data from keywork in spsinfo tool
SPS_INFO_KEYWORD_OFFSET = 1
##Window ssh tool path
WIN_SSH_PATH = 'C:\\cygwin64\\bin\\ssh.exe '
WIN_SSH_COPY_ID_PATH = 'C:\\cygwin64\\bin\\ssh-copy-id '
WIN_SCP_PATH = 'C:\\cygwin64\\bin\\scp.exe '
##Window ssh known_hosts path C:\cygwin64\home\hchen109\.ssh
WIN_SSH_KNOWN_HOST_PATH = 'C:\\cygwin64\\home\\hchen109\\.ssh\\known_hosts '
## LINUX ssh known hosts path
LINUX_SSH_KNOWN_HOST_PATH = '/home/howard/.ssh/known_hosts'
LINUX_SSH_ROOT_KNOWN_HOST_PATH = '/root/.ssh/known_hosts'
## Define Background run cmd
WIN_BACKGROUND_RUN = 'start '
LINUX_BACKGROUND_RUN = 'nohup '
## Define SSH LOG SAVE SWITCH
LOG_SAVE_OFF = 0
LOG_SAVE_EN  = 1
## Define SSH LOG FILE PATH
SSH_LOG_PATH_LINUX = 'nm_ssh_log'
SSH_LOG_PATH_WIN = 'nm_ssh_log'
# Path of OS RTC LOG
OS_RTC_LOG   = 'os_rtc'
OS_RTC_LOG_WIN   = 'os_rtc'
## Define result file
TEST_RESULT_WIN = 'nm_test_result'
TEST_RESULT_LINUX = 'nm_test_result'
#define previous OS IP data log path
OS_IP_LOG = 'nm_os_ip'
OS_IP_TEST_LIST = 'nm_os_ip_check_list'
# OS RTC TIME CMD
OSRTC  = 'timedatectl'
# Defualt RTC TIME
RTC_DEFAULT_YEAR = 1970
# Test Item Define
NM_TEST_ITEM = [  'NM_000',   'NM_001',     'NM_002','NM_003',   'NM_004',   'NM_005',   'NM_006',   'NM_007',   'NM_008',   'NM_009',   'NM_010',   'NM_011',   'NM_012',   'NM_013',   'NM_014', \
                'PECI_000', 'PECI_001', 'PECI_002','PECI_003', 'PECI_004', 'PECI_005', 'PECI_006', 'PECI_007', 'PECI_008', 'PECI_009', 'PECI_010', 'PECI_011', 'PECI_012', 'PECI_013', 'PECI_014', \
                'SMART_001', \
                'PM_002', 'PM_003', 'PM_004', 'PM_005', 'PM_006', \
                'DC_CYCLE', 'RESET_CYCLE', \
                'MCTP_001', 'MCTP_002', 'MCTP_003', 'MCTP_004', 'MCTP_005', 'MCTP_006', 'MCTP_007', 'MCTP_008', \
                'PTU_001', 'PTU_002', 'PTU_003', 'PTU_004', \
                'NM_WS_001', 'NM_WS_002', 'NM_WS_003', 'NM_WS_004', 'NM_WS_005', 'NM_WS_006', 'NM_WS_007', 'NM_WS_008', 'NM_WS_009', 'NM_WS_010', \
                'PTT_003', 'PTT_004', \
                'BTG_003',  \
                'BIOS_001', 'BIOS_002', 'BIOS_003', 'BIOS_004', \
                'ME_001', 'ME_002', 'ME_003', 'ME_004', 'ME_005', 'ME_006', 'ME_007', 'ME_008', 'ME_009', 'ME_010', 'ME_011', 'ME_012', 'ME_013', 'ME_014', 'ME_015', 'ME_016']
# Test Item ID
NM_000       = 0
NM_001       = 1
NM_002       = 2
NM_003       = 3
NM_004       = 4
NM_005       = 5
NM_006       = 6
NM_007       = 7
NM_008       = 8
NM_009       = 9
NM_010       = 10
NM_011       = 11
NM_012       = 12
NM_013       = 13
NM_014       = 14
PECI_000     = 15
PECI_001     = 16
PECI_002     = 17
PECI_003     = 18
PECI_004     = 19
PECI_005     = 20
PECI_006     = 21
PECI_007     = 22
PECI_008     = 23
PECI_009     = 24
PECI_010     = 25
PECI_011     = 26
PECI_012     = 27
PECI_013     = 28
PECI_014     = 29
# ENABLE / DISABLE
ENABLE       = 1
DISABLE      = 0
# Test STATUS : SUCCESSFUL/ERROR/NONE
PASS        = '0'
FAIL        = 'ERROR'
NONE        = 'NONE'

# RESP define
SUCCESSFUL   = '0'
ERROR        = 'ERROR'
SEARCH       = 'SEARCH'
# Debug OS Type define = 'win' or 'linux'
os_linux = 'linux'
os_win   = 'win'
# CMD RUNNING TYPE
background_run_disable = 0
background_run_enable  = 1
# OS User Name
os_user      = 'root'
# define max target ip range
start_ip_range = 20
end_ip_range = 35
head_ip_add  = '192.168.0.'
# define ping parameter for win and linux
WIN_PING_PARAMETER = ' -n 1 -w 10 '
LINUX_PING_PARAMETER = ' -c 1 -W 10 '
# BMC network settings
bmc_ip_addr  = '192.168.0.87'
user         = 'root'
password     = 'admin3'
bmc_interface = 'lanplus'
# ME bridge cmd settings
me_slave_addr = '0x2c'
me_bridge_channel = '6'
# Aardvark target address and channel settings
target_me_addr = 0x2c
target_bmc_addr = 0x20
target_me_bridge_channel = 0x06
target_bmc_bridge_channel = 0x00
# IPMI cmd header settings
lun = 0
ipmi_network_bridge_raw_cmd_header  =  'ipmitool'+ ' -H ' + bmc_ip_addr + ' -U '+ user + ' -P '+ password + ' -I ' + bmc_interface + ' -t '+ me_slave_addr+' -b '+ me_bridge_channel + ' raw '
ipmi_network_cmd_header = 'ipmitool'+ ' -H ' + bmc_ip_addr + ' -U '+ user + ' -P '+ password + ' -I ' + bmc_interface
ipmi_network_raw_cmd_header = 'ipmitool'+ ' -H ' + bmc_ip_addr + ' -U '+ user + ' -P '+ password + ' -I ' + bmc_interface + ' raw '
# Linux OS Shutdown cmd
centos_dc_off = ' init 0 '
centos_reset = ' init 6 '
# IPMI NETWORK FUNCTION define
Chassis              = ' 0x00 '
Bridge               = ' 0x01 '
Sensor               = ' 0x04 '
App                  = ' 0x06 '
Storage              = ' 0x0a '
Transpoet            = ' 0x0C '
OEM                  = ' 0x2e '
Controller_OEM       = ' 0x30 '
# Mise parameters
INTEL_MANUFACTURE_ID = ' 0x57 0x01 0x00 '
## SPS FW Sensor number list
pch_temp             = 0x08
psu0_ac_pwr          = 0x4e
psu1_ac_pwr          = 0x4f
psu2_ac_pwr          = 0x50
psu3_ac_pwr          = 0x51
psu4_ac_pwr          = 0x52
psu5_ac_pwr          = 0x53
psu6_ac_pwr          = 0x54
psu7_ac_pwr          = 0x55
psu0_dc_pwr          = 0xa4
psu1_dc_pwr          = 0xa5
psu2_dc_pwr          = 0xa6
psu3_dc_pwr          = 0xa7
psu4_dc_pwr          = 0xa8
psu5_dc_pwr          = 0xa9
psu6_dc_pwr          = 0xaa
psu7_dc_pwr          = 0xab
psu0_sts             = 0x66
psu1_sts             = 0x67
psu2_sts             = 0x68
psu3_sts             = 0x69
psu4_sts             = 0x6a
psu5_sts             = 0x6b
psu6_sts             = 0x6c
psu7_sts             = 0x6d
hsc0_input_pwr       = 0x29
hsc1_input_pwr       = 0x2d
hsc2_input_pwr       = 0xe0
hsc3_input_pwr       = 0xe6
smar_clst            = 0xb2
cups_core            = 0xbe
cups_mem             = 0xc0
cups_io              = 0xbf
ptas_outlet_temp     = 0xbd
ptas_air_flow        = 0xa2
ptas_inlet_temp      = 0xa3
hpio_domain_pwr      = 0xae
hpio0_pwr            = 0xb3
hpio1_pwr            = 0xb4
hpio2_pwr            = 0xb5
hpio3_pwr            = 0xb6
hpio4_pwr            = 0xb7
hpio5_pwr            = 0xb8
hpio6_pwr            = 0xb9
hpio7_pwr            = 0xba
## IPMI STANDARD CMD LIST:
# NetFun = Chassis = 0x00 , CMD = 0x02
chassis_control_off   = 0
chassis_control_on    = 1
chassis_control_cycle = 2
chassis_control_reset = 3
# NetFun = APP = 0x06 , CMD = 0x01
get_did_target_bmc   = 0
get_did_target_me    = 1
# NetFun = APP = 0x06 , CMD = 0x01 Respond data analyst
get_did_Intel_me     = 0x50
get_did_bmc          = 0x20
# NetFun =App = 0x06, CMD = 0x01 Byte 13 bit[3:0], NM / SiEn version info
get_did_NM_disable   = 0
get_did_NM_1         = 1
get_did_NM_2         = 2
get_did_NM_3         = 3
get_did_NM_4         = 4
get_did_NM_5         = 5
# NetFun =App = 0x06, CMD = 0x01 Byte 13 bit[7:4], DCMI info
get_did_DCMI_disable = 0
get_did_DCMI_1       = 1
get_did_DCMI_1_1     = 2
get_did_DCMI_1_5     = 3
# NetFun =App = 0x06, CMD = 0x01 Byte 16 bit[1:0], image flag
get_did_recovery     = 0
get_did_op1          = 1
get_did_op2          = 2
get_did_flash_err    = 3
# NetFun = Sensor = 0x04 , CMD = 0x2d
get_sensor_reading_target_bmc = 0
get_sensor_reading_target_me  = 1
# NetFun = Storage = 0x0A , CMD = 0x48
get_sel_time_target_bmc = 0
get_sel_time_target_me  = 1
## SPS OEM CMD LIST:
# 60h request data define
nmptu_60h_no_launch  = 0
nmptu_60h_launch     = 1
nmptu_60h_lanuch_hw  = 2
# 61h request data define
nmptu_61h_platform  = 0
nmptu_61h_cpu     = 1
nmptu_61h_memory  = 2
# F2h Domain Data define
f2h_platform_domain      = 0
f2h_cpu_domain           = 1
f2h_memory_domain        = 2
f2h_hw_protection_domain = 3
f2h_hpio_domain          = 4
# CBh Domain Data define
cbh_platform_domain      = 0
cbh_cpu_domain           = 1
cbh_memory_domain        = 2
cbh_hw_protection_domain = 3
cbh_hpio_domain          = 4
# C8h Domain Data define
platform_domain      = 0
cpu_domain           = 1
memory_domain        = 2
hw_protection_domain = 3
hpio_domain          = 4
# C8/C1h Power Domain define
AC_power_side        = 0
DC_power_side        = 1
# C8h Mode define
global_power_mode                = 1
global_inlet_temp_mode           = 2
global_throttling_sts_mode       = 3
#6Ah: Byte4[3:0], Control and Scope
hwpm_6ah_performance_preference   = 0
hwpm_6ah_performance_bias         = 1
#6Ah: Byte4[7:6], Control and Scope
hwpm_6ah_scope_entire_platform    = 0
hwpm_6ah_scope_cpu_scope          = 1
# C1h: Byte4,Domain ID define
c1h_platform_domain      = 0
c1h_cpu_domain           = 1
c1h_memory_domain        = 2
c1h_hw_protection_domain = 3
c1h_hpio_domain          = 4
# C1h: Byte4 bit[4] , policy enable
c1h_policy_enable        = 1
c1h_policy_disable       = 0
# C1h: Byte6[3:0],Policy Trigger Type define :
c1h_no_policy_trigger             = 0
c1h_inlet_temp_trigger            = 1
c1h_missing_power_reading_trigger = 2
c1h_time_after_HR_trigger         = 3
c1h_boot_time_trigger             = 4
c1h_mgpio_trigger                 = 6
# C1h : Byte6[4]
c1h_remove_policy        = 0
c1h_add_policy           = 1
# C1h : Byte6[6:5]
c1h_auto_aggressive    = 0
c1h_unaggressive       = 1
c1h_force_aggressive   = 2
# C1h : Byte6[7]
c1h_presistent         = 0
c1h_volatile           = 1
# C1h:Byte7 bit[0], Exception action alert
c1h_alert_disable      = 0
c1h_alert_enable       = 1
# C1h:Byte7 bit[1], Exception action shutdwon
c1h_shutdown_disable   = 0
c1h_shutdown_enable    = 1
# C1h:Byte[15:14],  policy trigger type = 0 , 4 , 6. These two bytes can be set 0 to ignore
c1h_trigger_limit_null = 0
# C1h:Byte[17:16],  statistic report period in sec
c1h_minimum_report_period = 1
# C0h:Byte4[2:0]
c0h_global_disable      = 0
c0h_global_enable       = 1
c0h_domain_disable      = 2
c0h_domain_enable       = 3
c0h_policy_disable      = 4
c0h_policy_enable       = 5
#C0h:Byte5[3:0]:Domain
c0h_platform_domain      = 0
c0h_cpu_domain           = 1
c0h_memory_domain        = 2
c0h_hw_protection_domain = 3
c0h_hpio_domain          = 4
# DFH:Byte4, Command
dfh_command_recovery        = 1
dfh_command_restore_default = 2
dfh_command_ptt_restore     = 3
#D4H:Byte4 [5:4]: Control_Knob
d4h_ctl_knob_max_pt         = 0
d4h_ctl_knob_max_cores      = 1
#D2H:Byte4[5:4] : Control_Knob
d2h_ctl_knob_max_pt         = 0
d2h_ctl_knob_max_cores      = 1
#D3H:Byte4[5:4] : Control_Knob
d3h_ctl_knob_max_pt         = 0
d3h_ctl_knob_max_cores      = 1
#D0H:Byte4[3:0] : Domain
d0h_platform_domain      = 0
d0h_cpu_domain           = 1
d0h_memory_domain        = 2
d0h_hw_protection_domain = 3
d0h_hpio_domain          = 4
#D0H:Byte4[7]: Control component_identifier
d0h_component_control_disable = 0
d0h_component_control_enable = 1
# 40h: Byte4 bit[7:6] :Interface select
peci_40h_interface_fall_back   = 0
peci_40h_interface_inbend_peci = 1
peci_40h_inteface_peci_wire    = 2
# 40h: byte4 bit[5:0] : CPU client address
peci_40h_client_addr_cpu0 = 0x30
peci_40h_client_addr_cpu1 = 0x31
peci_40h_client_addr_cpu2 = 0x32
peci_40h_client_addr_cpu3 = 0x33
# 65h: byte4 parameter_selector : 01 = CUPS index, 02= Dynamic load factors
cups_65h_cups_index = 0x01
cups_65h_dynamic_load_factors = 0x02
# D9H:byte4 bit[3:1] 
d9h_trans_type_send_byte         = 0
d9h_trans_type_read_byte         = 1
d9h_trans_type_write_byte        = 2
d9h_trans_type_read_word         = 3
d9h_trans_type_write_word        = 4
d9h_trans_type_block_read        = 5
d9h_trans_type_block_write       = 6
d9h_trans_type_block_wr_pro_call = 7
#D9H:byte4 bit[5:4]
d9h_stardard_device_addr = 0
d9h_extended_device_addr = 1
#D9H:byte4 bit[6]
d9h_pec_report = 1
#D9H:byte4 bit[7]
d9h_pec_en = 1
#D9H:byte5: Sensor Bus
d9h_smbus = 0
d9h_sml0 = 1
d9h_sml1 = 2
d9h_sml2 = 3
d9h_sml3 = 4
d9h_sml4 = 5
#D9H:byte10: Transmission Protocol
d9h_trans_potocol_pmbus = 0
d9h_trans_potocol_i2c = 1
# d7h Domain Data define
d7h_platform_domain      = 0
### RAW PECI CMD CODE
# CPU_ID
CPU0         = 0
CPU1         = 1
CPU2         = 2
CPU3         = 3
# GET TEMP
GET_TEMP     = 0x01
RdPkgConfig  = 0xa1
WrPkgConfig  = 0xa5
RdIAMSR      = 0xb1
RdPCIConfig  = 0x61

### PMbus CMD CODE
PMBUS_GET_VERSION = 0x98
PMBUS_READ_EIN    = 0x86
PMBUS_READ_EOUT   = 0x87
PMBUS_READ_PIN    = 0x97
PMBUS_READ_POUT   = 0x96
PMBUS_READ_WRITE_OT_WARM_LIMIT = 0x51
PMBUS_PAGE_PLUS_WRITE = 0x05
PMBUS_PAGE_PLUS_WRITE_BYTE_COUNT = 3
PMBUS_PAGE_PLUS_READ = 0x06
PMBUS_PAGE_PLUS_READ_BYTE_COUNT = 2
##PMBUS READ LEN 
PMBUS_GET_VERSION_READ_LEN = 1
PMBUS_READ_EIN_READ_LEN = 7
PMBUS_READ_EOUT_READ_LEN = 7
PMBUS_READ_PIN_READ_LEN = 2
PMBUS_READ_POUT_READ_LEN = 2
# PMBUS PSU PAGE
PMBUS_PSU_BMC_PAGE = 0
PMBUS_PSU_ME_PAGE = 1
# PMBUS PSU STATUS REGISTERS Define
PMBUS_STATUS_WORD_79H = 0x79
PMBUS_STATUS_IOUT_7BH = 0x7B
PMBUS_STATUS_INPUT_7CH = 0x7C
PMBUS_STATUS_TEMPERATURE_7DH =0x7D
PMBUS_STATUS_FANS_81H =  0x81
# 4BH:byte4 bit[3:0]
get_temp_4bh_no_cpu              = 0
get_temp_4bh_all_cpu             = 15
# 4BH:byte4 bit[5:4] - 0 = CPU0~3, 1= CPU4~7, other = reserve
get_temp_4bh_cpu_domain0              = 0
get_temp_4bh_cpu_domain1              = 1
get_temp_4bh_cpu_domain2              = 2
get_temp_4bh_cpu_domain3              = 3
# 4BH:byte4 bit[6] - 0 = Channel0~3, 1 = Channel4~7
get_temp_4bh_mem_domain0              = 0
get_temp_4bh_mem_domain1              = 1
# 4BH:byte4 bit[7] - 0 = standard, 1 = extended
get_temp_4bh_standard              = 0
get_temp_4bh_extended              = 1
# 4BH:byte5~byte20
get_temp_4bh_channel_all          = '0xFF'
get_temp_4bh_channel_none         = '0'




