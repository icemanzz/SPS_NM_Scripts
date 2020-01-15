#from file_path_handle import *
from os_parameters_define import *
from error_messages_define import *
from config import *
import os
import re
import datetime
import os.path
import time
import math
import numpy
import mmap

#### Below are define some basic utility function for all modules

def DEBUG(str):
     if(DEBUG_ENABLE == 1):
          print(str)
          return
     else:
          return

## Function : Bit Set
def BIT(offset):
     data = 1 << offset

     return data

## Function : Bit shift left
def bit_shift_left(data , offset):
     data = data << offset

     return data

## Function : Bit shift right
def bit_shift_right(data , offset):
     data = data >> offset

     return data

## Function : Bit Cut
def bits_cut( data , offset , length):
     loop     = 0
     cut_data = 0
     for loop in range(0 , length ):
         cut      = 1 << ( offset + loop )
         cut_data = cut_data + cut
     result = (data & cut_data) >> offset
     #DEBUG('bit_but: result = %d' %result)

     return result

## Function : transfer to 2's complement format
## input = floating decimal value
## output = int value
def two_complement( data , num_bits):
     x = int(data)
     y = bin(x)
     z = int(y,2)
     result = z - (1 << num_bits)
     DEBUG('2s complement value = % 4d' %result)

     return result

## Function : int to hex format transfer
def int_to_hex_string(data):
     str = '0x'+ format(data,'02x')
     DEBUG(int_to_hex_string.__name__ + ':'+ str)
     return str

## Function : Calculate Byte value
def calculate_byte_value(resp, start_byte, number ):
     # Calculate data location: note completion code = byte 1
     offset = (start_byte - 2)* 2 + (start_byte - 2) + 1
     # Calculate value for each byte
     loop = 0
     acc_data = 0
     for loop in range(0, number ):
         # Calculate Byte value, low byte
         low_byte_multiple_number = loop * 2
         high_byte_multiple_number = (loop * 2) + 1
         val_high = int('0x'+resp[(offset + loop*3) ],0)*math.pow(16,high_byte_multiple_number)
         val_low  = int('0x'+resp[((offset + 1) + (loop*3)) ],0)*math.pow(16,low_byte_multiple_number)
         acc_data = acc_data + val_high + val_low

     return acc_data

## Function : Calculate Byte value
def calculate_byte_value_py(resp, start_byte, number ):
     loop = 0
     acc_data = 0
     for loop in range(0, number):
     # Calculate value for each byte
	     acc_data = acc_data + ord(resp[start_byte + loop -1])*math.pow(256,loop)

     return acc_data

## Function : Converter Int value to HEX str text format
def int_to_hex_text_format(data, length):
     loop = 0
     result = []
     for loop in range(0, length):
         result.append('0x'+ format(data[loop],'02x'))
         DEBUG('int_to_hex_text_format: result[loop]='+ result[loop])

     return result

## Function : Converter Int value to HEX value
def int_to_hex( int_data, byte_number ):
     loop = 0
     result = numpy.zeros(byte_number,int)
     for loop in range(0, byte_number):
         val_high = int_data / 256
         val_low  = int_data % 256
         int_data = val_high
         DEBUG('loop = %d' %loop)
         DEBUG(val_low)
         result[loop] = val_low
     result_str = int_to_hex_text_format(result, byte_number)

     return result_str

## Function : Cut Bytes
def cut_byte(resp, start_byte, number ):
     # Calculate data location: note completion code = byte 1
     offset = (start_byte - 2)* 2 + (start_byte - 2) + 1
     DEBUG('cut_byte : offset = %d' %offset)
     DEBUG(resp[offset])
     # Calculate value for each bytes
     loop = 0
     data = numpy.zeros(number,int)
     for loop in range(0, number ):
         val  = int('0x'+resp[(offset + loop*3) ] + resp[((offset + 1) + (loop*3)) ],0)
         data[loop] = val

     return data


## Function : Get Specific bits data from IPMI Resp data. Note: only support 1 byte
def get_bits_data(resp, start_byte, bits_offset, bits_length ):
     int_bytes = cut_byte(resp, start_byte, 1)
     int_bits  = bits_cut(int_bytes[0], bits_offset, bits_length)

     return int_bits

## Function : Get Specific bits data from IPMI Resp data. Note: only support 1 byte
def get_bits_data_py(resp, bits_offset, bits_length ):
     int_bits  = bits_cut(resp, bits_offset, bits_length)

     return int_bits

## Function : Respond Data Analyst and Error filter
def ipmi_resp_analyst( resp , cmd_type):
     # Check if rsp data correct
     if(len(resp) == 0 ):
         DEBUG(IPMI_SEND_ERROR)
         return ERROR
     if(cmd_type == OEM):
         if(resp[1]!='5' and resp[2]!='7'):
             DEBUG(ME_OEM_RSP_ERROR)
             return ERROR

     return SUCCESSFUL

## Function : Respond Data Analyst and Error filter
def ipmi_resp_analyst_py( CC, cmd_type):
     if(CC != 0):
         DEBUG(IPMI_SEND_ERROR)
         return ERROR
     return SUCCESSFUL

     
## Fucntion : Search a keyword from file and get data from key word offset.
## resp_length : how many text you want to get from file.
## format_option = 0 = str ;;; format_option = 1 = int
def read_keyword_file(file_path, key_word, offset , resp_length, format_option):
     f = open(file_path, 'r+b')
     mf = mmap.mmap(f.fileno(), 0)
     mf.seek(0) # reset file cursor
     # Detect Key Word location
     m = re.search(key_word, mf)
     # print data location
     #DEBUG('read_keyword_file(): key word location as below range in file:')
     #DEBUG( m.start())
     #DEBUG( m.end())
     # Serch data from keyword + offset location, storage data in str format
     mf.seek((int(m.start()) + offset))
     str = mf.readline()
     if(format_option == 0):
         DEBUG('read_keyword_file(): Return data is string aray')
         return str[0:resp_length]
     elif(format_option == 1):
         # Convert str to int
         int_resp = int(str[0:resp_length], 0)
         DEBUG('read_keyword_file(): resp = %16d' %int_resp)
         return int_resp
     elif(format_option == 2):
         # Convert str to hex
         hex_resp = int(str[0:resp_length], 16)
         DEBUG('read_keyword_file(): resp = %x' %hex_resp)
         return hex_resp
     else:
         DEBUG('read_keyword_file(): format_option parameters cannot identify')
         return ERROR

     return ERROR

## Fucntion : Search a keyword from file and get data from key word offset.
## resp_length : how many text you want to get from file.
## format_option = 0 = str ;;; format_option = 1 = int
def read_keyword_file_from_end(file_path, key_word, offset , resp_length, format_option):
     f = open(file_path, 'r+b')
     mf = mmap.mmap(f.fileno(), 0)
     mf.seek(0) # reset file cursor
     # Detect Key Word location
     m = re.search(key_word, mf)
     # print data location
     #DEBUG('read_keyword_file(): key word location as below range in file:')
     #DEBUG( m.start())
     #DEBUG( m.end())
     # Serch data from keyword + offset location, storage data in str format
     mf.seek((int(m.end()) + offset))
     str = mf.readline()
     if(format_option == 0):
         DEBUG('read_keyword_file(): Return data is string aray')
         return str[0:resp_length]
     elif(format_option == 1):
         # Convert str to int
         int_resp = int(str[0:resp_length], 0)
         DEBUG('read_keyword_file(): resp = %16d' %int_resp)
         return int_resp
     elif(format_option == 2):
         # Convert str to hex
         hex_resp = int(str[0:resp_length], 16)
         DEBUG('read_keyword_file(): resp = %x' %hex_resp)
         return hex_resp
     else:
         DEBUG('read_keyword_file(): format_option parameters cannot identify')
         return ERROR

     return ERROR


## Fucntion : Search a keyword from file and get data from key word offset.
def search_keyword_file(file_path, key_word):
     f = open(file_path, 'r+b')
     mf = mmap.mmap(f.fileno(), 0)
     mf.seek(0) # reset file cursor
     # Detect Key Word location
     m = re.search(key_word, mf)
     if(m):
          # print data location
         DEBUG('read_keyword_file(): key word location as below range in file:')
         DEBUG( m.start())
         DEBUG( m.end())
         A = m.end() - m.start()
         DEBUG('A = %d' %A)
         return SUCCESSFUL 
     else:
         DEBUG('Key word not exist')
         return ERROR

     return ERROR



