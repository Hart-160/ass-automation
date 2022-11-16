import os
from threading import Thread

from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *

from generate_tmp import *
from ass_writer import *
from image_sections import *

'''
这个部分负责GUI，是实质上的主程序
'''

class Entrance:

    def __init__(self):
        self.ui = QUiLoader().load('GUI Pages\\entry.ui')

        self.ui.generate_template.clicked.connect(self.GenerateTMP)
        self.ui.run_ass.clicked.connect(self.RunASS)

    def GenerateTMP(self):
        #跳转至文本&模板生成
        self.subwin = Generate_TMP()
        self.subwin.ui.show()
        self.ui.close()

    def RunASS(self):
        #跳转至轴机运行
        self.subwin = ASS_Automation()
        self.subwin.ui.show()
        self.ui.close()

def rename(path_name,new_name):
    #应对出现重复文件的情况
    try:
        os.rename(path_name,new_name)
    except Exception as e:
        if e.args[0] ==17: #重命名
            fname, fename = os.path.splitext(new_name)
            rename(path_name, fname+"-1"+fename)

class Generate_TMP:

    def __init__(self):
        self.ui = QUiLoader().load('GUI Pages\\template.ui')
        #buttons below
        self.ui.choose_sce.clicked.connect(self.select_sce)
        self.ui.generate.clicked.connect(self.generate)
        self.ui.generate_text.clicked.connect(self.generateText)
        self.ui.back_main.clicked.connect(self.back)

    def select_sce(self):
        #选择sce文件
        scePath, _  = QFileDialog.getOpenFileName(
            self.ui,             
            "选择SCE文件",
            r"c:\\",
            "视频类型 (*.sce)"
        )
        self.ui.sce_route.setText(scePath)

    def generate(self):
        #生成翻译模板
        sce = self.ui.sce_route.text()
        if sce == '':
            QMessageBox.critical(self.ui, '发生错误', '必须填入SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
        else:
            TemplateUtils.sce_to_template(sce)
            rout, name = os.path.split(sce)
            sole_name= os.path.splitext(name)[0]
            new_name = '\\[TEMPLATE] ' + sole_name + '.txt'
            rename(rout + '\\' + sole_name + '.txt', rout + new_name)
            QMessageBox.information(self.ui, '任务完成', '模板已成功生成！', QMessageBox.Ok, QMessageBox.Ok)

    def generateText(self):
        #生成txt文本
        sce = self.ui.sce_route.text()
        if sce == '':
            QMessageBox.critical(self.ui, '发生错误', '必须填入SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
        else:
            TemplateUtils.clean_sce(sce)
            rout, name = os.path.split(sce)
            sole_name= os.path.splitext(name)[0]
            new_name = '\\[TEXT] ' + sole_name + '.txt'
            rename(rout + '\\' + sole_name + '.txt', rout + new_name)
            QMessageBox.information(self.ui, '任务完成', '文本已成功提取！', QMessageBox.Ok, QMessageBox.Ok)

    def back(self):
        #返回entry界面
        self.subwin = Entrance()
        self.subwin.ui.show()
        self.ui.close()

class ASS_Automation:

    def __init__(self):
        self.ui = QUiLoader().load('GUI Pages\\run_ass.ui')

        #buttons below
        self.ui.choose_video.clicked.connect(self.select_video)
        self.ui.choose_sce.clicked.connect(self.select_sce)
        self.ui.choose_template.clicked.connect(self.select_template)
        self.ui.back_main.clicked.connect(self.back)
        self.ui.generate.clicked.connect(self.start_ass)

        #placeholders below
        self.ui.video_route.setPlaceholderText('视频文件为必填项，且路径不能包含中文')
        self.ui.sce_route.setPlaceholderText('SCE文件为必填项，请确保与视频文件对应')
        self.ui.template_route.setPlaceholderText('模板为可选项，请确保与其余两项对应') 

        #connection below
        pb.setmax.connect(self.set_max)
        pb.update_bar.connect(self.set_bar)
        ab.text_output.connect(self.outputWritten)
        ab.send_status.connect(self.change_availability)

    def select_video(self):
        #选择视频文件
        videoPath, _  = QFileDialog.getOpenFileName(
            self.ui,             
            "选择视频文件",
            r"c:\\",
            "视频类型 (*.mp4 *.avi *.flv)"
        )
        self.ui.video_route.setText(videoPath)

    def select_sce(self):
        #选择sce文件
        scePath, _  = QFileDialog.getOpenFileName(
            self.ui,             
            "选择SCE文件",
            r"c:\\",
            "文件类型 (*.sce)"
        )
        self.ui.sce_route.setText(scePath)
    
    def select_template(self):
        #选择翻译模板文件
        tempPath, _  = QFileDialog.getOpenFileName(
            self.ui,             
            "选择TXT模板",
            r"c:\\",
            "文件类型 (*.txt)"
        )
        self.ui.template_route.setText(tempPath)

    def back(self):
        #返回entry界面
        self.subwin = Entrance()
        self.subwin.ui.show()
        self.ui.close()

    def outputWritten(self, text):
        #将文字打印到textBrowser上
        self.ui.output_window.append(text)

    def set_max(self, mvalue):
        #设置进度条最大值
        self.ui.progressBar.setMaximum(mvalue)

    def set_bar(self, value):
        #设置进度条的值
        self.ui.progressBar.setValue(value)

    def change_availability(self, yes:bool):
        #传入参数时告知主线程GUI取消两个按钮的disable状态
        if yes:
            QMessageBox.information(self.ui, 'D4DJ ASS AUTOMATION', '字幕文件已生成！<br> 文件位于视频路径', QMessageBox.Ok, QMessageBox.Ok)
            self.ui.back_main.setDisabled(False)
            self.ui.generate.setDisabled(False)
            self.ui.choose_video.setDisabled(False)
            self.ui.choose_sce.setDisabled(False)
            self.ui.choose_template.setDisabled(False)
        else:
            QMessageBox.critical(self.ui, 'D4DJ ASS AUTOMATION', '请检查报错后重新运行！', QMessageBox.Ok, QMessageBox.Ok)
            self.ui.back_main.setDisabled(False)
            self.ui.generate.setDisabled(False)
            self.ui.choose_video.setDisabled(False)
            self.ui.choose_sce.setDisabled(False)
            self.ui.choose_template.setDisabled(False)

    def start_ass(self):
        #运行轴机
        video = self.ui.video_route.text()
        sce = self.ui.sce_route.text()
        template = self.ui.template_route.text()
        if len(template) == 0:
            template = None

        if video=='' or sce=='':
            QMessageBox.critical(self.ui, 'D4DJ ASS AUTOMATION', '必须填入视频和SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.ui.output_window.clear()
            self.ui.back_main.setDisabled(True)
            self.ui.generate.setDisabled(True)
            self.ui.choose_video.setDisabled(True)
            self.ui.choose_sce.setDisabled(True)
            self.ui.choose_template.setDisabled(True)

            use_temp = False
            if os.path.exists('temp\\' + os.path.split(video)[1] + '.data'):
                reply = QMessageBox.question(self.ui, 'D4DJ ASS AUTOMATION', '是否使用现存视频分析数据？')
                if reply == QMessageBox.StandardButton.Yes:
                    use_temp = True
            def run(): 
                #必须是另起一个函数包装好自己需要的函数，然后开启thread
                #函数内不能包含跟self.ui相关的内容，会出现跨线程的bug
                AssBuilder.write_ass(sce, video, template, use_temp)
            thread1 = Thread(target=run)
            thread1.start()

if __name__ == '__main__':
    app = QApplication([])
    stats = Entrance()
    stats.ui.show()
    app.exec_()