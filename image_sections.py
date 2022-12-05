import numpy as np
import cv2
from PySide2.QtCore import Signal,QObject
import settings_handler as sh

'''
这个部分负责分析视频
'''

class ImageData(object):
    '''
    对一帧进行对话框和文字判定
    '''
    def __init__(self, image, lower_range, upper_range, white_threshold) -> None:
        self.image = image
        self.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.lower = lower_range
        self.upper = upper_range
        self.white_threshold = white_threshold

    def __read_pixel(frame, x1, x2, y1, y2):
        #判断四个点是否为白色，如果四个都是，返回true，否则返回false
        yes = 0
        is_dialogue = False
        if frame[y1, x1] == 255:
            yes += 1
        if frame[y2, x1] == 255:
            yes += 1
        if frame[y1, x2] == 255:
            yes += 1
        if frame[y2, x2] == 255:
            yes += 1
        if yes == 4:
            is_dialogue = True
        return is_dialogue
    
    def __is_valid_color(self,x1,x2,y1,y2) -> bool:
        #判断对话框的颜色部分（常规状况下为紫色）
        dialogue = bool(False)

        im = self.image
        fhsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(fhsv, np.array(self.lower), np.array(self.upper))
        im = cv2.bitwise_and(im, im, mask=mask)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, im = cv2.threshold(im, 80, 255, cv2.THRESH_BINARY)
        read_result = ImageData.__read_pixel(im, x1, x2, y1, y2)
        if read_result:
            dialogue = bool(True)
        return dialogue

    def is_word(self,x1,x2,y1,y2) -> bool:
        #判断文字
        self.word = bool(False)
        img = self.gray[y1:y2, x1:x2]
        ret, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY_INV)
        if np.count_nonzero(img) >= 50:
            self.word = bool(True)
        return self.word

    def __is_valid_white(self, x1, x2, y1, y2):
        #判断对话框外圈的白色部分
        white = bool(False)
        x1mod = x1 - 4
        x2mod = x2 + 4
        ret, gray = cv2.threshold(self.gray, int(self.white_threshold), 255, cv2.THRESH_BINARY)
        read_result = ImageData.__read_pixel(gray, x1mod, x2mod, y1, y2)
        if read_result:
            white = bool(True)
        return white

    def is_dialogue(self, x1, x2, y1, y2):
        #结合颜色判定&白色判定输出对话框判定结果
        self.dialogue = bool(False)
        self.dialogue = ImageData.__is_valid_color(self, x1, x2, y1, y2) and ImageData.__is_valid_white(self, x1, x2, y1, y2)
        return self.dialogue

class ImageSections(QObject):
    update_bar = Signal(int) #向GUI发送进度，更新进度条
    setmax = Signal(int)  #向GUI发送进度条最大值，并设置

    def __Merge(dict1, dict2): 
        res = {**dict1, **dict2} 
        return res 

    def image_section_generator(vid, width, height):
        '''
        输入视频路径，返回一个包含各节点的列表
        '''
        cap = cv2.VideoCapture(vid)
        total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        pb.setmax.emit(total_frame)

        image_sections = []
        #data_li = []
        word_count = 1

        #border
        x1,y1,x2,y2 = sh.Reference.box_splitter(sh.Reference.reference_reader(sh.Reference.TEXT_BORDER_MX, width, height))

        #dialogue
        x_1,y_1,x_2,y_2 = sh.Reference.box_splitter(sh.Reference.reference_reader(sh.Reference.TEXT_WORD_MX, width, height))
        
        #读取设置传入ImageData构造器
        lower_r = sh.Settings.hsv_range_splitter(sh.Settings.settings_reader(sh.Settings.DEFAULT_LOWER_RANGE))
        upper_r = sh.Settings.hsv_range_splitter(sh.Settings.settings_reader(sh.Settings.DEFAULT_UPPER_RANGE))
        white_gate = sh.Settings.settings_reader(sh.Settings.DEFAULT_WHITE_THRESHOLD)

        success, p_frame = cap.read()
        f = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        pb.update_bar.emit(f)
        prev_frame = ImageData(p_frame, lower_r, upper_r, white_gate)
        prev_frame.dialogue = prev_frame.is_dialogue(x1, x2, y1, y2)
        prev_frame.word = prev_frame.is_word(x_1, x_2, y_1, y_2)

        start = ''
        end = ''
        spec = {}

        while success:
            try:
                success, c_frame = cap.read()
                ms = cap.get(cv2.CAP_PROP_POS_MSEC)
                f = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                pb.update_bar.emit(f)
                curr_frame = ImageData(c_frame, lower_r, upper_r, white_gate)
                curr_frame.dialogue = curr_frame.is_dialogue(x1, x2, y1, y2)
                curr_frame.word = curr_frame.is_word(x_1, x_2, y_1, y_2)
                #data_li.append({'Frame':f, 'IsDialogue':curr_frame.dialogue, 'IsWord':curr_frame.word})

                if curr_frame.dialogue == prev_frame.dialogue:
                    if curr_frame.dialogue:
                        if curr_frame.word == False and prev_frame.word != curr_frame.word:
                            #判断文本更新
                            end = ms
                            image_sections.append(ImageSections.__Merge({'Index':word_count,'Start':start, 'End':end}, spec))
                            start = ms
                            spec = {}
                            word_count += 1
                else:
                    if curr_frame.dialogue:
                        #前一帧不是对话框，当前帧是对话框，判断对话框出现
                        start = ms
                        spec = {'OpenWindow':True}
                    else:
                        #前一帧是对话框，当前帧不是对话框，判断对话框消失
                        end = ms
                        spec = ImageSections.__Merge(spec, {'CloseWindow':True})
                        image_sections.append(ImageSections.__Merge({'Index':word_count,'Start':start, 'End':end}, spec))
                        word_count += 1
                prev_frame = curr_frame
            except cv2.error:
                break
        cap.release()

        return image_sections#, data_li

    def jitter_cleaner(img_sections:list):
        '''
        输入image sections，返回清理后的image sections和警告列表

        清除时间过短的视频分段，合并连续的过段分段并从主列表清除，另添加至警告列表
        '''

        #清除时长小于1秒的section
        remove_li = []
        for im in img_sections:
            if im['End'] - im['Start'] < 1000.0:
                remove_li.append(im)

        #合并多个连续的小于一秒的section
        tmp = []
        remove_subli = []
        for r in remove_li:
            img_sections.remove(r)
            if len(remove_subli) == 0 or remove_subli[-1]['Index'] + 1 == r['Index']:
                remove_subli.append(r)
            else:
                if len(remove_subli) >= 2:
                    tmp.append(remove_subli)
                remove_subli = [r]
        if len(remove_subli) >= 2:
            tmp.append(remove_subli)
            remove_subli = []

        #将合并的连续短section整合，另外添加至警告列表内
        alert = []
        count = 0
        for t in tmp:
            start = t[0]['Start']
            end = t[-1]['End']
            alert.append({'Index':count, 'Start':start, 'End':end, 'Jitter':True})

        for i in range(len(img_sections)):
            img = img_sections[i]
            img['Index'] = i+1

        return img_sections, alert

pb = ImageSections() #为GUI信号输出创建的实例

if __name__ == '__main__':
    pass