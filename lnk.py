import os
import csv
import glob
from datetime import datetime, timedelta
import struct
import sys
import binascii

def raw_data(filename):
    with open(filename, 'rb') as f:
       content = f.read()
    return bytearray(content)

def Win_ts(timestamp):
    WIN32_EPOCH = datetime(1601, 1, 1)
    return WIN32_EPOCH + timedelta(microseconds=timestamp//10, hours=9)

Dir_path=sys.argv[1]
LNK_file_list =  glob.glob(Dir_path+'/*.lnk')
LNK_file_Name_List = os.listdir(Dir_path)

LNK_File_Name, LNK_Creation_Time, LNK_File_Created_Time, LNK_Access_Time, LNK_Write_Time, LNK_File_Size = [],[],[],[],[],[]

f = open('LNK_info.csv', 'w', encoding='utf-8', newline='')

wr = csv.writer(f)
wr.writerow(["LNK_File_Name", "Creation_Time", "Created_Time" ,"Access_Time", "Write_Time", "File_Size"])

cut = 0

for LNK_file in LNK_file_list:
    Data = raw_data(LNK_file)
    LNK_File_Name = LNK_file_Name_List
    LNK_Creation_Time.append(Win_ts(struct.unpack_from("<Q", Data[0x1C:])[0]).strftime('%Y:%m:%d-%H:%M:%S.%f'))
    LNK_File_Created_Time.append(datetime.fromtimestamp(os.path.getctime(LNK_file)).strftime('%Y:%m:%d-%H:%M:%S.%f'))
    LNK_Access_Time.append(Win_ts(struct.unpack_from("<Q", Data[0x24:])[0]).strftime('%Y:%m:%d-%H:%M:%S.%f'))
    LNK_Write_Time.append(Win_ts(struct.unpack_from("<Q", Data[0x2C:])[0]).strftime('%Y:%m:%d-%H:%M:%S.%f'))
    LNK_File_Size.append(struct.unpack_from("<i",(Data[0x34:]))[0])
    
    print('[*]File_Name :'+ str(LNK_File_Name[cut]))
    print('[**]Creation_Time :' + str(LNK_Creation_Time[cut]))
    print('[***]Created_Time :' + str(LNK_File_Created_Time[cut]))
    print('[****]Access_Time :' + str(LNK_Access_Time[cut]))
    print('[*****]Write_Time : '+ str(LNK_Write_Time[cut]))
    print('[*****]File_Size : ' + str(LNK_File_Size[cut])+'byte')
    print('\n')
    
    cut +=1
		

cut = 0

for LNK in LNK_file_Name_List:
    if LNK.endswith('.lnk'):
        wr.writerow([LNK_File_Name[cut], LNK_Creation_Time[cut], LNK_File_Created_Time[cut], LNK_Access_Time[cut], LNK_Write_Time[cut], str(LNK_File_Size[cut])+'byte'])
        cut+=1

f.close()

print('Finished')