###
### This is manually test enviornment config file
###
################################
## 1.  Below parameter is define target os ip mode :
##      - Set dhcp_ip_mode_en = 0  When you want to manually define static IP settings 
##                                                     The CentOS static IP must be manually edit in parameter  "os_ip_addr" 
##      - Set dhcp_ip_mode_en = 1   When you want to use Ubuntu DHCP service automaticcaly assign IP for Cent OS 
##                                                      The CentOS  IP = dynamic DHCP IP which assign by Ubuntu DHCP service. Tool will automatically search CentOS IP
dhcp_ip_mode_en = 1
################################
## 2.  Below parameter is define CentOS static IP. 
##      When you set " dhcp_ip_mode_en = 0 "  , then "os_ip_addr" parameter must manually set correct CentOS IP.
##      If dhcp_ip_mode_en = 1 ,  then os_ip_addr parameter will be ignored.
os_ip_addr   = '192.168.0.222'
################################
## 3.  Below parameter is define Debug PC OS Type 
##      Your Debug PC can be Windows OS (DEBUG_OS_TYPE = 'win') or Ubuntu OS (DEBUG_OS_TYPE = 'linux').
DEBUG_OS_TYPE = 'linux'
################################
## 4. Below parameter is the Debug Function SWITCH :
##     - DEBUG_ENABLE = 1  ,  Print Debug Message function 
##     - DEBUG_ENABLED= 0 ,  DONT Print Debug Message function
DEBUG_ENABLE = 0
################################
## 5. Below parameter is define the maximum time (in secs) for target system boot into CentOS from system power on. 
##     There are many tests will trigger system on/off process, the timeout value will prenvent tool run into dead loop.
OS_BOOT_FAIL_TIMEOUT = 180
