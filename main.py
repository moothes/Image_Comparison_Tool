import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from math import *
from shutil import *
import numpy as np
import os
from PIL import Image
from settings import *


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Image Viewer')  
        screenRect = QApplication.desktop().screenGeometry()
        self.sh = screenRect.height()
        self.sw = screenRect.width()

        self.config = {'num_fold': 4, 'row': 2, 'col': 2, 'folders': ['',] * 4, 'img_list': [], 'num_img': 0, 'path': '', 'rename': False, 'eps': False, 'img_size': 280}
        
        self.listview = None
        self.lbls = []
        self.open_btn = []
        self.method_name = []
        
        self.initUI()

        
    def initUI(self):
        self.row = self.config['row'] # floor(sqrt(self.config['row']))
        self.col = self.config['col'] # ceil(self.config['num_fold'] /self.row)
        
        self.img_size = self.config['img_size'] # 280
        self.pad_x = 15
        self.pad_y = self.pad_x + 20

        # calculate window size
        win_w = 260 + self.col * (self.img_size + self.pad_x)
        win_h = 80 + self.row * (self.img_size + self.pad_y)
        self.setGeometry((self.sw - win_w) // 2, (self.sh - win_h) // 2, win_w, win_h)
        self.setFixedSize(win_w, win_h)
        
        self.statusBar().showMessage('Ready!!!')
        
        # main menu
        setAct = QAction('Settings', self)
        setAct.setStatusTip('Set number of folders')
        setAct.triggered.connect(lambda: self.child_show(Settings))
        
        #loadAct = QAction('Set folders', self)
        #loadAct.setStatusTip('Select image folders')
        #loadAct.triggered.connect(lambda: self.child_show(LoadWindow))
        
        #self.exsetAct = QAction('Export Settings', self)
        #self.exsetAct.setStatusTip('Export the selected images to target folder')
        #self.exsetAct.triggered.connect(lambda: self.child_show(ExportSetting))
        #self.exsetAct.setEnabled(False)

        self.exportAct = QAction('Export')
        self.exportAct.setShortcut("S")
        self.exportAct.setStatusTip('Export the selected images to target folder')
        self.exportAct.triggered.connect(self.export)
        self.exportAct.setEnabled(False)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        #exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.clear()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(setAct)
        #fileMenu.addAction(loadAct)
        #fileMenu.addAction(self.exsetAct)
        fileMenu.addAction(self.exportAct)
        fileMenu.addAction(exitAct)
        
        
        self.list_lbl = QLabel(self)
        self.list_lbl.setGeometry(40, 50, 180, 20)
        self.list_lbl.setText('Image list:')
        
        if self.listview is None:
            self.listview = QListWidget(self)
            self.listview.clicked.connect(self.checkItem)
        self.listview.setGeometry(40, 70, 180, self.row * (self.img_size + self.pad_y) - self.pad_y)
        #self.layout().addWidget(self.listview)
        
        for lbl, btn, f_name in zip(self.lbls, self.open_btn, self.method_name):
            lbl.deleteLater()
            btn.deleteLater()
            f_name.deleteLater()
            
        self.lbls.clear()
        self.open_btn.clear()
        self.method_name.clear()
        
        for i in range(self.config['num_fold']):
            x = i % self.col
            y = i // self.col
            
            f_name = QLabel(self)
            f_name.setText('Folder {}:'.format(i))
            f_name.setGeometry(x * (self.img_size + self.pad_x) + 250, y * (self.img_size + self.pad_y) + 40, 100, 25)
            
            btn = QPushButton(self, text="Set".format(i))
            btn.tag = i
            btn.clicked.connect(self.open_folder)
            btn.setGeometry(x * (self.img_size + self.pad_x) + 470, y * (self.img_size + self.pad_y) + 40, 60, 25)
            
            lbl = QLabel(self)
            lbl.setStyleSheet("QLabel{background:white;}"
                              "QLabel{color:rgb(0,0,0,120);font-size:25px;font-weight:bold;font-family:宋体;}"
                             )
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setText('Folder {}'.format(i))
            #lbl.setMouseTracking(True)
            lbl.mouseMoveEvent = self.mouseMove
            #lbl.installEventFilter(self.mouseMoveEvent(self))
            #lbl.moved.connect(self.mouseMoveEvent)
            lbl.setGeometry(x * (self.img_size + self.pad_x) + 250, y * (self.img_size + self.pad_y) + 70, self.img_size, self.img_size)
            
            
            self.method_name.append(f_name)
            self.open_btn.append(btn)
            self.lbls.append(lbl)
            #print(len(self.open_btn))
            
            #self.layout().addWidget(f_name)
            self.layout().addWidget(f_name)
            self.layout().addWidget(btn)
            self.layout().addWidget(lbl)
                
        '''
        old_num = len(self.lbls)
        if old_num < self.config['num_fold']:
            for i in range(self.config['num_fold']):
                x = i % self.col
                y = i // self.col
                if i >= old_num:
                    
                    f_name = QLabel(self)
                    f_name.setText('Folder {}:'.format(i))
                    f_name.setGeometry(x * (self.img_size + self.pad_x) + 250, y * (self.img_size + self.pad_y) + 40, 100, 25)
                    
                    btn = QPushButton(self, text="Set".format(i))
                    btn.tag = i
                    btn.clicked.connect(self.open_folder)
                    btn.setGeometry(x * (self.img_size + self.pad_x) + 470, y * (self.img_size + self.pad_y) + 40, 60, 25)
                    
                    lbl = QLabel(self)
                    lbl.setStyleSheet("QLabel{background:white;}"
                                      "QLabel{color:rgb(0,0,0,120);font-size:25px;font-weight:bold;font-family:宋体;}"
                                     )
                    lbl.setAlignment(Qt.AlignCenter)
                    lbl.setText('Folder {}'.format(i))
                    #lbl.setMouseTracking(True)
                    lbl.mouseMoveEvent = self.mouseMove
                    #lbl.installEventFilter(self.mouseMoveEvent(self))
                    #lbl.moved.connect(self.mouseMoveEvent)
                    lbl.setGeometry(x * (self.img_size + self.pad_x) + 250, y * (self.img_size + self.pad_y) + 70, self.img_size, self.img_size)
                    
                    
                    self.method_name.append(f_name)
                    self.open_btn.append(btn)
                    self.lbls.append(lbl)
                    print(len(self.open_btn))
                    
                    #self.layout().addWidget(f_name)
                    self.layout().addWidget(f_name)
                    self.layout().addWidget(btn)
                    self.layout().addWidget(lbl)
                
                else:
                    lbl = self.lbls[i]
                    btn = self.open_btn[i]
                    f_name = self.method_name[i]
                    
                    lbl.setGeometry(x * (self.img_size + self.pad_x) + 250, y * (self.img_size + self.pad_y) + 70, self.img_size, self.img_size)
                    
                    btn.setGeometry(x * (self.img_size + self.pad_x) + 470, y * (self.img_size + self.pad_y) + 40, 60, 25)
                    
                    f_name.setText('Folder {}:'.format(i))
                    f_name.setGeometry(x * (self.img_size + self.pad_x) + 250, y * (self.img_size + self.pad_y) + 40, 60, 25)
        else:
            for i in range(old_num):
                lbl = self.lbls[i]
                btn = self.open_btn[i]
                f_name = self.method_name[i]
                if i < self.config['num_fold']:
                    x = i % self.col
                    y = i // self.col
                    lbl.setGeometry(x * (self.img_size + self.pad_x) + 250, y * (self.img_size + self.pad_y) + 70, self.img_size, self.img_size)
                    btn.setGeometry(x * (self.img_size + self.pad_x) + 470, y * (self.img_size + self.pad_y) + 40, 60, 25)
                    
                    f_name.setText('Folder {}:'.format(i))
                    f_name.setGeometry(x * (self.img_size + self.pad_x) + 250, y * (self.img_size + self.pad_y) + 50, 60, 20)
                else:
                    lbl.deleteLater()
                    btn.deleteLater()
                    f_name.deleteLater()

            self.lbls = self.lbls[:self.config['num_fold']]
            self.method_name = self.method_name[:self.config['num_fold']]
        '''
        
        self.show()
        
    def checkItem(self, index):
        #print(index.row(), index.column(), index.data())
        self.show_img(index.row())

    def child_show(self, window):
        self.sub_window = window(self.config)
        #if window.__name__ == 'LoadWindow':
        #    self.sub_window.signal.connect(self.get_folds)
        if window.__name__ == 'Settings':
            self.sub_window.signal.connect(self.setting)
            
        self.sub_window.show()
        
        
    def setting(self, refrash):
        if refrash:
            self.initUI()
            
    '''
    def get_folds(self):
        if self.config['folders'][0] == '' or not self.config['num_img']:
            return
        
        self.listview.clear()
        self.listview.addItems(self.config['img_list'])
        self.listview.setCurrentRow(0)
        
        self.show_img(0)
        self.statusBar().showMessage('Load image complete!')
        
        self.exportAct.setEnabled(True)
    '''
    
    def open_folder(self):
        idx = self.sender().tag
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "C:/Users/admin/Desktop/debug1/debug")
        if not os.path.exists(dir_path):
            return
        self.method_name[idx].setText(dir_path.split('/')[-1])
        self.config['folders'][idx] = dir_path
        
        img_list = os.listdir(dir_path)
        if not idx:
            self.config['img_list'] = []
            for img_name in img_list:
                suffix = img_name.split('.')[-1]
                if suffix in ['jpg', 'png', 'bmp']:
                    self.config['img_list'].append(img_name)
            self.config['num_img'] = len(self.config['img_list'])
            self.list_lbl.setText('Total {} images: '.format(self.config['num_img']))
            if self.config['path'] == '':
                self.config['path'] = os.path.dirname(self.config['folders'][idx])
            #img_list = self.config['img_list']
            
            self.show_img(0)
            self.listview.clear()
            self.listview.addItems(self.config['img_list'])
            self.listview.setCurrentRow(0)
            self.exportAct.setEnabled(True)
        else:
            sel_idx = self.listview.currentRow()
            self.show_img(sel_idx)
        
        self.statusBar().showMessage('Load image complete!')

    def set_export(self, result):
        self.config.update(result)

    def show_img(self, idx):
        name = self.config['img_list'][idx]
    
        assert len(self.config['folders']) == self.config['num_fold']
        for i, fold in enumerate(self.config['folders']):
            if fold == '':
                continue
            self.method_name[i].setText(fold.split('/')[-1] + ':')
            path = os.path.join(fold, name)
            if not os.path.exists(path):
                self.lbls[i].setText('No Image!')
                continue
            
            scaledPixmap = QPixmap(path).scaled(QSize(self.img_size, self.img_size))
            self.lbls[i].setPixmap(scaledPixmap)

    def keyPressEvent(self, event):
        sel_idx = self.listview.currentRow()
        if self.config['num_img'] < 1:
            return
        
        # 1677723 4-7 左上右下
        key = event.key()
        if key in [16777234, 16777236]:
            sel_idx = np.clip(key - 16777235 + sel_idx, 0, self.config['num_img'] - 1)
            self.show_img(sel_idx)
            self.listview.setCurrentRow(sel_idx)
            
            msg = 'total image: {}, now: {} .'.format(self.config['num_img'], sel_idx)
            self.statusBar().showMessage(msg)

        #if event.key() == 83:
        #    # s
        #    self.export()

    def mouseMove(self, e):
        if self.config['num_img'] < 1:
            return

        gx = e.globalPos().x()
        gy = e.globalPos().y()
        ind_x = (gx - 770) // (self.img_size + self.pad_x)
        ind_y = (gy - 260) // (self.img_size + self.pad_x)
        index = np.clip(self.col * ind_y + ind_x, 0, self.config['num_fold']-1)
        
        x = e.pos().x()
        y = e.pos().y()
        x = np.clip(x, 0, self.img_size - 1)
        y = np.clip(y, 0, self.img_size - 1)

        pix = self.lbls[index].pixmap()
        if pix is None:
            return
        val = pix.toImage().pixel(x, y)
        red, green, blue = qRed(val), qGreen(val), qBlue(val)
        self.statusBar().showMessage('x: {}, y: {}, Value: {}, {}, {}.'.format(x, y, red, green, blue))

        for i in range(self.config['num_fold']):
            pix = self.lbls[i].pixmap()
            if pix is None:
                continue
            im = pix.toImage()
            value = qRgb(255, 255, 0)
            
            im.setPixel(x-1, y-1, value)
            im.setPixel(x-1, y  , value)
            im.setPixel(x-1, y+1, value)
            im.setPixel(x  , y-1, value)
            im.setPixel(x  , y  , value)
            im.setPixel(x  , y+1, value)
            im.setPixel(x+1, y-1, value)
            im.setPixel(x+1, y  , value)
            im.setPixel(x+1, y+1, value)
            
            self.lbls[i].setPixmap(QPixmap.fromImage(im))
    
    def export(self):
        main_path = os.path.join(self.config['path'], 'comparison')
        if not os.path.exists(main_path):
            os.mkdir(main_path)

        img_name = self.listview.selectedItems()[0].text()
        for i, fold in enumerate(self.config['folders']):
            if fold != '':
                method = fold.split('/')[-2]
                method_path = os.path.join(main_path, method)
                if not os.path.exists(method_path):
                    os.mkdir(method_path)
                
                src_path = os.path.join(fold, img_name)
                
                num_img = len(os.listdir(method_path))
                img_tag, suffix = img_name.split('.')
                img_tag = str(num_img) if self.config['rename'] else img_tag
                suffix = 'eps' if self.config['eps'] else suffix
                new_name = '{}.{}'.format(img_tag, suffix)
                tar_path = os.path.join(method_path, new_name)
                
                if self.config['eps']:
                    im = Image.open(src_path)
                    im.save(tar_path, 'EPS')

                else:
                    copyfile(src_path, tar_path)
        
        msg = 'Image {} has been saved in {}.'.format(img_name, main_path)
        self.statusBar().showMessage(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('WindowsXP')
    ex1 = Example()
    sys.exit(app.exec_())
