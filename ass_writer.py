from dialogue_sections import DialogueSections
from image_sections import ImageSections
import settings_handler as sh
import os
import cv2
import shutil

'''
这个部分负责以视频分析列表和sce分析列表为基础写入字幕文件
'''

class ASS_Line(object):
    def __init__(self, start:str, end:str, name:str = None, text:str = None) -> None:
        self.layer = 0
        self.start = start
        self.end = end
        self.style = ''
        self.name = name
        self.margin_set = '0,0,0'
        self.effect = None
        self.text = text

    def build_dialogue(self):
        li = []
        s = ','
        for name, value in vars(self).items():
            if value == None:
                value = ''
            li.append(str(value))
        
        return 'Dialogue: ' + s.join(li)

    def build_comment(self):
        li = []
        s = ','
        for name, value in vars(self).items():
            if value == None:
                value = ''
            li.append(str(value))
        
        return 'Comment: ' + s.join(li)

class Dialogue(ASS_Line):
    def __init__(self, start: str, end: str, name: str = None, text: str = None) -> None:
        super().__init__(start, end, name, text)
        self.layer = 1
        self.style = 'D4DJ 剧情'

class Title(ASS_Line):
    def __init__(self, start: str, end: str, name: str = None, text: str = None) -> None:
        super().__init__(start, end, name, text)
        self.layer = 0
        self.style = 'D4DJ TITLE'

class Shader(ASS_Line):
    def __init__(self, start: str, end: str, name: str = None, text: str = None) -> None:
        super().__init__(start, end, name, text)
        self.layer = 0
        self.style = 'D4DJ shader'

class Caution(ASS_Line):
    def __init__(self, start: str, end: str, name: str = None, text: str = None) -> None:
        super().__init__(start, end, name, text)
        self.layer = 1
        self.style = 'CAUTION'

class AssBuilder(object):
    def __get_tstamp(milliseconds) -> str:
        '''
        将视频进行时的毫秒数转化为aegisub中的时间戳
        '''
        seconds = milliseconds//1000
        milliseconds = milliseconds%1000

        minutes = 0
        hours = 0
        if seconds >= 60:
            minutes = seconds//60
            seconds = seconds % 60

        if minutes >= 60:
            hours = minutes//60
            minutes = minutes % 60

        hr = str(hours)
        m = str(int(minutes)).zfill(2)
        s = str(int(seconds)).zfill(2)
        ms = str(int(milliseconds))[:-1].zfill(2)

        tstamp = '{}:{}:{}.{}'.format(hr, m, s, ms)
        return tstamp
    
    def __shader_builder(length:int, width, height):
        x1b, x2b = sh.Reference.shader_splitter(sh.Reference.reference_reader(sh.Reference.SCREEN_INITIAL, width, height))
        x3b = x2b
        var = int(sh.Reference.reference_reader(sh.Reference.SCREEN_VARIABLE, width, height))

        x1 = x1b + int(var) * length
        x2 = x2b + int(var) * length
        x3 = x3b + int(var) * length

        effect = '{\\p1}'
        shelter_template = sh.Reference.reference_reader(sh.Reference.SCREEN_TEXT, width, height).format(x1, x2, x3)

        return effect + shelter_template

    def write_ass(sce, video, template=None) -> bool:
        cap = cv2.VideoCapture(video)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = round(cap.get(cv2.CAP_PROP_FPS))
        cap.release()

        if width == 0 or height == 0:
            print('请确保视频路径不包含中文字符！')
            return False
        print('视频帧宽度：{}'.format(width))
        print('视频帧高度：{}'.format(height))
        print('FPS: {}'.format(fps))

        ref = sh.AutoRead.get_preferred_ref(width, height)
        if ref == None:
            print('未找到Reference文件！请检查是否存在与视频分辨率相符的Reference！')
            if sh.AutoRead.get_preferred_ref(height, width) != None:
                print('视频文件可能存在翻转，请将其调整为正确的方向！')
            return False
        elif fps < 55:
            print('本程序只支持60hz视频，请确保视频帧率符合要求！')
            return False
        else:
            print('Reference: ' + sh.AutoRead.get_preferred_ref(width, height))
            print('任务开始…')
            ev_sections = DialogueSections.sce_handler(sce)
            if template != None:
                try:
                    ev_sections = DialogueSections.tl_substitude(template, DialogueSections.sce_handler(sce))
                except IndexError:
                    print('请检查模板文件中有无多余换行！')
                    return False
            im_sections, alert_li = ImageSections.jitter_cleaner(ImageSections.image_section_generator(video, width, height))

            dialogue_list = []
            title_list = []
            change_windows = []
            colorfade_li = []
            jitter_list = []

            ass_dialogue = []
            ass_shader = []
            ass_alert = []

            for d in ev_sections:
                if d['EventType'] == 'Dialogue':
                    dialogue_list.append(d)
                if d['EventType'] == 'Title' or d['EventType'] == 'Subtitle':
                    title_list.append(d)
                if d['EventType'] == 'CloseWindow':
                    change_windows.append(d)
                if d['EventType'] == 'Jitter':
                    jitter_list.append(d)

            if change_windows != []:
                for ch in change_windows:
                    if 'Color' in ch:
                        colorfade_li.append(ch['Index'])

            for di, im in zip(dialogue_list, im_sections):
                if 'CloseWindow' in im:
                    open_offset = 0
                    if 'OpenWindow' in im:
                        naming = 'OpenClose'
                        open_offset = int(sh.Settings.settings_reader(sh.Settings.OPEN_BOX_OFFSET))

                    if change_windows != [] and 'Color' in ch and im['Index'] in colorfade_li:
                        naming = 'BlackFade'
                        extra_fad = '{\\fad(0,600)}'
                        text_fad = '{\\fad(0,500)}'
                        fade_offset = int(sh.Settings.settings_reader(sh.Settings.BLACK_FADEIN_OFFSET))
                    else:
                        naming = 'NormalClose'
                        extra_fad = '{\\fad(0,100)}'
                        text_fad = '{\\fad(0,100)}'
                        fade_offset = int(sh.Settings.settings_reader(sh.Settings.NORMAL_CLOSE_OFFSET))
                    line = Dialogue(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End'] + fade_offset), di['Talker'], text = text_fad + di['Body'])
                    shader = Shader(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End'] + fade_offset), name=naming, text=AssBuilder.__shader_builder(len(di['Talker']), width, height) + extra_fad)
                else:
                    open_offset = 0
                    naming = None
                    if 'OpenWindow' in im:
                        open_offset = int(sh.Settings.settings_reader(sh.Settings.OPEN_BOX_OFFSET))
                        naming = 'OpenWindow'
                        
                    line = Dialogue(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End']), di['Talker'], di['Body'])
                    shader = Shader(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End']), name=naming, text=AssBuilder.__shader_builder(len(di['Talker']), width, height))
                shader = shader.build_comment()
                ass_shader.append(shader)
                line = line.build_dialogue()
                ass_dialogue.append(line)

            tit_count = 0
            for ti in title_list:
                title = Title(AssBuilder.__get_tstamp(0), AssBuilder.__get_tstamp(750), name = 'Title' , text = '{\\fad(100,100)}' + ti['Body'])
                title = title.build_dialogue()
                modify_index = tit_count - 1
                ind = ti['Index'] + modify_index
                ass_dialogue.insert(ind, title)
                tit_count += 1

            for a in alert_li:
                alert = Caution(AssBuilder.__get_tstamp(a['Start']), AssBuilder.__get_tstamp(a['End']), 'ALERT', 'PLEASE TAKE NOTICE\\NIT MAY BE A JITTER')
                alert = alert.build_comment()
                ass_alert.append(alert)
            
            src = sh.Settings.settings_reader(sh.Settings.SAMPLE_ASS_PATH, width, height)
            route, name = os.path.split(video)
            shutil.copy(src, route)
            old_name = os.path.join(route, src)
            try:
                new_name = video + '.ass'
                os.rename(old_name, new_name)
            except FileExistsError:
                new_name = video + ' - copy' + '.ass'
                os.rename(old_name, new_name)

            with open(new_name, 'a+', encoding='utf-8') as a:
                for s in ass_shader:
                    a.write(s + '\n')
                for al in ass_alert:
                    a.write(al + '\n')
                for dial in ass_dialogue:
                    a.write(dial + '\n')

            print('任务完成！')
            if len(im_sections) != len(dialogue_list):
                print('共有{}行文本产生偏移，请留意！'.format(abs(len(dialogue_list) - len(im_sections))))
            if jitter_list != []:
                print('剧情内共有{}行抖动出现，请留意！'.format(len(jitter_list)))
            return True

if __name__ == '__main__':
    pass