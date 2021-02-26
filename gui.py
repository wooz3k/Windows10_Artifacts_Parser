import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic, QtSql
import sqlite3 as sq
import prefetch
import lnk
import registry
import pytz
from datetime import datetime, timedelta, timezone

def Win_ts(timestamp):
    epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    result_datetime=epoch+timedelta(microseconds=timestamp)
    return result_datetime

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("mainwindow.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('WinArti')
        self.setWindowIcon(QtGui.QIcon('WinArti.png'))

        self.dir_path_btn_p.clicked.connect(self.dir_path_search_p)
        self.go_btn_p.clicked.connect(self.prefetch_Function)
        self.csv_btn_1.clicked.connect(self.csv_download_p)

        self.dir_path_btn_LNK.clicked.connect(self.dir_path_search_LNK)
        self.go_btn_LNK.clicked.connect(self.lnk_Function)
        self.csv_btn_2.clicked.connect(self.csv_download_LNK)

        self.go_btn_r.clicked.connect(self.registry_Function)

        self.dir_path_btn_t.clicked.connect(self.dir_path_search_time)
        self.go_btn_t.clicked.connect(self.time_Function)
    
    def time_Function(self):
        conn = sq.connect(self.dir_path_time.text())
        cur = conn.cursor()
    
        sql = "SELECT AppId, PackageIdHash, AppActivityId, StartTime, LastModifiedOnClient FROM Activity"
        cur.execute(sql)
        rows = cur.fetchall()        
    
        conn.close()

        count = len(rows)
        
        self.dtable_3.setColumnCount(5)
        self.dtable_3.setRowCount(count)
        self.dtable_3.setHorizontalHeaderLabels(["AppId", "PackageIdHash", "AppActivityId", "StartTime", "LastModifiedOnClient"])

        for x in range(count):
            appid, packageid_hash, appactivityid, starttime, LastModified = rows[x]

            self.dtable_3.setItem(x, 0, QtWidgets.QTableWidgetItem(appid))
            self.dtable_3.setItem(x, 1, QtWidgets.QTableWidgetItem(packageid_hash))
            self.dtable_3.setItem(x, 2, QtWidgets.QTableWidgetItem(appactivityid))
            self.dtable_3.setItem(x, 3, QtWidgets.QTableWidgetItem(Win_ts(starttime).strftime('%Y:%m:%d-%H:%M:%S.%f')))
            self.dtable_3.setItem(x, 4, QtWidgets.QTableWidgetItem(Win_ts(LastModified).strftime('%Y:%m:%d-%H:%M:%S.%f')))
            
            print(starttime)


    def registry_Function(self):
        self.label_3.setText(registry.Windows_info())

    def prefetch_Function(self):
        prefetch.Pdir_path=self.dir_path_p.text()
        row_len_size=prefetch.prefetch_parser()

        self.dtable_1.setColumnCount(6)
        self.dtable_1.setRowCount(row_len_size)
        self.dtable_1.setHorizontalHeaderLabels(["File_Name", "File_Size", "Last_Run_Time", "Created_Time", "Modified_Time", "Run_Count"])

        c=0

        for i, (name, size, run_time, created_time, modified_time, run_count) in enumerate(prefetch.PF_Data):
            self.dtable_1.setItem(c, 0, QtWidgets.QTableWidgetItem(name.replace(" ","")))
            self.dtable_1.setItem(c, 1, QtWidgets.QTableWidgetItem(str(size)))
            self.dtable_1.setItem(c, 2, QtWidgets.QTableWidgetItem(run_time))
            self.dtable_1.setItem(c, 3, QtWidgets.QTableWidgetItem(created_time))
            self.dtable_1.setItem(c, 4, QtWidgets.QTableWidgetItem(modified_time))
            self.dtable_1.setItem(c, 5, QtWidgets.QTableWidgetItem(str(run_count)))
            
            c+=1
        
        print(i)
        
        self.dtable_1.setSortingEnabled(False) # 정렬기능 self.table.resizeRowsToContents() 
        self.dtable_1.resizeColumnsToContents() # 이것만으로는 checkbox 컬럼은 잘 조절안됨. 
        self.dtable_1.setColumnWidth(0, 50) # checkbox 컬럼 폭 강제 조절.

        hheader = self.dtable_1.horizontalHeader() # qtablewidget --> qtableview --> horizontalHeader() --> QHeaderView 
        hheader.sectionClicked.connect(self._horizontal_header_clicked_p)
    
    def lnk_Function(self):
        lnk.LDir_path=self.dir_path_LNK.text()
        row_len_size=lnk.lnk_parser()

        self.dtable_2.setColumnCount(6)
        self.dtable_2.setRowCount(row_len_size)
        self.dtable_2.setHorizontalHeaderLabels(["LNK_File_Name", "Creation_Time", "Created_Time" ,"Access_Time", "Write_Time", "File_Size"])

        c=0

        for i, (name, creation_time, created_time, access_time, write_time, size) in enumerate(lnk.LNK_Data):
            self.dtable_2.setItem(c, 0, QtWidgets.QTableWidgetItem(name.replace(" ","")))
            self.dtable_2.setItem(c, 1, QtWidgets.QTableWidgetItem(creation_time))
            self.dtable_2.setItem(c, 2, QtWidgets.QTableWidgetItem(created_time))
            self.dtable_2.setItem(c, 3, QtWidgets.QTableWidgetItem(access_time))
            self.dtable_2.setItem(c, 4, QtWidgets.QTableWidgetItem(write_time))
            self.dtable_2.setItem(c, 5, QtWidgets.QTableWidgetItem(str(size)))

            c+=1
        
        self.dtable_2.setSortingEnabled(False) # 정렬기능 self.table.resizeRowsToContents() 
        self.dtable_2.resizeColumnsToContents() # 이것만으로는 checkbox 컬럼은 잘 조절안됨. 
        self.dtable_2.setColumnWidth(0, 30) # checkbox 컬럼 폭 강제 조절.

        hheader = self.dtable_2.horizontalHeader() # qtablewidget --> qtableview --> horizontalHeader() --> QHeaderView 
        hheader.sectionClicked.connect(self._horizontal_header_clicked_LNK)

        self.dir_path_btn_LNK.clicked.connect(self.dir_path_search_LNK)
        self.go_btn_LNK.clicked.connect(self.lnk_Function)
    
    def csv_download_p(self):
        path=(QtWidgets.QFileDialog.getExistingDirectory())
        prefetch.prefetch_output_csv(path)
    
    def csv_download_LNK(self):
        path=(QtWidgets.QFileDialog.getExistingDirectory())
        lnk.lnk_output_csv(path)

    def dir_path_search_p(self):
        self.dir_path_p.setText(QtWidgets.QFileDialog.getExistingDirectory())

    def dir_path_search_LNK(self):
        self.dir_path_LNK.setText(QtWidgets.QFileDialog.getExistingDirectory())

    def dir_path_search_time(self):
        self.dir_path_time.setText(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './')[0])
    
    def _horizontal_header_clicked_p(self, idx): 
        self.dtable_1.setSortingEnabled(True) 
        self.dtable_1.setSortingEnabled(False) 
    
    def _horizontal_header_clicked_LNK(self, idx): 
        self.dtable_1.setSortingEnabled(True) 
        self.dtable_1.setSortingEnabled(False) 

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QtWidgets.QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
