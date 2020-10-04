import os
import csv
import glob
from datetime import datetime, timedelta
import struct
from XPRESS_decompress import *

def Win_ts(timestamp):
    WIN32_EPOCH = datetime(1601, 1, 1)
    return WIN32_EPOCH + timedelta(microseconds=timestamp//10, hours=9)

Dir_path=sys.argv[1]
PF_file_list =  glob.glob(Dir_path+'/*.pf')
PF_file_Name_List = os.listdir(Dir_path)

PF_file_Name, PF_file_Size, PF_file_Last_Run_Time, PF_file_Created_Time, PF_file_Modified_Time, PF_file_Run_Count = [],[],[],[],[],[]

cut = 0

f = open('Prefetch_info.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(["PF_File_Name", "File_Name", "File_Size", "Last_Run_Time", "Created_Time", "Modified_Time", "Run_Count"])

for PF_file in PF_file_list:
	Data = decompress(PF_file)
	PF_file_Name.append("".join(map(chr,Data[16:75])))
	PF_file_Size.append(struct.unpack_from("<i",(Data[0x0C:]))[0])
	PF_file_Last_Run_Time.append(Win_ts(struct.unpack_from("<Q", Data[0x80:])[0]).strftime('%Y:%m:%d-%H:%M:%S.%f'))
	PF_file_Created_Time.append(datetime.fromtimestamp(os.path.getctime(PF_file)).strftime('%Y:%m:%d-%H:%M:%S.%f'))
	PF_file_Modified_Time.append(datetime.fromtimestamp(os.path.getmtime(PF_file)).strftime('%Y:%m:%d-%H:%M:%S.%f'))
	PF_file_Run_Count.append(struct.unpack_from("<i", Data[0xD0:])[0])
		
	print('[*]File_Name:'+ str(PF_file_Name[cut]))
	print('[**]File_Size:' + str(PF_file_Size[cut])+'byte')
	print('[***]Last_Run_Time:' + str(PF_file_Last_Run_Time[cut]))
	print('[****]Created_Time:' + str(PF_file_Created_Time[cut]))
	print('[*****]Modified_Time:' + str(PF_file_Modified_Time[cut]))
	print('[******]Run_Count: '+ str(PF_file_Run_Count[cut]))
	print('\n')

		
	cut +=1
		

cut = 0

for PF in PF_file_Name_List:
	if PF.endswith('.pf'):
		wr.writerow([PF, PF_file_Name[cut], str(PF_file_Size[cut])+' byte', PF_file_Last_Run_Time[cut], PF_file_Created_Time[cut], PF_file_Modified_Time[cut], PF_file_Run_Count[cut]])
		cut+=1

f.close()

print('Finished')