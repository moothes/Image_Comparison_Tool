import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Settings(QWidget):
    signal = pyqtSignal(int)
    
    def __init__(self, config):
        super().__init__()

        self.setWindowTitle('Settings')
        self.config = config
        self.default_path = os.path.dirname(config['folders'][0]) if config['folders'] is not None else ''
        #if settings is None:
        #    self.result = {'path': self.default_path, 'rename': False, 'eps': False, 'num_folder': 4}
        #else:
        #    self.result = settings
        
        lbl = QLabel(self)
        lbl.setText('number of folder:')
        lbl.setGeometry(130, 10, 100, 30)
        self.le_num = QLineEdit(self)
        self.le_num.setText(str(config['num_fold']))
        self.le_num.setGeometry(240, 10, 60, 30)
        
        lbl1 = QLabel(self)
        lbl1.setText('save path:')
        lbl1.setGeometry(80, 50, 100, 30)
        self.qle = QLineEdit(self)
        self.qle.setText(self.default_path)
        self.qle.setGeometry(145, 50, 200, 30)
        
        self.btn = QPushButton(self, text="Open")
        self.btn.clicked.connect(self.open_folder)
        
        self.btn.setGeometry(360, 50,  70, 30)
        
        self.checkBox1 = QCheckBox("rename", self)
        self.checkBox1.setChecked(config['rename'])
        self.checkBox2 = QCheckBox("to eps", self)
        self.checkBox2.setChecked(config['eps'])
        
        self.checkBox1.setGeometry(130, 90, 90, 30)
        self.checkBox2.setGeometry(250, 90, 90, 30)
        
        btn_close = QPushButton(self, text="Ok")
        btn_close.clicked.connect(self.close_window)
        btn_close.setGeometry(220, 130, 70, 30)
        
    def open_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "C:/Users/admin/Desktop/")
        self.qle.setText(dir_path)
        self.config['path'] = dir_path
        
    def close_window(self):
        new_num_fold = int(self.le_num.text())
        old_num_fold = self.config['num_fold']
        if new_num_fold > old_num_fold:
            for i in range(new_num_fold - old_num_fold):
                self.config['folders'].append('')
        else:
            self.config['folders'] = self.config['folders'][:new_num_fold]
        
        refrash = new_num_fold != old_num_fold
        self.config['num_fold'] = new_num_fold
        self.config['rename'] = self.checkBox1.isChecked()
        self.config['eps'] = self.checkBox2.isChecked()
        self.signal.emit(int(refrash))
        self.close()

class LoadWindow(QWidget):
    signal = pyqtSignal()

    def __init__(self, config):
        super().__init__()
        h = 65
            
        self.config = config
        #self.config = {'num_fold': 4, 'folders': None, 'img_list': [], 'num_img': 0, 'path': '', 'rename': False, 'eps': False}
        
        self.setWindowTitle('Folder Path')
        self.resize(580, 80 + h * config['num_fold'])
        self.setFixedSize(self.width(), self.height())

        btn_close = QPushButton(self, text="show")
        btn_close.clicked.connect(self.close_window)
        btn_close.setGeometry(210, 30 + h * config['num_fold'], 170, h - 35)
        
        
        self.lbls = []
        self.qles = []
        self.btns = []
        for i in range(config['num_fold']):
            btn = QPushButton(self, text="Folder {}".format(i))
            btn.tag = i
            btn.clicked.connect(self.open_folder)
            
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
        
        #if config['folders'] is not None:
        #   #self.folds = config['folders']
        #   #self.num_img = config['num_img']
        #   #self.img_list = config['img_list']
        for i, fold in enumerate(config['folders']):
            self.qles[i].setText(fold)
                
        # first time
        '''
        else:
            self.img_list = []
            self.num_img = 0
            self.folds = ['',] * num_fold
        '''

    def open_folder(self):
        idx = self.sender().tag
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "C:/Users/admin/Desktop/debug1/debug")
        self.qles[idx].setText(dir_path)
        self.config['folders'][idx] = dir_path
        
        img_list = os.listdir(dir_path)
        if not idx:
            self.config['img_list'] = []
            for img_name in img_list:
                suffix = img_name.split('.')[-1]
                if suffix in ['jpg', 'png', 'bmp']:
                    self.config['img_list'].append(img_name)
            self.config['num_img'] = len(self.config['img_list'])
            self.config['path'] = os.path.dirname(self.config['folders'][idx])
            img_list = self.config['img_list']
        
        self.lbls[idx].setText('toal {} files.'.format(len(img_list)))
    
    def close_window(self):
        if self.qles[0].text() == '':
            return
        self.signal.emit()
        self.close()