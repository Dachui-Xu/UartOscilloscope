import sys
import serial
import serial.tools.list_ports

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer
from Ui_tiny import Ui_MainWindow

import threading

APP_NAME = "Electrochemistry V1.0.0"


class Pyqt5_Serial(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Pyqt5_Serial, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.ser = serial.Serial()
        self.uart_refresh()
        self.init()

        #测试数据
        self.i = 0
        self.x = []  # x轴的值
        self.y = []  # y轴的值


        #串口获得的数据
       # self.temp = " "
        self.xValue = float()
        self.yValue = float()
        #self.XY = []


        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.rx_lcdNumber.setDigitCount(10)
        self.rx_lcdNumber.display(self.data_num_received)
        self.data_num_sended = 0
        self.tx_lcdNumber.setDigitCount(10)
        self.tx_lcdNumber.display(self.data_num_sended)
        #线程创建有问题
        #self.th = threading.Thread(target=self.ComRecvDeal)  # 创建串口接收线程







    def drawings(self):

        # 通过控件名称 drawing，找到Qt designer设计的 控件
        self.drawing.setBackground('w')
        # 设置上下左右的label
        self.drawing.setLabel("left","电流")
        self.drawing.setLabel("bottom","电压")
        self.drawing.plot(self.x, self.y,pen=(255,0,0))
        #self.curve.setData(self.x, self.y)




    def init(self):
        # 关联串口刷新按钮
        self.pushButton_refresh.clicked.connect(self.uart_refresh)
        # 关联打开串口按钮
        self.pushButton_open.clicked.connect(self.uart_open)
        # 关联发送数据按钮
        self.pushButton_send.clicked.connect(self.send_data)
        # 定时器接收数据
        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)

        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.drawings)
        self.timer1.start(10)




        # 关联发送计数
        self.pushButton_clear_tx.clicked.connect(self.clear_send_num)
        # 关联接收计数
        self.pushButton_clear_rx.clicked.connect(self.clear_receive_num)

    def uart_refresh(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.comboBox_uart.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[1]] = "%s" % port[0]
            self.comboBox_uart.addItem(port[1])
        if len(self.Com_Dict) == 0:
            self.comboBox_uart.setCurrentText("")
            self.pushButton_open.setEnabled(False)
        else:
            self.pushButton_open.setEnabled(True)

    def uart_open(self):

        if self.pushButton_open.text() == '打开串口':
            self.ser.port = self.Com_Dict[self.comboBox_uart.currentText()]
            self.ser.baudrate = int(self.comboBox_baud.currentText())
            self.ser.bytesize = int(self.comboBox_data.currentText())
            self.ser.stopbits = int(self.comboBox_stop.currentText())
            self.ser.parity = self.comboBox_check.currentText()

            try:
                self.ser.open()

            except:
                QMessageBox.warning(self, "错误", "无法打开此串口！")
                return

            if self.ser.isOpen():
                self.pushButton_open.setText('关闭串口')

                # 打开串口接收定时器，周期为10ms
                self.timer.start(10)
        else:
            self.timer.stop()
            try:
                self.ser.close()
            except:
                pass

            if self.ser.isOpen() == False:
                self.pushButton_open.setText('打开串口')

    def send_data(self):
        if self.ser.isOpen():
            send_data = self.tx_plainTextEdit.toPlainText()
            send_data = send_data.encode('UTF-8')
            send_count = self.ser.write(send_data)
            self.data_num_sended += send_count
            self.tx_lcdNumber.display(self.data_num_sended)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                self.timer.stop()
                self.ser.close()
                self.pushButton_open.setText('打开串口')
                return
            if num > 0:
                line = self.ser.readline().decode()  # line是bytes格式，使用decode()转成字符串
                print(line)
                self.AddDataToDict(line)  # 把收到的数据添加到字典中
                self.rx_textBrowser.insertPlainText(line)

                # 统计接收字符的数量
                self.data_num_received += num
                self.rx_lcdNumber.display(self.data_num_received)

                # 获取到text光标
                textCursor = self.rx_textBrowser.textCursor()
                # 滚动到底部
                textCursor.movePosition(textCursor.End)
                # 设置光标到text中去
                self.rx_textBrowser.setTextCursor(textCursor)

    def clear_send_num(self):
        self.data_num_sended = 0
        self.tx_lcdNumber.display(self.data_num_sended)
        self.tx_plainTextEdit.clear()

    def clear_receive_num(self):
        self.data_num_received = 0
        self.rx_lcdNumber.display(self.data_num_received)
        self.rx_textBrowser.clear()

    def ComRecvDeal(self):


         if self.ser.isOpen():
            while(True):
                line = self.ser.readline().decode()  # line是bytes格式，使用decode()转成字符串

                self.AddDataToDict(line)  # 把收到的数据添加到字典中


    # 将串口收到的数据添加到字典
    # 数据格式 ”float1,float2\n"
    def AddDataToDict(self,line):
        global Xval, Yval


        line = line.split("\r\n")  # 目的是去除最后的\n换行，别的方式还没用明白


        #color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']  # 颜色表，这些应该够了，最多8条线，在添加颜色可以用(r,g,b)表示
        for a in line:  # 遍历获取单个变量 如“a,1;b,2;c,3”中的"a,1"
            s = a.split(',')  # 提取名称和数据部分

            if (len(s) != 2):  # 不等于2字符串可能错了，正确的只有名称和数据两个字符串
                return
            Xval_str = s[0]
            Yval_str = s[1]


            if (len(Xval_str) > 0 and len(Yval_str) > 0 ):  # 再判断下是否匹配到了数字
                Xval = float(Xval_str)  # 转成浮点型数字
                Yval = float(Yval_str)
                self.x.append(Xval)
                self.y.append(Yval)
            else:  # 接收错误
                print("error:" + a)
                return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    tiny_uart = Pyqt5_Serial()

    tiny_uart.show()
    sys.exit(app.exec_())
