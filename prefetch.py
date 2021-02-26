import os
import csv
import glob
from datetime import datetime, timedelta
import struct
from XPRESS_decompress import *

def Win_ts(timestamp):
    WIN32_EPOCH = datetime(1601, 1, 1)
    return WIN32_EPOCH + timedelta(microseconds=timestamp//10, hours=9)

Pdir_path= ""
PF_file_list =  ""
PF_file_Name_List = ""

PF_file_Name, PF_file_Size, PF_file_Last_Run_Time, PF_file_Created_Time, PF_file_Modified_Time, PF_file_Run_Count = [],[],[],[],[],[]
PF_Data=[]

def prefetch_parser():
	cut = 0
	PF_file_list =  glob.glob(Pdir_path+'/*.pf')
	PF_file_Name_List = os.listdir(Pdir_path)

	for PF_file in PF_file_list:
		Data = decompress(PF_file)
		PF_file_Name.append("".join(map(chr,Data[16:75])))
		PF_file_Size.append(struct.unpack_from("<i",(Data[0x0C:]))[0])
		PF_file_Last_Run_Time.append(Win_ts(struct.unpack_from("<Q", Data[0x80:])[0]).strftime('%Y:%m:%d-%H:%M:%S.%f'))
		PF_file_Created_Time.append(datetime.fromtimestamp(os.path.getctime(PF_file)).strftime('%Y:%m:%d-%H:%M:%S.%f'))
		PF_file_Modified_Time.append(datetime.fromtimestamp(os.path.getmtime(PF_file)).strftime('%Y:%m:%d-%H:%M:%S.%f'))
		PF_file_Run_Count.append(struct.unpack_from("<i", Data[0xD0:])[0])
			
		PF_Data.append((PF_file_Name[cut], PF_file_Size[cut], PF_file_Last_Run_Time[cut], PF_file_Created_Time[cut], PF_file_Modified_Time[cut], PF_file_Run_Count[cut]))

		cut +=1

	return len(PF_file_Name_List)



def prefetch_output_csv(path):
	f = open(path+'/Prefetch_info.csv', 'w', encoding='utf-8', newline='')
	wr = csv.writer(f)
	wr.writerow(["File_Name", "File_Size", "Last_Run_Time", "Created_Time", "Modified_Time", "Run_Count"])

	for i, (name, size, run_time, created_time, modified_time, run_count) in enumerate(PF_Data):
		wr.writerow([name, str(size)+' byte', run_time, created_time, modified_time, str(run_count)])

	print(i)
	f.close()
