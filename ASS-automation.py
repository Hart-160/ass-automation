from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from generate_tmp import *
import os
from ass_writer import write_ass
class Entrance:

    def __init__(self):
        self.ui = QUiLoader().load('GUI Pages\\entry.ui')

        self.ui.generate_template.clicked.connect(self.GenerateTMP)
        self.ui.run_ass.clicked.connect(self.RunASS)

    def GenerateTMP(self):
        self.subwin = Generate_TMP()
        self.subwin.ui.show()
        self.ui.close()

    def RunASS(self):
        self.subwin = ASS_Automation()
        self.subwin.ui.show()
        self.ui.close()

class Generate_TMP:

    def __init__(self):
        self.ui = QUiLoader().load('GUI Pages\\template.ui')
        #buttons below
        self.ui.choose_sce.clicked.connect(self.select_sce)
        self.ui.generate.clicked.connect(self.generate)
        self.ui.generate_text.clicked.connect(self.generateText)
        self.ui.back_main.clicked.connect(self.back)

    def select_sce(self):
        scePath, _  = QFileDialog.getOpenFileName(
            self.ui,             
            "选择SCE文件",
            r"c:\\",
            "视频类型 (*.sce)"
        )
        self.ui.sce_route.setText(scePath)

    def generate(self):
        sce = self.ui.sce_route.text()
        if sce == '':
            QMessageBox.critical(self.ui, '发生错误', '必须填入SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
        else:
            TemplateUtils.sce_to_template(sce)
            rout, name = os.path.split(sce)
            sole_name= os.path.splitext(name)[0]
            new_name = '\\[TEMPLATE] ' + sole_name + '.txt'
            os.rename(rout + '\\' + sole_name + '.txt', rout + new_name)
            QMessageBox.information(self.ui, '任务完成', '模板已成功生成！', QMessageBox.Ok, QMessageBox.Ok)

    def generateText(self):
        sce = self.ui.sce_route.text()
        if sce == '':
            QMessageBox.critical(self.ui, '发生错误', '必须填入SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
        else:
            TemplateUtils.clean_sce(sce)
            rout, name = os.path.split(sce)
            sole_name= os.path.splitext(name)[0]
            new_name = '\\[TEXT] ' + sole_name + '.txt'
            os.rename(rout + '\\' + sole_name + '.txt', rout + new_name)
            QMessageBox.information(self.ui, '任务完成', '文本已成功提取！', QMessageBox.Ok, QMessageBox.Ok)

    def back(self):
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

        self.ui.video_route.setPlaceholderText('视频文件为必填项，请确保与其余两项对应')
        self.ui.sce_route.setPlaceholderText('SCE文件为必填项，请确保与其余两项对应')
        self.ui.template_route.setPlaceholderText('模板为可选项，请确保与其余两项对应')

        #button below
        self.ui.generate.clicked.connect(self.run)

    def select_video(self):
        videoPath, _  = QFileDialog.getOpenFileName(
            self.ui,             
            "选择视频文件",
            r"c:\\",
            "视频类型 (*.mp4 *.avi *.flv)"
        )
        self.ui.video_route.setText(videoPath)

    def select_sce(self):
        scePath, _  = QFileDialog.getOpenFileName(
            self.ui,             
            "选择SCE文件",
            r"c:\\",
            "文件类型 (*.sce)"
        )
        self.ui.sce_route.setText(scePath)
    
    def select_template(self):
        tempPath, _  = QFileDialog.getOpenFileName(
            self.ui,             
            "选择TXT模板",
            r"c:\\",
            "文件类型 (*.txt)"
        )
        self.ui.template_route.setText(tempPath)

    def back(self):
        self.subwin = Entrance()
        self.subwin.ui.show()
        self.ui.close()

    def run(self):
        video = self.ui.video_route.text()
        sce = self.ui.sce_route.text()
        template = self.ui.template_route.text()
        if len(template) == 0:
            template = None

        if video=='' or sce=='':
            QMessageBox.critical(self.ui, '发生错误', '必须填入视频和SCE文件！', QMessageBox.Ok, QMessageBox.Ok)
        else:
            success = write_ass(sce, video, template)
            if success:
                QMessageBox.information(self.ui, '任务完成', '字幕已经生成！', QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.critical(self.ui, '发生错误', '请检查终端报错后重新运行！', QMessageBox.Ok, QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication([])
    stats = Entrance()
    stats.ui.show()
    app.exec_()