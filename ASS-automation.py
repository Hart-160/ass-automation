import ctypes
import json
import logging
import os
import sys
import threading

#from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                               QMessageBox)

from ass_writer import *
from generate_tmp import *
from image_sections import *
from ui_entry import Ui_MainWindow
from ui_run_ass import Ui_ASS_automation
from ui_template import Ui_GenerateTemplate

'''
这个部分负责GUI，是实质上的主程序
'''

class Configs:
    #记录配置用
    PREFERRED_SCE_PATH = 'PreferredSCEPath'
    PREFERRED_ASS_PATH = 'PreferredASSPath'
    
    def config_creator():
        data = {
            Configs.PREFERRED_SCE_PATH:'',
            Configs.PREFERRED_ASS_PATH:''
        }
        with open('temp\\config.json', 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def config_reader(parameter):
        with open('temp\\config.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
        return data[parameter]

    def config_editor(parameter, input):
        with open('temp\\config.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
        data[parameter] = input
        with open('temp\\config.json', 'w+', encoding='utf-8') as f:
             json.dump(data, f, indent=4)

class Entrance(QMainWindow, Ui_MainWindow):

    '''def __init__(self):
        self = QUiLoader().load('GUI Pages\\entry.ui')'''
    def __init__(self) -> None:
        super(Entrance, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon("dj_icon.ico"))
        self.generate_template.clicked.connect(self.GenerateTMP)
        self.run_ass.clicked.connect(self.RunASS)

    def GenerateTMP(self):
        #跳转至文本&模板生成
        self.subwin = Generate_TMP()
        self.subwin.show()
        self.close()
        logging.info('[GenerateTMP] Start')

    def RunASS(self):
        #跳转至轴机运行
        self.subwin = ASS_Automation()
        self.subwin.show()
        self.close()
        logging.info('[ASSautomation] Start')

def rename(path_name,new_name):
    #应对出现重复文件的情况
    try:
        os.rename(path_name,new_name)
    except Exception as e:
        if e.args[0] ==17: #重命名
            fname, fename = os.path.splitext(new_name)
            rename(path_name, fname+"-1"+fename)

class Generate_TMP(QMainWindow, Ui_GenerateTemplate):

    '''def __init__(self):
        self = QUiLoader().load('GUI Pages\\template.ui')'''
    def __init__(self) -> None:
        super(Generate_TMP, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("dj_icon.ico"))
        #buttons below
        self.choose_sce.clicked.connect(self.select_sce)
        self.generate.clicked.connect(self.generateTemplate)
        self.generate_text.clicked.connect(self.generateText)
        self.back_main.clicked.connect(self.back)

    def select_sce(self):
        #选择sce文件
        config_sce_path = Configs.config_reader(Configs.PREFERRED_SCE_PATH)
        if config_sce_path == '':
            config_sce_path = r"C:\\"
        scePath, _  = QFileDialog.getOpenFileName(
            self,             
            "选择SCE文件",
            config_sce_path,
            "文件类型 (*.sce)"
        )
        if scePath == '':
            return
        self.sce_route.setText(scePath)
        Configs.config_editor(Configs.PREFERRED_SCE_PATH, os.path.split(scePath)[0])
        logging.info('[GenerateTMP] SCE file selected: {}'.format(scePath))

    def generateTemplate(self):
        #生成翻译模板
        sce = self.sce_route.text()
        if sce == '':
            QMessageBox.critical(self, '发生错误', '必须填入SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
            logging.warning('[GenerateTMP] SCE file not selected')
        else:
            TemplateUtils.sce_to_template(sce)
            rout, name = os.path.split(sce)
            sole_name= os.path.splitext(name)[0]
            new_name = '\\[TEMPLATE] ' + sole_name + '.txt'
            rename(rout + '\\' + sole_name + '.txt', rout + new_name)
            QMessageBox.information(self, '任务完成', '模板已成功生成！', QMessageBox.Ok, QMessageBox.Ok)
            logging.info('[GenerateTMP] Template generated')

    def generateText(self):
        #生成txt文本
        sce = self.sce_route.text()
        if sce == '':
            QMessageBox.critical(self, '发生错误', '必须填入SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
            logging.warning('[GenerateTMP] SCE file not selected')
        else:
            TemplateUtils.clean_sce(sce)
            rout, name = os.path.split(sce)
            sole_name= os.path.splitext(name)[0]
            new_name = '\\[TEXT] ' + sole_name + '.txt'
            rename(rout + '\\' + sole_name + '.txt', rout + new_name)
            QMessageBox.information(self, '任务完成', '文本已成功提取！', QMessageBox.Ok, QMessageBox.Ok)
            logging.info('[GenerateTMP] Text generated')

    def back(self):
        #返回entry界面
        self.subwin = Entrance()
        self.subwin.show()
        self.close()
        logging.info('[GenerateTMP] Back to entrance')

class ASS_Automation(QMainWindow, Ui_ASS_automation):

    '''def __init__(self):
        self = QUiLoader().load('GUI Pages\\run_ass.ui')'''
    def __init__(self) -> None:
        super(ASS_Automation, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("dj_icon.ico"))

        #buttons below
        self.choose_video.clicked.connect(self.select_video)
        self.choose_sce.clicked.connect(self.select_sce)
        self.choose_template.clicked.connect(self.select_template)
        self.back_main.clicked.connect(self.back)
        self.generate.clicked.connect(self.start_ass)

        #placeholders below
        self.video_route.setPlaceholderText('视频文件为必填项，且路径不能包含中文')
        self.sce_route.setPlaceholderText('SCE文件为必填项，请确保与视频文件对应')
        self.template_route.setPlaceholderText('模板为可选项，请确保与其余两项对应') 

        #connection below
        pb.setmax.connect(self.set_max)
        pb.update_bar.connect(self.set_bar)
        ab.text_output.connect(self.outputWritten)
        ab.send_status.connect(self.change_availability)

    def select_video(self):
        #选择视频文件
        config_ass_path = Configs.config_reader(Configs.PREFERRED_ASS_PATH)
        if config_ass_path == '':
            config_ass_path = r"C:\\"
        videoPath, _  = QFileDialog.getOpenFileName(
            self,             
            "选择视频文件",
            config_ass_path,
            "视频类型 (*.mp4 *.avi *.flv)"
        )
        if videoPath == '':
            return
        self.video_route.setText(videoPath)
        Configs.config_editor(Configs.PREFERRED_ASS_PATH, os.path.split(videoPath)[0])
        logging.info('[ASSautomation] Video file selected: {}'.format(videoPath))

    def select_sce(self):
        #选择sce文件
        config_ass_path = Configs.config_reader(Configs.PREFERRED_ASS_PATH)
        if config_ass_path == '':
            config_ass_path = r"C:\\"
        scePath, _  = QFileDialog.getOpenFileName(
            self,             
            "选择SCE文件",
            config_ass_path,
            "文件类型 (*.sce)"
        )
        if scePath == '':
            return
        self.sce_route.setText(scePath)
        Configs.config_editor(Configs.PREFERRED_ASS_PATH, os.path.split(scePath)[0])
        logging.info('[ASSautomation] SCE file selected: {}'.format(scePath))
    
    def select_template(self):
        #选择翻译模板文件
        config_ass_path = Configs.config_reader(Configs.PREFERRED_ASS_PATH)
        if config_ass_path == '':
            config_ass_path = r"C:\\"
        tempPath, _  = QFileDialog.getOpenFileName(
            self,             
            "选择TXT模板",
            config_ass_path,
            "文件类型 (*.txt)"
        )
        if tempPath == '':
            return
        self.template_route.setText(tempPath)
        Configs.config_editor(Configs.PREFERRED_ASS_PATH, os.path.split(tempPath)[0])
        logging.info('[ASSautomation] Template file selected: {}'.format(tempPath))

    def back(self):
        #返回entry界面
        self.subwin = Entrance()
        self.subwin.show()
        self.close()
        logging.info('[ASSautomation] Back to entrance')

    def outputWritten(self, text):
        #将文字打印到textBrowser上
        self.output_window.append(text)

    def set_max(self, mvalue):
        #设置进度条最大值
        self.progressBar.setMaximum(mvalue)

    def set_bar(self, value):
        #设置进度条的值
        self.progressBar.setValue(value)

    def change_availability(self, yes:bool):
        #传入参数时告知主线程GUI取消两个按钮的disable状态
        if yes:
            QMessageBox.information(self, 'D4DJ ASS AUTOMATION', '字幕文件已生成！<br> 文件位于视频路径', QMessageBox.Ok, QMessageBox.Ok)
            self.back_main.setDisabled(False)
            self.generate.setDisabled(False)
            self.choose_video.setDisabled(False)
            self.choose_sce.setDisabled(False)
            self.choose_template.setDisabled(False)
        else:
            QMessageBox.critical(self, 'D4DJ ASS AUTOMATION', '请检查报错后重新运行！', QMessageBox.Ok, QMessageBox.Ok)
            self.back_main.setDisabled(False)
            self.generate.setDisabled(False)
            self.choose_video.setDisabled(False)
            self.choose_sce.setDisabled(False)
            self.choose_template.setDisabled(False)

    def start_ass(self):
        #运行轴机
        video = self.video_route.text()
        sce = self.sce_route.text()
        template = self.template_route.text()
        if len(template) == 0:
            template = None

        if video=='' or sce=='':
            QMessageBox.critical(self, 'D4DJ ASS AUTOMATION', '必须填入视频和SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
            logging.warning('[ASSautomation] SCE or Video not selected')
        else:
            self.output_window.clear()
            self.back_main.setDisabled(True)
            self.generate.setDisabled(True)
            self.choose_video.setDisabled(True)
            self.choose_sce.setDisabled(True)
            self.choose_template.setDisabled(True)

            use_temp = False
            if os.path.exists('temp\\' + os.path.split(video)[1] + '.data'):
                reply = QMessageBox.question(self, 'D4DJ ASS AUTOMATION', '是否使用现存视频分析数据？')
                if reply == QMessageBox.StandardButton.Yes:
                    use_temp = True
                    logging.info('[ASSautomation] Choose to use previous data')
            def run(): 
                #必须是另起一个函数包装好自己需要的函数，然后开启thread
                #函数内不能包含跟self相关的内容，会出现跨线程的bug
                AssBuilder.write_ass(sce, video, template, use_temp)
            thread1 = threading.Thread(target=run)
            thread1.start()

if __name__ == '__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    
    if not os.path.exists('temp'):
        os.makedirs('temp')
    logging.basicConfig(filename='temp\\runtime-log.log', filemode='w', level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)

    if not os.path.exists('temp\\config.json'):
        Configs.config_creator()

    def handle_exception(exc_type, exc_value, exc_traceback):
        #GUI部分的log输出，sys的excepthook有三个参数
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)) # 重点

    def thread_exception(exc_type):
        #轴机主体的log输出（因为是单独开的线程）threading的excepthook只有一个参数
        logger.error("Uncaught exception", exc_info=(exc_type))

    sys.excepthook = handle_exception
    threading.excepthook = thread_exception

    if sys.platform.startswith('win'):
        ctypes.windll.user32.SetProcessDPIAware()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication([])
    stats = Entrance()
    stats.show()
    app.exec_()
