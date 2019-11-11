import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ExportSetting(QWidget):
    getSettings = pyqtSignal()
    
    def __init__(self, settings, folds):
        super().__init__()

        self.setWindowTitle('Export Settings')
        assert len(folds) > 0
        self.default_path = os.path.dirname(folds[0])
        if settings is None:
            self.result = {'path': self.default_path, 'rename': False, 'eps': False}
        else:
            self.result = settings
            
        self.qle = QLineEdit(self)
        self.qle.setFocusPolicy(Qt.NoFocus)
        self.qle.setText(self.result['path'])
        
        self.btn = QPushButton(self, text="Open")
        self.btn.clicked.connect(self.open_folder)
        #btn.clicked.connect(lambda: self.open_folder(i - 1))
        
        self.btn.setGeometry( 50, 40,  70, 30)
        self.qle.setGeometry(145, 40, 250, 30)
        
        self.checkBox1 = QCheckBox("rename", self)
        self.checkBox1.setChecked(self.result['rename'])
        self.checkBox2 = QCheckBox("to eps", self)
        self.checkBox2.setChecked(self.result['eps'])
        
        self.checkBox1.setGeometry( 50, 90, 90, 30)
        self.checkBox2.setGeometry(170, 90, 90, 30)
        
        btn_close = QPushButton(self, text="Ok")
        btn_close.clicked.connect(self.close_window)
        btn_close.setGeometry(170, 140, 70, 30)
        
    def open_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "C:/Users/admin/Desktop/")
        self.qle.setText(dir_path)
        self.result['path'] = dir_path
        
    def close_window(self):
        #if len(self.qle.text()) < 1:
        #    return
        self.result['rename'] = self.checkBox1.isChecked()
        self.result['eps'] = self.checkBox2.isChecked()
        self.close()

    def closeEvent(self, event):
        self.getSettings.emit()

class SetNumber(QWidget):
    set_number = pyqtSignal()
    
    def __init__(self, num_fold):
        super().__init__()
        self.num_fold = num_fold
        
        self.setWindowTitle(' ')
        self.qle = QLineEdit(self)
        self.qle.setGeometry(10, 10, 60, 30)
        
        btn_close = QPushButton(self, text="Set")
        btn_close.clicked.connect(self.close_window)
        btn_close.setGeometry(80, 10, 30, 30)
        
    def close_window(self):
        self.num_fold = int(self.qle.text())
        self.close()

    def closeEvent(self, event):
        self.set_number.emit()

class LoadWindow(QWidget):
    window_close_signal = pyqtSignal()

    def __init__(self, num_fold, folders, img_list, num_img):
        super().__init__()
        
        h = 65
            
        #print(self.parent().folders)
        #num_fold = 4
        self.setWindowTitle('Folder Path')
        self.resize(580, 80 + h * num_fold)
        self.setFixedSize(self.width(), self.height())

        btn_close = QPushButton(self, text="show")
        btn_close.clicked.connect(self.close_window)
        btn_close.setGeometry(210, 30 + h * num_fold, 170, h - 35)
        
        
        self.lbls = []
        self.qles = []
        self.btns = []
        for i in range(num_fold):
            btn = QPushButton(self, text="Folder {}".format(i))
            btn.tag = i
            btn.clicked.connect(self.open_folder)
            #btn.clicked.connect(lambda: self.open_folder(i - 1))
            
            lbl = QLabel(self)
            lbl.setText('plase select folder')
            qle = QLineEdit(self)
            qle.setFocusPolicy(Qt.NoFocus)
            
            btn.setGeometry( 50, h * i + 40,  70, h - 35)
            qle.setGeometry(145, h * i + 40, 250, h - 35)
            lbl.setGeometry(420, h * i + 40, 180, h - 35)
            
            self.lbls.append(lbl)
            self.qles.append(qle)
            self.btns.append(btn)
        
        
        if folders is not None:
            self.folds = folders
            self.num_img = num_img
            self.img_list = img_list
            for i, fold in enumerate(self.folds):
                self.qles[i].setText(fold)
                
        else:
            self.img_list = []
            self.num_img = 0
            self.folds = ['',] * num_fold

    def open_folder(self):
        idx = self.sender().tag
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "C:/Users/admin/Desktop/debug1/debug")
        self.qles[idx].setText(dir_path)
        self.folds[idx] = dir_path
        
        img_list = os.listdir(dir_path)
        if not idx:
            self.img_list = []
            for img_name in img_list:
                if img_name.endswith('jpg') or img_name.endswith('png'):
                    self.img_list.append(img_name)
            self.num_img = len(self.img_list)
        
        num_img = len(img_list)
        self.lbls[idx].setText('toal {} files.'.format(num_img))
        
    def closeEvent(self, event):
        self.window_close_signal.emit()
    
    def close_window(self):
        if self.qles[0].text() == '':
            return
        self.close()