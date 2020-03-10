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

#Import path
from os_parameters_define import *
from utility_function import *
from nm_ipmi_raw_to_str import *
from error_messages_define import *
from nm_functions import *
from config import *

# Import src
sys.path.append('src/')
from get_device_id import *



## _Main_ ##

print 'Start to Test IPMI_001...'
sts, sps_version, platform, dcmi, nm, image  = get_device_id_py(ipmi)

if(sts == PASS ):
	# Show Result
	print('SPS Version = '+ sps_version)
	print('platform = %d' %platform  )
	print('dcmi =%d' %dcmi)
	print('nm = %d' %nm)
	print('image = %d' %(image))

	if(image == 0 ):
		print colored ('IPMI_001 Fail, SPS ME not in operation mode' , 'red')
	else:
        	print colored ('IPMI_001 Pass' , 'green')
else:
         print colored ('IPMI_001 Fail, Aardvark data transfer error or initial error ' , 'red')

