import json
import logging
import os
import shutil
import time

import cv2
from PySide2.QtCore import QObject, Signal

import settings_handler as sh
from dialogue_sections import DialogueSections
from image_sections import ImageSections

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
    
    chara_dict = sh.Settings.settings_reader(sh.Settings.NAME_STYLES)
    
    def __init__(self, start: str, end: str, name: str = None, text: str = None) -> None:
        super().__init__(start, end, name, text)
        self.layer = 1
        if name in Dialogue.chara_dict:
            self.style = Dialogue.chara_dict[name]
        else:
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

class AssBuilder(QObject):
    text_output = Signal(str) #文字输出到GUI主线程
    send_status = Signal(bool) #告知GUI运行结果，弹出提示框，以及使界面上的两个按钮可用

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
        '''
        根据名字长度以及以分辨率为基础的reference生成随名字长度变化的遮罩字幕
        '''
        x1b, x2b = sh.Reference.shader_splitter(sh.Reference.reference_reader(sh.Reference.SCREEN_INITIAL, width, height))
        x3b = x2b
        var = int(sh.Reference.reference_reader(sh.Reference.SCREEN_VARIABLE, width, height))

        x1 = x1b + int(var) * length
        x2 = x2b + int(var) * length
        x3 = x3b + int(var) * length

        effect = '{\\p1}'
        shelter_template = sh.Reference.reference_reader(sh.Reference.SCREEN_TEXT, width, height).format(x1, x2, x3)

        return effect + shelter_template

    def __write_log(infos:list):
        '''
        传入提示列表，写入log文件内
        '''
        log_path = os.path.join(os.getcwd(), 'ASS-automation.log')
        if os.path.exists(log_path):
            with open(log_path, 'a+', encoding='utf-8') as f:
                f.write('----------------------------------------------------------------\n')
                for i in infos:
                    f.write(i + '\n')
        else:
            with open(log_path, 'w+', encoding='utf-8') as f:
                f.write('###D4DJ-ASS-AUTOMATION-LOG###\n')
                f.write('----------------------------------------------------------------\n')
                for i in infos:
                    f.write(i + '\n')

    def __rename(p_name,n_name):
        #应对出现重复文件的情况
        try:
            os.rename(p_name,n_name)
        except Exception as e:
            if e.args[0] ==17:
                fname, fename = os.path.splitext(n_name)
                n_name = fname+"-1"+fename
                n_name = AssBuilder.__rename(p_name, n_name)
        return n_name

    def __read_temp(route):
        #读取已有的image section
        with open(route, 'r+', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def __write_temp(route, li):
        #将image section储存，便于以后使用更快捷
        with open(route, 'w+', encoding='utf-8') as f:
            json.dump(li, f, indent=2, ensure_ascii=False)

    def write_ass(sce, video, template=None, use_temp=None):
        '''
        根据视频文件和sce文件，生成字幕文件（其中翻译模板template为选择性添加）
        '''
        log_infos = []
        cap = cv2.VideoCapture(video)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = round(cap.get(cv2.CAP_PROP_FPS))
        cap.release()

        if width == 0 or height == 0:
            ab.text_output.emit('请确保视频路径不包含中文字符！')
            ab.send_status.emit(False)
            logging.critical('[ASSautomation] Not reading width & height')
            return
        ab.text_output.emit('视频帧宽度：{}'.format(width))
        ab.text_output.emit('视频帧高度：{}'.format(height))
        ab.text_output.emit('FPS: {}'.format(fps))

        ref = sh.AutoRead.get_preferred_ref(width, height)
        if ref == None:
            ab.text_output.emit('未找到Reference文件！请检查是否存在与视频分辨率相符的Reference！')
            if sh.AutoRead.get_preferred_ref(height, width) != None:
                ab.text_output.emit('视频文件可能存在翻转，请将其调整为正确的方向！')
            ab.send_status.emit(False)
            logging.critical('[ASSautomation] No reference found')
            return
        if fps < 55:
            ab.text_output.emit('本程序只支持60hz视频，请确保视频帧率符合要求！')
            ab.send_status.emit(False)
            logging.critical('[ASSautomation] FPS not supported')
            return
        else:
            t1 = time.time()
            ab.text_output.emit('Reference: ' + sh.AutoRead.get_preferred_ref(width, height))
            #获取sce分析列表
            ev_sections = DialogueSections.sce_handler(sce)
            logging.info('[ASSautomation] Dialogue Sections generated')
            if template != None:
                try:
                    #模板选项不为空时，sce分析列表内的文字将被替换为翻译好的中文
                    ev_sections = DialogueSections.tl_substitude(template, DialogueSections.sce_handler(sce))
                    logging.info('[ASSautomation] Dialogue Sections generated w/ template')
                except IndexError:
                    ab.text_output.emit('请检查模板文件中有无多余换行！')
                    ab.send_status.emit(False)
                    logging.critical('[ASSautomation] IndexError')
                    return
            #获取视频分析列表
            if use_temp:
                im_sections, alert_li = ImageSections.jitter_cleaner(AssBuilder.__read_temp('temp\\' + os.path.split(video)[1] + '.data'))
                logging.info('[ASSautomation] Image Sections generated from Previous Data')
            else:
                #detailed data是拿来测试用的
                generate_detailed_data = False #需要时此项改为True即可
                video_process_method = ImageSections.TEMPLATE_MATCH #选择对话框识别方式
                
                if generate_detailed_data:
                    raw, data = ImageSections.image_section_generator(video, width, height, generate_detailed_data, video_process_method)
                else:
                    raw = ImageSections.image_section_generator(video, width, height, generate_detailed_data, video_process_method)
                AssBuilder.__write_temp('temp\\' + os.path.split(video)[1] + '.data', raw)
                logging.info('[ASSautomation] RAW Image Sections data written')
                im_sections, alert_li = ImageSections.jitter_cleaner(raw)
                logging.info('[ASSautomation] Cleaned Image Sections generated')
                if not os.path.exists('temp'):
                    os.makedirs('temp')
                if generate_detailed_data:
                    AssBuilder.__write_temp('temp\\[DETAILED] ' + os.path.split(video)[1] + '.data', data)
                    logging.info('[ASSautomation] Detailed Image Sections data written')

            dialogue_list = []
            title_list = []
            change_windows = []
            open_windows = []
            change_li = []
            colorfade_li = []
            jitter_list = []

            ass_dialogue = []
            ass_shader = []
            ass_alert = []

            #将sce分析列表内的项目分类
            for d in ev_sections:
                if d['EventType'] == 'Dialogue':
                    dialogue_list.append(d)
                if d['EventType'] == 'Title' or d['EventType'] == 'Subtitle':
                    title_list.append(d)
                if d['EventType'] == 'CloseWindow':
                    change_windows.append(d)
                if d['EventType'] == 'OpenWindow':
                    open_windows.append(d)
                if d['EventType'] == 'Jitter':
                    jitter_list.append(d)

            #为有颜色变化的对话框消失做标记，分类到专门的黑\白屏列表中
            if change_windows != []:
                for ch in change_windows:
                    change_li.append(ch['Index'])
                    if 'Color' in ch:
                        colorfade_li.append(ch['Index'])

            if len(dialogue_list) == len(im_sections):
                for o in open_windows:
                    for ims in im_sections:
                        if ims['Index'] == o['Index']:
                            if o['EventType'] not in ims:
                                ims[o['EventType']] = True
                            break
                for c in change_windows:
                    for ims in im_sections:
                        if ims['Index'] == c['Index']:
                            if c['EventType'] not in ims:
                                ims[c['EventType']] = True
                            break

            for di, im in zip(dialogue_list, im_sections):
                if 'CloseWindow' in im:
                    open_offset = 0
                    if 'OpenWindow' in im:
                        open_offset = int(sh.Settings.settings_reader(sh.Settings.OPEN_BOX_OFFSET))

                    if change_windows != [] and im['Index'] in colorfade_li:
                        #黑屏
                        naming = 'BlackFade'
                        extra_fad = '{\\fad(0,500)}'
                        text_fad = '{\\fad(0,500)}'
                        extra_cut = 0
                        if 'Fade' in change_windows[change_li.index(im['Index'])]:
                            base_fade_amount = 400
                            base_cut_amount = 300
                            multiply_index = change_windows[change_li.index(im['Index'])]['Fade']
                            
                            if video_process_method == ImageSections.TEMPLATE_MATCH:
                                if multiply_index == 0.25:
                                    extra_cut -= 50
                            elif video_process_method == ImageSections.COLOR_DETECT:
                                base_cut_amount = base_fade_amount
                            
                            naming = 'BlackFade ({})'.format(multiply_index)
                            extra_fad = '{\\fad(0,' + str(100 + int(base_fade_amount * multiply_index)) + ')}'
                            text_fad = '{\\fad(0,' + str(100 + int(base_fade_amount * multiply_index)) + ')}'
                            extra_cut = int(base_cut_amount - base_cut_amount * multiply_index)
                        fade_offset = int(sh.Settings.settings_reader(sh.Settings.BLACK_FADEIN_OFFSET)) - extra_cut
                    else:
                        #普通对话框消失
                        naming = 'NormalClose'
                        if 'OpenWindow' in im:
                            naming = 'OpenClose'
                        extra_fad = '{\\fad(0,100)}'
                        text_fad = '{\\fad(0,100)}'
                        fade_offset = int(sh.Settings.settings_reader(sh.Settings.NORMAL_CLOSE_OFFSET))
                    #创建文本行和对应的遮罩行
                    line = Dialogue(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End'] + fade_offset), di['Talker'], text = text_fad + di['Body'])
                    shader = Shader(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End'] + fade_offset), name=naming, text=AssBuilder.__shader_builder(len(di['Talker']), width, height) + extra_fad)
                elif change_windows != [] and im['Index'] in colorfade_li:
                    #白屏
                    naming = 'WhiteFade'
                    extra_fad = '{\\fad(0,500)}'
                    text_fad = '{\\fad(0,500)}'
                    extra_cut = 0
                    if 'Fade' in change_windows[change_li.index(im['Index'])]:
                        base_fade_amount = 400
                        base_cut_amount = 300
                        multiply_index = change_windows[change_li.index(im['Index'])]['Fade']
                        
                        if video_process_method == ImageSections.TEMPLATE_MATCH:
                            if multiply_index == 0.25:
                                extra_cut -= 50
                        elif video_process_method == ImageSections.COLOR_DETECT:
                            base_cut_amount = base_fade_amount
                        
                        naming = 'WhiteFade ({})'.format(multiply_index)
                        extra_fad = '{\\fad(0,' + str(100 + int(base_fade_amount * multiply_index)) + ')}'
                        text_fad = '{\\fad(0,' + str(100 + int(base_fade_amount * multiply_index)) + ')}'
                        extra_cut = int(base_cut_amount - base_cut_amount * multiply_index)
                    fade_offset = int(sh.Settings.settings_reader(sh.Settings.BLACK_FADEIN_OFFSET)) - extra_cut
                    line = Dialogue(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End'] + fade_offset), di['Talker'], text = text_fad + di['Body'])
                    shader = Shader(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End'] + fade_offset), name=naming, text=AssBuilder.__shader_builder(len(di['Talker']), width, height) + extra_fad)
                else:
                    open_offset = 0
                    naming = None
                    if 'OpenWindow' in im:
                        #对话框出现
                        open_offset = int(sh.Settings.settings_reader(sh.Settings.OPEN_BOX_OFFSET))
                        naming = 'OpenWindow'
                    #创建文本行和对应的遮罩行
                    line = Dialogue(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End']), di['Talker'], di['Body'])
                    shader = Shader(AssBuilder.__get_tstamp(im['Start'] + open_offset), AssBuilder.__get_tstamp(im['End']), name=naming, text=AssBuilder.__shader_builder(len(di['Talker']), width, height))
                shader = shader.build_comment() #转化为ass内的格式
                ass_shader.append(shader)
                line = line.build_dialogue() #转化为ass内的格式
                ass_dialogue.append(line)

            #标题行填入
            tit_count = 0
            for i in range(len(title_list)):
                ti = title_list[i]
                modify_index = tit_count - 1
                ind = ti['Index'] + modify_index
                for d in im_sections:
                    if d['Index'] == ti['Index']:
                        start = d['Start']
                        break
                
                #连续标题行处理
                extra = 0
                cont_index = 1
                while ti != title_list[-1] and title_list[i+cont_index]['Index'] == ti['Index']:
                    extra += 1000
                    cont_index += 1
                    if i + cont_index == len(title_list):
                        break

                title = Title(AssBuilder.__get_tstamp(start - 1130 - extra), AssBuilder.__get_tstamp(start - 380 - extra), name = 'Title' , text = '{\\fad(100,100)}' + ti['Body'])
                title = title.build_dialogue()
                ass_dialogue.insert(ind, title)
                tit_count += 1

            #警告列表填入
            for a in alert_li:
                alert = Caution(AssBuilder.__get_tstamp(a['Start']), AssBuilder.__get_tstamp(a['End']), 'ALERT', 'PLEASE TAKE NOTICE\\NIT MAY BE A JITTER')
                alert = alert.build_comment()
                ass_alert.append(alert)
            
            #复制untitled文件至视频同目录，并进行重命名
            src = sh.Settings.settings_reader(sh.Settings.SAMPLE_ASS_PATH, width, height)
            route, vid_name = os.path.split(video)
            shutil.copy(src, route)
            logging.info('[ASSautomation] Untitled.ass copied to destination')
            old_name = os.path.join(route, src)
            new_name = os.path.join(route, video + '.ass')
            new_name = AssBuilder.__rename(old_name, new_name)

            pop_instruction = 1
            log_infos.append('TASK-VIDEO = {}'.format(vid_name))
            if use_temp:
                pop_instruction += 1
                log_infos.append('USE-SAVED-DATA = {}'.format(os.path.split(video)[1] + '.data'))

            #写入字幕至复制出的untitled文件
            with open(new_name, 'a+', encoding='utf-8') as a:
                for s in ass_shader:
                    a.write(s + '\n')
                for al in ass_alert:
                    a.write(al + '\n')
                for dial in ass_dialogue:
                    a.write(dial + '\n')
            logging.info('[ASSautomation] ASS file has written')

            if not use_temp:
                t2 = time.time()
                process_time = t2 - t1
                length = total_frame / fps
                ab.text_output.emit('运行时间/视频时长 比例：{}'.format(round(process_time / length, 2)))
            if len(im_sections) != len(dialogue_list):
                ab.text_output.emit('共有{}行文本产生偏移，请留意！'.format(abs(len(dialogue_list) - len(im_sections))))
                log_infos.append('偏移文本行数：{}'.format(abs(len(dialogue_list) - len(im_sections))))
            if jitter_list != []:
                ab.text_output.emit('剧情内共有{}行抖动出现，请留意！'.format(len(jitter_list)))
                log_infos.append('抖动行数：{}（具体位置如下）'.format(len(jitter_list)))
                for j in jitter_list:
                    s = ''
                    for key, value in j.items():
                        s += '{}: {} '.format(key, value)
                    log_infos.append(s)
            if log_infos != []:
                if len(log_infos) > pop_instruction:    
                    ab.text_output.emit('上述提示已添加至：ASS-automation.log')
                else:
                    log_infos.append('ALL-CLEAR')
                AssBuilder.__write_log(log_infos)
            logging.info('[ASSautomation] User log has written')
                
            ab.send_status.emit(True)

ab = AssBuilder() #为GUI信号输出创建的实例

if __name__ == '__main__':
    pass
