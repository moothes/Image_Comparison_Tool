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
        lbl.setText('Folders:')
        lbl.setGeometry(50, 10, 100, 30)
        self.le_num = QLineEdit(self)
        self.le_num.setText(str(config['row']))
        self.le_num.setGeometry(110, 10, 40, 30)
        lbl = QLabel(self)
        lbl.setText('×')
        lbl.setGeometry(155, 10, 30, 30)
        self.col_num = QLineEdit(self)
        self.col_num.setText(str(config['col']))
        self.col_num.setGeometry(170, 10, 40, 30)
        
        lbl1 = QLabel(self)
        lbl1.setText('save path:')
        lbl1.setGeometry(50, 50, 100, 30)
        self.qle = QLineEdit(self)
        self.qle.setText(self.default_path)
        self.qle.setGeometry(115, 50, 200, 30)
        
        self.btn = QPushButton(self, text="Open")
        self.btn.clicked.connect(self.open_folder)
        
        self.btn.setGeometry(350, 50,  70, 30)
        
        self.checkBox1 = QCheckBox("rename", self)
        self.checkBox1.setChecked(config['rename'])
        self.checkBox2 = QCheckBox("eps", self)
        self.checkBox2.setChecked(config['eps'])
        
        self.checkBox1.setGeometry(250, 10, 90, 30)
        self.checkBox2.setGeometry(330, 10, 90, 30)
        
        btn_close = QPushButton(self, text="Ok")
        btn_close.clicked.connect(self.close_window)
        btn_close.setGeometry(180, 90, 70, 30)
        
    def open_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "C:/Users/admin/Desktop/")
        self.qle.setText(dir_path)
        self.config['path'] = dir_path
        
    def close_window(self):
        new_num_fold = int(self.le_num.text()) * int(self.col_num.text())
        old_num_fold = self.config['num_fold']
        if new_num_fold > old_num_fold:
            for i in range(new_num_fold - old_num_fold):
                self.config['folders'].append('')
        else:
            self.config['folders'] = self.config['folders'][:new_num_fold]
        
        refrash = new_num_fold != old_num_fold
        self.config['num_fold'] = new_num_fold
        self.config['row'] = int(self.le_num.text())
        self.config['col'] = int(self.col_num.text())
        self.config['rename'] = self.checkBox1.isChecked()
        self.config['eps'] = self.checkBox2.isChecked()
        self.signal.emit(int(refrash))
        self.close()
